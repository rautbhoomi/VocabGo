"""Benchmarking utility for AI Language Assistant (OpenAI API edition).

Measures:
- Per-prompt response time
- Average response time
- Success rate
- Output quality samples

Runs against OpenAI API models (requires active internet connection and OPENAI_API_KEY).
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List
from dotenv import load_dotenv

from src.language_tasks import create_prompt
from src.model import get_openai_client, query_openai_model, DEFAULT_MODEL_NAME

load_dotenv()

BENCHMARK_DATASET_PATH = os.path.join(
    os.path.dirname(__file__), "benchmark_dataset.json"
)


def load_benchmark_dataset() -> Dict[str, List[Dict[str, Any]]]:
    """Loads the benchmark dataset from JSON."""
    if not os.path.exists(BENCHMARK_DATASET_PATH):
        raise FileNotFoundError(f"Benchmark dataset not found at {BENCHMARK_DATASET_PATH}")
    with open(BENCHMARK_DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_benchmark(model_name: str, output_file: str = None):
    """Runs all benchmark test cases against the specified OpenAI model."""
    print(f"\n=======================================================")
    print(f" AI Language Assistant - OpenAI Benchmark Runner")
    print(f" Model: {model_name}")
    print(f"=======================================================\n")

    # Step 1: Pre-flight check for API Key
    try:
        client = get_openai_client()
    except ValueError as err:
        print(f"[ERROR] {err}")
        print("Please configure your OPENAI_API_KEY in the .env file before running benchmarks.")
        sys.exit(1)

    # Step 2: Load benchmark dataset
    dataset = load_benchmark_dataset()
    results = []
    total_time = 0.0
    successful_runs = 0

    categories = ["translation", "grammar", "rewriting", "simplification"]

    for category in categories:
        items = dataset.get(category, [])
        print(f"--- Running {category.upper()} tests ({len(items)} cases) ---")

        for item in items:
            item_id = item.get("id", "unknown")
            task = item["task"]
            user_input = item["input"]
            language = item.get("language")
            style = item.get("style")

            prompt = create_prompt(
                task=task,
                text=user_input,
                language=language,
                style=style,
            )

            print(f"[{item_id}] Processing...", end="", flush=True)
            result = query_openai_model(
                prompt=prompt,
                model_name=model_name,
                client=client,
            )

            if result["success"]:
                elapsed = result["elapsed_seconds"]
                total_time += elapsed
                successful_runs += 1
                print(f" DONE in {elapsed:.2f}s")
                results.append({
                    "id": item_id,
                    "category": category,
                    "task": task,
                    "input": user_input,
                    "language": language,
                    "style": style,
                    "response": result["response"],
                    "elapsed_seconds": elapsed,
                    "success": True,
                })
            else:
                print(f" FAILED: {result['error']}")
                results.append({
                    "id": item_id,
                    "category": category,
                    "task": task,
                    "input": user_input,
                    "language": language,
                    "style": style,
                    "response": "",
                    "elapsed_seconds": result["elapsed_seconds"],
                    "success": False,
                    "error": result["error"],
                })

        print()

    # Step 3: Print summary
    total_count = len(results)
    avg_time = (total_time / successful_runs) if successful_runs > 0 else 0.0

    print("=======================================================")
    print(" Benchmark Summary")
    print("=======================================================")
    print(f"Model Tested:          {model_name}")
    print(f"Total Test Cases:      {total_count}")
    print(f"Successful:            {successful_runs}/{total_count}")
    print(f"Average Response Time: {avg_time:.2f} seconds")
    print("=======================================================\n")

    # Step 4: Optional save
    if output_file:
        summary_payload = {
            "model": model_name,
            "total_cases": total_count,
            "successful_cases": successful_runs,
            "average_response_time_seconds": round(avg_time, 2),
            "results": results,
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summary_payload, f, indent=2, ensure_ascii=False)
        print(f"Detailed results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run benchmark tests for AI Language Assistant via OpenAI API"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL_NAME,
        help=f"OpenAI model identifier to test (default: {DEFAULT_MODEL_NAME})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional path to save JSON benchmark results",
    )
    args = parser.parse_args()
    run_benchmark(model_name=args.model, output_file=args.output)


if __name__ == "__main__":
    main()

"""Local Ollama model communication module.

Handles:
- Direct HTTP communication with the local Ollama API
- Model execution timing (response speed measurement)
- Connection and model-not-found error handling
- Zero cloud dependencies / strictly local execution
"""

import os
import time
from typing import Any, Dict, List, Optional
import requests

# Default local model name - configurable in one place
# Can also be overridden by setting the OLLAMA_MODEL environment variable
DEFAULT_MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

# Ollama local API base URL (standard Ollama port is 11434)
DEFAULT_OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

# Recommended lightweight models suitable for local laptops
RECOMMENDED_MODELS = [
    "llama3.2:1b",
    "qwen2.5:1.5b",
    "llama3.2:3b",
    "qwen2.5:0.5b",
]


def check_ollama_status(api_base: str = DEFAULT_OLLAMA_HOST) -> Dict[str, Any]:
    """Checks whether the local Ollama daemon is running and lists installed models.

    Args:
        api_base: Base URL for the local Ollama API.

    Returns:
        Dict containing:
            - 'running' (bool): True if Ollama service responds.
            - 'models' (List[str]): List of locally installed model names.
            - 'error' (Optional[str]): Error message if Ollama is unreachable.
    """
    try:
        response = requests.get(f"{api_base}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models_list = [m.get("name", "") for m in data.get("models", [])]
            return {
                "running": True,
                "models": models_list,
                "raw_models": data.get("models", []),
                "error": None,
            }
        else:
            return {
                "running": False,
                "models": [],
                "error": f"Ollama returned unexpected HTTP status {response.status_code}.",
            }
    except requests.exceptions.ConnectionError:
        return {
            "running": False,
            "models": [],
            "error": "Ollama is not running.\n\nPlease start Ollama and try again.",
        }
    except Exception as exc:
        return {
            "running": False,
            "models": [],
            "error": f"Could not connect to Ollama: {str(exc)}",
        }


def query_local_model(
    prompt: str,
    model_name: str = DEFAULT_MODEL_NAME,
    api_base: str = DEFAULT_OLLAMA_HOST,
    timeout: int = 180,
) -> Dict[str, Any]:
    """Sends a prompt to the local Ollama instance and returns the generated text.

    Args:
        prompt: The fully formatted task prompt.
        model_name: The name of the local Ollama model (e.g. 'llama3.2:1b').
        api_base: Base URL of the local Ollama server.
        timeout: Maximum seconds to wait for model response.

    Returns:
        Dict containing:
            - 'success' (bool): True if response received successfully.
            - 'response' (str): Generated text from local model.
            - 'elapsed_seconds' (float): Time taken to complete the request.
            - 'error' (Optional[str]): Friendly error message if call failed.
            - 'model' (str): Model name used for inference.
    """
    start_time = time.perf_counter()
    url = f"{api_base}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=timeout)
        elapsed_seconds = round(time.perf_counter() - start_time, 2)

        # Handle 404: Model not found
        if response.status_code == 404:
            return {
                "success": False,
                "response": "",
                "elapsed_seconds": elapsed_seconds,
                "error": (
                    f"Model '{model_name}' has not been downloaded in Ollama.\n\n"
                    f"To install this model locally, open your terminal and run:\n"
                    f"ollama run {model_name}"
                ),
                "model": model_name,
            }

        # Check for non-200 HTTP statuses
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                if "error" in error_json:
                    error_detail = error_json["error"]
            except Exception:
                pass

            # Detect "not found" in error message
            if "not found" in error_detail.lower():
                return {
                    "success": False,
                    "response": "",
                    "elapsed_seconds": elapsed_seconds,
                    "error": (
                        f"Model '{model_name}' has not been downloaded in Ollama.\n\n"
                        f"To install this model locally, open your terminal and run:\n"
                        f"ollama run {model_name}"
                    ),
                    "model": model_name,
                }

            return {
                "success": False,
                "response": "",
                "elapsed_seconds": elapsed_seconds,
                "error": f"Ollama returned an error (HTTP {response.status_code}): {error_detail}",
                "model": model_name,
            }

        # Success - parse response
        data = response.json()
        generated_text = data.get("response", "").strip()

        return {
            "success": True,
            "response": generated_text,
            "elapsed_seconds": elapsed_seconds,
            "error": None,
            "model": model_name,
        }

    except requests.exceptions.ConnectionError:
        elapsed_seconds = round(time.perf_counter() - start_time, 2)
        return {
            "success": False,
            "response": "",
            "elapsed_seconds": elapsed_seconds,
            "error": "Ollama is not running.\n\nPlease start Ollama and try again.",
            "model": model_name,
        }

    except requests.exceptions.Timeout:
        elapsed_seconds = round(time.perf_counter() - start_time, 2)
        return {
            "success": False,
            "response": "",
            "elapsed_seconds": elapsed_seconds,
            "error": (
                f"The request timed out after {timeout} seconds. "
                "The local model took too long to respond. "
                "Try using a smaller model (such as llama3.2:1b or qwen2.5:0.5b)."
            ),
            "model": model_name,
        }

    except Exception as exc:
        elapsed_seconds = round(time.perf_counter() - start_time, 2)
        return {
            "success": False,
            "response": "",
            "elapsed_seconds": elapsed_seconds,
            "error": f"An unexpected error occurred: {str(exc)}",
            "model": model_name,
        }

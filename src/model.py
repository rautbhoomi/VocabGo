"""OpenAI model communication module.

Handles:
- Direct interaction with OpenAI Chat Completions API
- Secure API key retrieval via python-dotenv / environment variables
- Error handling for API authentication, rate limits, and connection issues
- Response latency measurement
"""

import os
import time
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Default model name
DEFAULT_MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5-mini")


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Returns an initialized OpenAI client using the provided or environment API key.

    Args:
        api_key: Optional API key. If omitted, loaded from OPENAI_API_KEY env var.

    Raises:
        ValueError: If no valid API key is found.
    """
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key or key.strip() == "" or key.strip() == "YOUR_API_KEY_HERE":
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."
        )
    return OpenAI(api_key=key.strip())


def query_openai_model(
    prompt: str,
    model_name: str = DEFAULT_MODEL_NAME,
    client: Optional[OpenAI] = None,
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """Sends a task prompt to OpenAI's Chat Completions API and measures latency.

    Args:
        prompt: Formatted task prompt.
        model_name: OpenAI model identifier (e.g. 'gpt-5-mini', 'gpt-4o-mini').
        client: Optional OpenAI client instance.
        temperature: Sampling temperature.

    Returns:
        Dict containing:
            - 'success' (bool): True if API responded successfully.
            - 'response' (str): Generated response text.
            - 'elapsed_seconds' (float): Time taken in seconds.
            - 'error' (Optional[str]): Error message if call failed.
            - 'model' (str): Model name used.
    """
    start_time = time.perf_counter()

    try:
        if client is None:
            client = get_openai_client()

        chat_completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, accurate, and concise AI language assistant. "
                        "Always follow the instructions and return only the requested output."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )

        elapsed_seconds = round(time.perf_counter() - start_time, 2)
        generated_text = chat_completion.choices[0].message.content.strip()

        return {
            "success": True,
            "response": generated_text,
            "elapsed_seconds": elapsed_seconds,
            "error": None,
            "model": model_name,
        }

    except Exception as exc:
        elapsed_seconds = round(time.perf_counter() - start_time, 2)
        return {
            "success": False,
            "response": "",
            "elapsed_seconds": elapsed_seconds,
            "error": str(exc),
            "model": model_name,
        }

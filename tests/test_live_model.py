"""Live model integration tests for AI Language Assistant (OpenAI API edition).

These tests run against the live OpenAI API and are automatically
skipped if a valid OPENAI_API_KEY is not configured in .env.
"""

import os
import unittest
from dotenv import load_dotenv
from src.language_tasks import create_prompt, TASK_TRANSLATE
from src.model import query_openai_model

load_dotenv()


class TestLiveOpenAIIntegration(unittest.TestCase):
    """Integration tests running against OpenAI's live API."""

    @classmethod
    def setUpClass(cls):
        """Check if a valid OpenAI API key is set."""
        cls.api_key = os.getenv("OPENAI_API_KEY", "")
        cls.has_valid_key = bool(
            cls.api_key and cls.api_key.strip() != "YOUR_API_KEY_HERE"
        )

    def test_live_translation(self):
        """Test live model response if valid OpenAI API key is present."""
        if not self.has_valid_key:
            self.skipTest(
                "OPENAI_API_KEY is not configured or is placeholder. Skipping live test."
            )

        prompt = create_prompt(
            task=TASK_TRANSLATE,
            text="Hello, welcome to our office.",
            language="Hindi",
        )
        result = query_openai_model(prompt=prompt, model_name="gpt-4o-mini")
        self.assertTrue(result["success"])
        self.assertGreater(len(result["response"]), 0)
        self.assertGreater(result["elapsed_seconds"], 0)


if __name__ == "__main__":
    unittest.main()

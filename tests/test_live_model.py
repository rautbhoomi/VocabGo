"""Live model integration tests for Offline Language Assistant.

These tests run against a live local Ollama instance and are automatically
skipped if Ollama is not running or the model is not installed.
"""

import unittest
from src.model import check_ollama_status, query_local_model, DEFAULT_MODEL_NAME
from src.language_tasks import create_prompt, TASK_TRANSLATE


class TestLiveModelIntegration(unittest.TestCase):
    """Integration tests running against local Ollama service."""

    @classmethod
    def setUpClass(cls):
        """Check if local Ollama service is reachable."""
        cls.status = check_ollama_status()
        cls.is_ollama_running = cls.status["running"]
        cls.installed_models = cls.status.get("models", [])

    def test_live_translation(self):
        """Test live model response if Ollama and the model are available."""
        if not self.is_ollama_running:
            self.skipTest("Ollama is not running locally. Skipping live test.")

        if DEFAULT_MODEL_NAME not in self.installed_models:
            self.skipTest(f"Model '{DEFAULT_MODEL_NAME}' is not downloaded. Skipping live test.")

        prompt = create_prompt(
            task=TASK_TRANSLATE,
            text="Hello, welcome to our office.",
            language="Hindi",
        )
        result = query_local_model(prompt=prompt, model_name=DEFAULT_MODEL_NAME)
        self.assertTrue(result["success"])
        self.assertGreater(len(result["response"]), 0)
        self.assertGreater(result["elapsed_seconds"], 0)


if __name__ == "__main__":
    unittest.main()

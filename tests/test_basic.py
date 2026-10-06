"""Unit tests for Offline Language Assistant.

Tests:
- Prompt generation
- Translation prompt creation (English, Hindi, Marathi)
- Grammar prompt creation
- Rewrite prompt creation (Professional, Simple, Friendly)
- Simplification prompt creation
- Empty input handling
- Graceful offline error handling

Does NOT require a downloaded AI model or running Ollama daemon.
"""

import unittest
from src.language_tasks import (
    TASK_TRANSLATE,
    TASK_GRAMMAR,
    TASK_REWRITE,
    TASK_SIMPLIFY,
    create_prompt,
)
from src.model import query_local_model, check_ollama_status


class TestPromptGeneration(unittest.TestCase):
    """Tests for prompt creation logic."""

    def test_translation_prompt_creation(self):
        """Test translation prompt generation for English, Hindi, and Marathi."""
        sample_text = "Good morning, how are you today?"

        for lang in ["Hindi", "Marathi", "English"]:
            prompt = create_prompt(
                task=TASK_TRANSLATE,
                text=sample_text,
                language=lang,
            )
            self.assertIn(f"Translate the following text into {lang}.", prompt)
            self.assertIn(sample_text, prompt)
            self.assertIn("Return only the translated text.", prompt)

    def test_grammar_prompt_creation(self):
        """Test grammar correction prompt generation."""
        sample_text = "He go to school yesterday and he eat a apple."
        prompt = create_prompt(
            task=TASK_GRAMMAR,
            text=sample_text,
        )
        self.assertIn("Correct the grammar, spelling, punctuation", prompt)
        self.assertIn(sample_text, prompt)
        self.assertIn("Return only the corrected text.", prompt)

    def test_rewrite_prompt_creation(self):
        """Test rewrite prompt generation across all supported styles."""
        sample_text = "Hey boss, won't make it today. Sick."

        for style in ["Professional", "Simple", "Friendly"]:
            prompt = create_prompt(
                task=TASK_REWRITE,
                text=sample_text,
                style=style,
            )
            self.assertIn(f"Rewrite the following text in a {style} style.", prompt)
            self.assertIn(sample_text, prompt)
            self.assertIn("Return only the rewritten text.", prompt)

    def test_simplification_prompt_creation(self):
        """Test text simplification prompt generation."""
        sample_text = (
            "The photosynthetic mechanism in vascular flora orchestrates "
            "the photochemical conversion of irradiance into saccharides."
        )
        prompt = create_prompt(
            task=TASK_SIMPLIFY,
            text=sample_text,
        )
        self.assertIn("Rewrite the following text using simple and easy-to-understand language.", prompt)
        self.assertIn(sample_text, prompt)
        self.assertIn("Return only the simplified text.", prompt)

    def test_empty_input_handling(self):
        """Test that empty or whitespace input raises ValueError with the expected message."""
        empty_inputs = ["", "   ", "\n\t", None]
        for empty_text in empty_inputs:
            with self.assertRaises(ValueError) as context:
                create_prompt(task=TASK_GRAMMAR, text=empty_text)
            self.assertEqual(str(context.exception), "Please enter some text first.")

    def test_missing_language_for_translation(self):
        """Test that translating without a target language raises an error."""
        with self.assertRaises(ValueError) as context:
            create_prompt(task=TASK_TRANSLATE, text="Hello", language=None)
        self.assertIn("Please select a target language", str(context.exception))

    def test_missing_style_for_rewriting(self):
        """Test that rewriting without a style raises an error."""
        with self.assertRaises(ValueError) as context:
            create_prompt(task=TASK_REWRITE, text="Hello", style=None)
        self.assertIn("Please select a style", str(context.exception))

    def test_unsupported_task(self):
        """Test that unknown tasks raise an unsupported task error."""
        with self.assertRaises(ValueError) as context:
            create_prompt(task="Unknown Task", text="Hello")
        self.assertIn("Unsupported task", str(context.exception))


class TestModelOfflineHandling(unittest.TestCase):
    """Tests for model communication error handling when Ollama is offline."""

    def test_check_ollama_status_offline(self):
        """Test check_ollama_status against an invalid port returns running=False."""
        # Port 65530 is an unused local port to simulate offline Ollama
        status = check_ollama_status(api_base="http://127.0.0.1:65530")
        self.assertFalse(status["running"])
        self.assertEqual(status["models"], [])
        self.assertIn("Ollama is not running", status["error"])

    def test_query_local_model_offline(self):
        """Test query_local_model against an offline port returns a friendly error message."""
        result = query_local_model(
            prompt="Hello",
            model_name="llama3.2:1b",
            api_base="http://127.0.0.1:65530",
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["response"], "")
        self.assertIn("Ollama is not running", result["error"])
        self.assertIn("Please start Ollama and try again", result["error"])


if __name__ == "__main__":
    unittest.main()

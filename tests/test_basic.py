"""Unit tests for AI Language Assistant (OpenAI API edition).

Tests prompt generation, task mappings, input validation, and secure key checking.
Does NOT require an active internet connection or a real OpenAI API key to run.
"""

import unittest
from src.language_tasks import (
    TASK_TRANSLATE,
    TASK_GRAMMAR,
    TASK_REWRITE,
    TASK_SIMPLIFY,
    create_prompt,
)
from src.model import get_openai_client


class TestPromptGeneration(unittest.TestCase):
    """Tests for prompt creation logic and task routing."""

    def test_translation_prompt_creation(self):
        """Test translation prompt generation for English, Hindi, and Marathi."""
        sample_text = "Water is essential for all known forms of life."

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
        sample_text = "She do not knows where the books was kept yesterday."
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
            "Decentralized execution paradigms provide latency mitigation and privacy guarantees."
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


class TestAPIKeyValidation(unittest.TestCase):
    """Tests for secure API key validation without exposing secrets."""

    def test_placeholder_or_empty_api_key_raises_error(self):
        """Test that missing or placeholder API key raises a clear ValueError."""
        invalid_keys = ["", "   ", "YOUR_API_KEY_HERE", None]
        for key in invalid_keys:
            with self.assertRaises(ValueError) as context:
                get_openai_client(api_key=key)
            self.assertIn("OpenAI API key not found", str(context.exception))


if __name__ == "__main__":
    unittest.main()

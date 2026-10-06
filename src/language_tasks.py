"""Language tasks mapping and prompt generation module.

Maps user-selected tasks and parameters (language, style) to prompt templates.
Designed to be modular, robust, and beginner-friendly.
"""

from typing import Optional
from src.prompts import (
    TRANSLATION_PROMPT,
    GRAMMAR_PROMPT,
    REWRITE_PROMPT,
    SIMPLIFICATION_PROMPT,
)

# Supported language tasks
TASK_TRANSLATE = "Translate"
TASK_GRAMMAR = "Correct Grammar"
TASK_REWRITE = "Rewrite"
TASK_SIMPLIFY = "Simplify"

SUPPORTED_TASKS = [
    TASK_TRANSLATE,
    TASK_GRAMMAR,
    TASK_REWRITE,
    TASK_SIMPLIFY,
]

# Supported languages for translation
SUPPORTED_LANGUAGES = ["English", "Hindi", "Marathi"]

# Supported styles for rewriting
SUPPORTED_STYLES = ["Professional", "Simple", "Friendly"]


def create_prompt(
    task: str,
    text: str,
    language: Optional[str] = None,
    style: Optional[str] = None,
) -> str:
    """Creates a formatted prompt for the specified language task.

    Args:
        task: The task to perform (Translate, Correct Grammar, Rewrite, Simplify).
        text: The input text to process.
        language: Target language for translation (e.g. 'Hindi', 'Marathi', 'English').
        style: Style for rewriting (e.g. 'Professional', 'Simple', 'Friendly').

    Returns:
        Formatted prompt string ready for model inference.

    Raises:
        ValueError: If input text is empty or required arguments are missing/invalid.
    """
    cleaned_text = text.strip() if text else ""
    if not cleaned_text:
        raise ValueError("Please enter some text first.")

    normalized_task = task.strip().lower()

    # Translation
    if normalized_task in ("translate", "translation"):
        if not language:
            raise ValueError("Please select a target language for translation.")
        return TRANSLATION_PROMPT.format(language=language.strip(), text=cleaned_text)

    # Grammar Correction
    elif normalized_task in ("correct grammar", "grammar", "grammar correction", "grammar_correction"):
        return GRAMMAR_PROMPT.format(text=cleaned_text)

    # Text Rewriting
    elif normalized_task in ("rewrite", "text rewriting", "rewriting", "text_rewriting"):
        if not style:
            raise ValueError("Please select a style for text rewriting.")
        return REWRITE_PROMPT.format(style=style.strip(), text=cleaned_text)

    # Text Simplification
    elif normalized_task in ("simplify", "simplification", "text simplification", "text_simplification"):
        return SIMPLIFICATION_PROMPT.format(text=cleaned_text)

    else:
        valid_tasks_str = ", ".join(SUPPORTED_TASKS)
        raise ValueError(
            f"Unsupported task '{task}'. Supported tasks are: {valid_tasks_str}."
        )

"""Prompt templates for Offline Language Assistant tasks.

Contains prompt templates for:
- Translation
- Grammar correction
- Text rewriting
- Text simplification
"""

# Translation prompt template
TRANSLATION_PROMPT = """Translate the following text into {language}.

Preserve the original meaning, tone, and important details.

Return only the translated text.

Text:
{text}"""

# Grammar correction prompt template
GRAMMAR_PROMPT = """Correct the grammar, spelling, punctuation, and sentence structure of the following text.

Preserve the original meaning.

Return only the corrected text.

Text:
{text}"""

# Text rewriting prompt template
REWRITE_PROMPT = """Rewrite the following text in a {style} style.

Preserve the original meaning and important information.

Return only the rewritten text.

Text:
{text}"""

# Text simplification prompt template
SIMPLIFICATION_PROMPT = """Rewrite the following text using simple and easy-to-understand language.

Preserve the original meaning and important information.

Return only the simplified text.

Text:
{text}"""

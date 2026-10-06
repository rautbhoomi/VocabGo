"""Offline Language Assistant - Streamlit Frontend Application.

Runs 100% locally on the user's machine using Ollama.
No cloud APIs, no external dependencies, completely offline-capable.
"""

import streamlit as st
from src.language_tasks import (
    TASK_TRANSLATE,
    TASK_GRAMMAR,
    TASK_REWRITE,
    TASK_SIMPLIFY,
    SUPPORTED_TASKS,
    SUPPORTED_LANGUAGES,
    SUPPORTED_STYLES,
    create_prompt,
)
from src.model import (
    DEFAULT_MODEL_NAME,
    RECOMMENDED_MODELS,
    check_ollama_status,
    query_local_model,
)

# Page configuration
st.set_page_config(
    page_title="Offline Language Assistant",
    page_icon="🌐",
    layout="centered",
)

# Sidebar: Local Environment & Model Configuration
st.sidebar.title("⚙️ Local Configuration")

# Check local Ollama status
status = check_ollama_status()
if status["running"]:
    st.sidebar.success("🟢 Ollama: Running (Local)")
    installed_models = status.get("models", [])
    if installed_models:
        default_index = 0
        if DEFAULT_MODEL_NAME in installed_models:
            default_index = installed_models.index(DEFAULT_MODEL_NAME)
        selected_model = st.sidebar.selectbox(
            "Installed Models:",
            options=installed_models,
            index=default_index,
            help="Select one of your installed local Ollama models.",
        )
    else:
        st.sidebar.warning("⚠️ No models installed yet.")
        selected_model = st.sidebar.text_input(
            "Model Name:",
            value=DEFAULT_MODEL_NAME,
            help="Type the name of the model you plan to run (e.g. llama3.2:1b).",
        )
else:
    st.sidebar.error("🔴 Ollama: Not Running")
    st.sidebar.info(
        "**To start Ollama:**\n\n"
        "1. Open a terminal and run:\n"
        "   ```bash\n"
        "   ollama serve\n"
        "   ```\n"
        "2. Or open the Ollama desktop app."
    )
    selected_model = st.sidebar.text_input(
        "Target Model Name:",
        value=DEFAULT_MODEL_NAME,
    )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "### 💡 Recommended Small Models\n"
    "- `llama3.2:1b` (~1.3 GB, fast)\n"
    "- `qwen2.5:1.5b` (~1.0 GB, multilingual)\n"
    "- `llama3.2:3b` (~2.0 GB, high quality)\n\n"
    "Run `ollama run <model>` to download."
)
st.sidebar.markdown("---")
st.sidebar.caption("🔒 **100% Offline & Private**\nAll inference runs on your local machine.")

# Main Application Header
st.title("🌐 Offline Language Assistant")
st.write("An AI language assistant that runs locally on your computer.")

st.markdown("---")

# Task Selector
task = st.selectbox("Choose a task:", options=SUPPORTED_TASKS)

# Task-specific Options
target_language = None
rewrite_style = None

if task == TASK_TRANSLATE:
    target_language = st.selectbox("Translate to:", options=SUPPORTED_LANGUAGES)
elif task == TASK_REWRITE:
    rewrite_style = st.selectbox("Choose a style:", options=SUPPORTED_STYLES)

# Text Input Area
user_text = st.text_area(
    "Enter your text:",
    height=140,
    placeholder="Enter the text you want to process...",
)

# Process Button
if st.button("Process", type="primary", use_container_width=True):
    # Validation 1: Empty input check
    if not user_text or not user_text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            # Build prompt
            prompt = create_prompt(
                task=task,
                text=user_text,
                language=target_language,
                style=rewrite_style,
            )

            # Query local model with spinner
            with st.spinner("Processing locally with Ollama..."):
                result = query_local_model(
                    prompt=prompt,
                    model_name=selected_model,
                )

            # Handle model errors gracefully
            if not result["success"]:
                st.error(result["error"])
            else:
                st.markdown("### Output:")
                st.info(result["response"])
                st.caption(f"Processing time: {result['elapsed_seconds']} seconds")

        except ValueError as val_err:
            st.warning(str(val_err))
        except Exception as exc:
            st.error(f"An unexpected error occurred: {str(exc)}")

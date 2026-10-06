"""AI Language Assistant - Streamlit Frontend Application.

Uses the OpenAI API for language tasks:
- Translation (English, Hindi, Marathi)
- Grammar Correction
- Text Rewriting (Professional, Simple, Friendly)
- Text Simplification

Requires an active internet connection and an OpenAI API key in .env.
"""

import os
import time

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

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

# Load environment variables securely from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Configurable model name near the top of the file
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5-mini")

# Configure Streamlit page
st.set_page_config(
    page_title="AI Language Assistant",
    page_icon="🌐",
    layout="centered",
)

# Verify API key is present and not the placeholder
if not API_KEY or API_KEY.strip() == "" or API_KEY.strip() == "YOUR_API_KEY_HERE":
    st.error(
        "⚠️ **OpenAI API Key Missing!**\n\n"
        "Please add your OpenAI API key to the `.env` file:\n"
        "```text\n"
        "OPENAI_API_KEY=your_actual_api_key_here\n"
        "```\n"
        "Then restart or refresh the application."
    )
    st.info(
        "Need an API key? You can get one from the "
        "[OpenAI Developer Platform](https://platform.openai.com/api-keys)."
    )
    st.stop()

# Initialize OpenAI client securely (key is loaded from .env, never hardcoded)
try:
    client = OpenAI(api_key=API_KEY)
except Exception as init_err:
    st.error(f"Failed to initialize OpenAI client: {str(init_err)}")
    st.stop()

# Sidebar: Settings & Status
st.sidebar.title("⚙️ Assistant Settings")
st.sidebar.success("🔑 API Key detected from `.env`")

# Allow model selection or custom override in sidebar (defaults to MODEL_NAME)
available_models = ["gpt-5-mini", "gpt-4o-mini", "gpt-4o"]
default_idx = available_models.index(MODEL_NAME) if MODEL_NAME in available_models else 0
selected_model = st.sidebar.selectbox(
    "Active Model:",
    options=available_models,
    index=default_idx,
    help="Select the OpenAI model to use for inference.",
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "🌐 **Internet Connection Required**\n"
    "This version uses the cloud OpenAI API for inference.\n"
    "Your API key remains private on your machine."
)

# Main Application Interface
st.title("🌐 AI Language Assistant")
st.write("Translate, correct, rewrite, and simplify text using AI.")

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
    placeholder="Type or paste the text you want to process...",
)

# Process Button
if st.button("Process", type="primary", use_container_width=True):
    # Validation: Empty input check
    if not user_text or not user_text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            # Build the task prompt
            prompt = create_prompt(
                task=task,
                text=user_text,
                language=target_language,
                style=rewrite_style,
            )

            # Send prompt to OpenAI API with spinner
            with st.spinner("Processing with OpenAI API..."):
                start_time = time.perf_counter()

                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful, accurate, and concise AI language assistant. "
                                "Always follow the task instructions precisely and return only the requested output."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                )

                elapsed_seconds = round(time.perf_counter() - start_time, 2)
                output_text = response.choices[0].message.content.strip()

            # Display Output
            st.markdown("### Output:")
            st.info(output_text)
            st.caption(f"⏱️ Processing time: {elapsed_seconds} seconds | Model: `{selected_model}`")

        except ValueError as val_err:
            st.warning(str(val_err))
        except Exception as api_err:
            error_message = str(api_err)
            # Friendly error handling for common API issues
            if "Incorrect API key" in error_message or "invalid_api_key" in error_message:
                st.error("Authentication Error: The OpenAI API key in your `.env` file is invalid. Please check your key.")
            elif "rate_limit" in error_message.lower():
                st.error("Rate Limit Error: You have exceeded your OpenAI API rate limit or quota. Please check your account.")
            elif "model_not_found" in error_message.lower() or "does not exist" in error_message.lower():
                st.error(
                    f"Model Error: The model `{selected_model}` was not found or is not available on your account. "
                    "Please try selecting `gpt-4o-mini` from the sidebar."
                )
            elif "connection" in error_message.lower():
                st.error("Connection Error: Could not reach OpenAI servers. Please check your internet connection.")
            else:
                st.error(f"OpenAI API Error: {error_message}")

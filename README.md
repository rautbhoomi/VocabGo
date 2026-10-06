# 🌐 AI Language Assistant

An AI language assistant built with **Streamlit** and powered by the **OpenAI API**. It provides four language features: translation, grammar correction, text rewriting, and text simplification.

> **Note**: This application uses the cloud-based OpenAI API and **requires an active internet connection**. It does not run offline.

---

## 1. Overview

The **AI Language Assistant** allows you to perform advanced language processing tasks directly in a web interface. It securely connects to OpenAI's language models (such as `gpt-5-mini` or `gpt-4o-mini`) using your personal API key stored safely in a local `.env` file.

---

## 2. Features

- **A. Translation**: Translate text between **English**, **Hindi**, and **Marathi**.
- **B. Grammar Correction**: Corrects grammatical mistakes, spelling errors, punctuation, and sentence structure while preserving original meaning.
- **C. Text Rewriting**: Rewrites text in three styles: **Professional**, **Simple**, or **Friendly**.
- **D. Text Simplification**: Simplifies complex, academic, or technical text into easy-to-understand language.
- **Secure Key Handling**: Loads your OpenAI API key from a private `.env` file (never exposed in the UI or hardcoded).
- **Latency Tracking**: Measures and displays response generation time for each request.
- **Clean UI**: Simple, beginner-friendly Streamlit interface.

---

## 3. Architecture

```text
User
 ↓
Streamlit Frontend (app.py)
 ↓
Secure Environment Configuration (.env -> python-dotenv)
 ↓
Python OpenAI Client (openai Python SDK)
 ↓ (HTTPS Internet Connection)
OpenAI API Cloud Service (e.g., gpt-5-mini / gpt-4o-mini)
 ↓
Formatted response displayed with generation time
```

---

## 4. Requirements

- **Operating System**: Windows, Linux, or macOS
- **Python**: Version 3.11+
- **OpenAI API Key**: A valid API key from [OpenAI Developer Platform](https://platform.openai.com/api-keys)
- **Active Internet Connection**

---

## 5. Quick Installation & Setup

### Step 1: Clone or navigate to the project directory
```powershell
cd offline-language-assistant
```

### Step 2: (Optional) Set up a virtual environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure your OpenAI API key
Open the `.env` file in the root folder and replace the placeholder with your actual OpenAI API key:

```text
OPENAI_API_KEY=sk-proj-your_actual_api_key_here
```

> **Security Note**: Never commit your `.env` file or paste your actual key in public repositories. The `.gitignore` file is already set up to protect your `.env` file from Git commits.

---

## 6. Running the Application

To start the Streamlit web application:

```powershell
streamlit run app.py
```

Streamlit will launch automatically in your browser at `http://localhost:8501`.

---

## 7. Running Tests

Unit tests verify prompt formatting, task routing, and missing key validation without needing an internet connection:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

To run the automated benchmark across all task categories with your OpenAI key:

```powershell
python benchmark.py --model gpt-5-mini
```

---

## 8. Security and Privacy

- **No Hardcoded Keys**: The application never hardcodes API keys inside Python scripts.
- **Private `.env` File**: All keys are retrieved via `python-dotenv`.
- **UI Protection**: The API key is never rendered or revealed in the web browser interface.
- **Git Exclusions**: The `.gitignore` file excludes `.env`, `.env.*`, `.venv`, and cache files from Git tracking.

---

## 9. Project Structure

```text
offline-language-assistant/
│
├── app.py                      # Main Streamlit web application
├── benchmark.py                # Automated benchmark runner for OpenAI models
├── benchmark_dataset.json      # Structured test cases (Translation, Grammar, Rewrite, Simplify)
├── docs.md                     # Technical documentation & project overview
├── README.md                   # Project instructions and documentation
├── requirements.txt            # Minimal dependencies: streamlit, openai, python-dotenv
├── .env                        # Local configuration storing OPENAI_API_KEY (git-ignored)
├── .gitignore                  # Git exclusions for secrets, virtual environment, and cache
│
├── src/
│   ├── __init__.py
│   ├── model.py                # OpenAI client helper & execution timer
│   ├── prompts.py              # Prompt templates for the 4 language tasks
│   └── language_tasks.py       # Prompt generation and input validation
│
└── tests/
    ├── __init__.py
    ├── test_basic.py           # Unit tests
    └── test_live_model.py      # Live API integration test (auto-skips if key is unset)
```

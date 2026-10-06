# 🌐 Offline Language Assistant

An AI language assistant that runs **completely locally** on your computer. It performs translation, grammar correction, text rewriting, and text simplification without requiring any internet connection or cloud API subscriptions.

---

## 1. Overview

The **Offline Language Assistant** is designed for privacy, reliability, and offline usability. Unlike standard AI tools that rely on cloud servers (such as OpenAI, Gemini, Claude, or Google Translate), this assistant runs an open-weight language model directly on your laptop's hardware using [Ollama](https://ollama.com).

Once your preferred local model is downloaded, you can turn off Wi-Fi and continue using all features seamlessly.

---

## 2. Features

- **A. Translation**: Bidirectional translation between **English**, **Hindi**, and **Marathi**.
- **B. Grammar Correction**: Fixes grammatical errors, spelling typos, punctuation, and sentence structure while preserving original meaning.
- **C. Text Rewriting**: Rewrites input text into **Professional**, **Simple**, or **Friendly** styles.
- **D. Text Simplification**: Transforms dense, complicated sentences and technical jargon into plain, easy-to-understand language.
- **Local AI Inference**: Powered by local models running on Ollama.
- **100% Offline Capable**: Zero internet access required after setup.
- **Response-Time Measurement**: Tracks and displays inference latency for every request.
- **Beginner-Friendly UI**: Clean, intuitive interface built with Streamlit.

---

## 3. Architecture

```text
User
 ↓
Streamlit Frontend (app.py)
 ↓
Python Application Logic (src/language_tasks.py)
 ↓
Local Ollama API (http://127.0.0.1:11434)
 ↓
Local AI Model (e.g., llama3.2:1b)
 ↓
Response displayed with execution time
```

---

## 4. Requirements

- **Operating System**: Windows, Linux, or macOS
- **Python**: Version 3.11 or higher
- **Ollama**: Free local inference engine installed from [ollama.com](https://ollama.com)
- **RAM / Memory**: Sufficient system memory for your chosen local model (e.g., 4 GB to 8 GB+ RAM for 1B–3B parameter models)

---

## 5. Installation

Follow these step-by-step commands in your terminal:

### Step 1: Clone the repository
```powershell
git clone <repository-url>
cd offline-language-assistant
```

### Step 2: Create and activate a Python virtual environment
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

---

## 6. Setting Up the Local AI Model (Ollama)

Ollama runs the local AI model on your computer.

1. Download and install Ollama from [https://ollama.com](https://ollama.com).
2. Download a lightweight model of your choice by running this command in your terminal:
   ```powershell
   ollama run llama3.2:1b
   ```
   *Alternative lightweight models:*
   - `ollama run qwen2.5:1.5b` (Great for Hindi & Marathi)
   - `ollama run llama3.2:3b` (Higher quality, ~2 GB)

*Note: Once the command finishes downloading, you can press `Ctrl + D` or type `/bye` to exit the chat prompt. The model remains installed on your computer.*

---

## 7. Running the Application

Ensure your virtual environment is active and run:

```powershell
streamlit run app.py
```

Your default web browser will automatically open the application at `http://localhost:8501`.

---

## 8. Offline Test (Verification)

To verify that the application works without an internet connection:

1. Start Ollama and download your selected local model (`ollama run llama3.2:1b`).
2. Start the Streamlit application: `streamlit run app.py`.
3. **Turn off your laptop's Wi-Fi / disconnect Ethernet**.
4. Test any feature:
   - Select **Translate**, choose **Hindi**, enter `Hello, welcome to our office.`, and click **Process**.
   - Select **Grammar Correction**, enter `She do not knows the answer.`, and click **Process**.
5. Confirm that the application responds with the result and displays the processing time, proving full offline functionality.

---

## 9. Running Tests

Unit tests do not require an active model or internet connection:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

To run the automated benchmark across all competition task categories:

```powershell
python benchmark.py --model llama3.2:1b
```

---

## 10. Security and Privacy

- **Local Data Processing**: All user text is processed locally on your computer.
- **Zero Cloud APIs**: No data is ever transmitted to OpenAI, Gemini, Claude, or any external third-party server.
- **Privacy Assurance**: Your queries and documents stay strictly on your local machine.
- **Repository Safety**: Model weight files (`.gguf`, binary weights) and environment files are ignored by Git and never committed to GitHub.

---

## 11. Project Structure

```text
offline-language-assistant/
│
├── app.py                      # Main Streamlit frontend
├── benchmark.py                # Benchmark runner for local models
├── benchmark_dataset.json      # Evaluation dataset (Translation, Grammar, Rewrite, Simplify)
├── docs.md                     # Competition evaluation & resource trade-off documentation
├── README.md                   # Project documentation and guide
├── requirements.txt            # Minimal Python dependencies
├── .gitignore                  # Git exclusions for models, cache, and venv
│
├── src/
│   ├── __init__.py
│   ├── model.py                # Local Ollama communication and error handling
│   ├── prompts.py              # Prompt templates for all 4 language tasks
│   └── language_tasks.py       # Task routing and prompt construction
│
└── tests/
    ├── __init__.py
    ├── test_basic.py           # Offline unit tests
    └── test_live_model.py      # Live model integration test (skips if offline)
```

---

## 12. Suggested Initial Git Commit

```powershell
git add .
git commit -m "Initial project setup"
```

# AI Language Assistant — Technical Documentation

This document describes the design, architecture, security model, and evaluation setup for the **AI Language Assistant** using the **OpenAI API**.

---

## 1. Architecture Overview

The system uses a clean client-server architecture where a local Streamlit interface interacts with OpenAI's cloud models over HTTPS.

```text
+-----------------------------------------------------------+
|                      User's Machine                       |
|                                                           |
|  [ User ]                                                 |
|     |                                                     |
|     v                                                     |
|  [ Streamlit UI (app.py) ]                                |
|     |                                                     |
|     v                                                     |
|  [ Language Tasks (src/language_tasks.py) ]               |
|     |                                                     |
|     v                                                     |
|  [ OpenAI Client (src/model.py / openai SDK) ]            |
|     | (Loads OPENAI_API_KEY from .env securely)           |
+-----|-----------------------------------------------------+
      |
      | HTTPS Encrypted Traffic (Internet connection required)
      v
+-----------------------------------------------------------+
|                    OpenAI Cloud Service                   |
|                                                           |
|  [ Model: gpt-5-mini / gpt-4o-mini / gpt-4o ]             |
|     |                                                     |
|     +---> Returns structured completion to app.py         |
+-----------------------------------------------------------+
```

---

## 2. Supported Features & Tasks

1. **Translation**:
   - Supports translation between **English**, **Hindi**, and **Marathi**.
   - Preserves original tone, sentiment, and vocabulary nuances.
2. **Correct Grammar**:
   - Detects and repairs subject-verb disagreements, misspelled words, incorrect punctuation, and awkward phrasing.
3. **Rewrite**:
   - Provides three tone variations:
     - **Professional**: Business-appropriate, clear, and courteous.
     - **Simple**: Plain language, accessible to general readers.
     - **Friendly**: Warm, conversational, and approachable.
4. **Simplify**:
   - Unpacks complex sentences and dense academic or technical jargon into direct, easily readable language.

---

## 3. Security and API Key Best Practices

- **Zero Hardcoded Secrets**: The API key is never written directly inside any source code file (`app.py`, `model.py`, etc.).
- **Local `.env` Storage**: Keys are read dynamically at runtime using `python-dotenv`.
- **UI Masking & Protection**: The application never displays the secret key in UI widgets, error messages, or logs.
- **Git Exclusions**: `.env` and `.env.*` are included in `.gitignore` to prevent leaking keys to version control systems like GitHub.
- **Fail-Safe Startup**: If `OPENAI_API_KEY` is missing or contains the placeholder `YOUR_API_KEY_HERE`, the app immediately displays a clean warning and stops before making any network calls.

---

## 4. Benchmark Dataset & Evaluation

The included `benchmark_dataset.json` contains representative test cases for all four tasks:
- **Translation**: Multi-directional tests (English <-> Hindi, English <-> Marathi).
- **Correct Grammar**: Grammatical, spelling, and punctuation errors.
- **Rewrite**: Informal, professional, and short text style conversions.
- **Simplify**: Complex academic sentences, technical explanations, and multi-sentence paragraphs.

### Running Benchmarks
To run the automated benchmark with your API key:
```powershell
python benchmark.py --model gpt-5-mini --output benchmark_results.json
```

# Offline Language Assistant — Technical Documentation & Evaluation Guide

This document outlines the architecture, evaluation criteria, benchmarking methodology, resource trade-off experiments, and privacy specifications for the **Offline Language Assistant**.

---

## 1. Project Overview & Architecture

The **Offline Language Assistant** is designed to provide complete natural language processing capabilities on a standard consumer laptop without requiring an active internet connection.

### System Architecture Flow

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
|  [ Language Tasks & Prompts (src/language_tasks.py) ]     |
|     |                                                     |
|     v                                                     |
|  [ Local Model Client (src/model.py) ]                    |
|     | (Local HTTP on 127.0.0.1:11434)                     |
|     v                                                     |
|  [ Local Ollama Inference Engine ]                        |
|     |                                                     |
|     v                                                     |
|  [ Local Open-Weight Model (e.g. llama3.2:1b) ]           |
|     |                                                     |
|     v                                                     |
|  [ Response & Timing returned to UI ]                     |
+-----------------------------------------------------------+
```

### Key Design Tenets
1. **Zero External API Calls**: The codebase has no integrations with OpenAI, Gemini, Claude, DeepL, Google Translate, or any cloud LLM endpoints.
2. **Local Loopback Only**: The only network communication is to `http://127.0.0.1:11434` (Ollama's local service).
3. **Graceful Fault Tolerance**: If the local model is offline or uninstalled, the user receives an actionable error message rather than a raw Python crash or stack trace.
4. **Lightweight & Beginner-Friendly**: Minimal dependencies (`streamlit` and `requests`), clean modular code, no complex framework abstractions (no LangChain, no LlamaIndex).

---

## 2. Competition Evaluation Criteria

For intermediate-level competition evaluation, the system is assessed across eight key dimensions:

1. **Usefulness**: Does the system effectively assist users with day-to-day writing and translation tasks?
2. **Response Quality**: Are grammar corrections accurate? Are translations faithful to the original tone? Does rewriting respect the requested style?
3. **Response Speed**: Does the local model deliver responses in reasonable time on consumer CPU/GPU hardware?
4. **Model Size**: How much disk space is consumed by the local model weights?
5. **RAM / Memory Usage**: Can the model run within standard laptop memory constraints (e.g., 8 GB or 16 GB unified RAM)?
6. **Hardware Requirements**: Can the system run on a CPU-only laptop without requiring an expensive dedicated discrete GPU?
7. **Offline Functionality**: Does the entire workflow function seamlessly with Wi-Fi/Ethernet disabled?
8. **Resource vs. Usefulness Trade-off**: What is the minimum model size that maintains acceptable quality?

---

## 3. Benchmark Dataset

A structured benchmark dataset is provided in `benchmark_dataset.json` covering four core language tasks:

### A. Translation
Evaluates bidirectional translations across three supported languages:
* **English -> Hindi**: Everyday informational facts.
* **English -> Marathi**: Conversational and customer service sentences.
* **Hindi -> English**: Declarative project explanations.
* **Marathi -> English**: Informational and security-oriented statements.

### B. Grammar Correction
Evaluates error detection and correction without altering semantic meaning:
* **Grammatical mistakes**: Subject-verb agreement, irregular verb forms, tense mismatches.
* **Spelling mistakes**: Misspelled technical and conversational terms.
* **Punctuation mistakes**: Run-on sentences, missing apostrophes, missing capitalization and period termination.

### C. Text Rewriting
Evaluates style transfer while preserving core information:
* **Informal text -> Professional style**: Transforming casual chat into formal business communication.
* **Professional text -> Friendly style**: Softening legalistic or bureaucratic wording into warm interpersonal prose.
* **Short message -> Simple style**: Clarifying dense or ornate notices into direct announcements.

### D. Text Simplification
Evaluates reduction of syntactic and lexical complexity:
* **Complicated sentences**: Sentences laden with archaic or overly complex vocabulary.
* **Technical explanations**: AI and computing jargon translated for non-specialists.
* **Long paragraphs**: Multi-clause academic paragraphs condensed into clear, digestible statements.

---

## 4. Running Benchmarks & Measuring Performance

### Running the Benchmark Suite
To execute the automated evaluation against your local Ollama model:

```powershell
python benchmark.py --model llama3.2:1b --output benchmark_results_llama1b.json
```

To test a different model (e.g., `qwen2.5:1.5b` or `llama3.2:3b`):

```powershell
python benchmark.py --model qwen2.5:1.5b --output benchmark_results_qwen1.5b.json
```

### How to Measure System Metrics

#### 1. Measuring Response Time
- **In UI**: Displayed automatically under each generated result (`Processing time: X.XX seconds`).
- **In Benchmark Script**: Measured per prompt using Python's high-resolution `time.perf_counter()`.

#### 2. Measuring Model Size on Disk
In PowerShell, check the downloaded model size via Ollama:
```powershell
ollama list
```
This shows the exact disk footprint of each downloaded model.

#### 3. Measuring RAM / Memory Usage
To measure RAM usage while Ollama is actively processing:
* **Windows (PowerShell)**:
  ```powershell
  Get-Process -Name ollama* | Select-Object ProcessName, Id, @{Name="WorkingSet_MB"; Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}}
  ```
* **Windows (Task Manager)**: Open Task Manager -> Look for `ollama.exe` or `ollama_llama_server.exe` under Background processes during inference.
* **Linux / macOS**:
  ```bash
  ps aux | grep ollama
  ```

---

## 5. Resource Trade-off Experiment

### Objective
The goal is to identify the **sweet spot**: the smallest model that delivers acceptable response quality while maintaining fast response speeds and low memory consumption on a standard laptop.

As model size decreases (e.g., from 3B parameters to 1B or 0.5B), memory and latency decrease, but translation accuracy for low-resource languages (like Marathi or Hindi) or complex grammar correction may degrade.

### Comparison Table

> **Note**: As per evaluation integrity guidelines, values below are templates and must be recorded from actual testing on the target hardware. Values are left blank until testing is conducted.

| Model | Download Size | RAM Usage | Avg Response Time | Output Quality | Useful for Tasks? | Recommended Hardware |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `qwen2.5:0.5b` | ~398 MB | [Test on hardware] | [Test on hardware] | [Evaluate outputs] | [Yes / Partial / No] | Low-end CPU (4 GB RAM) |
| `llama3.2:1b` | ~1.3 GB | [Test on hardware] | [Test on hardware] | [Evaluate outputs] | [Yes / Partial / No] | Standard CPU (8 GB RAM) |
| `qwen2.5:1.5b` | ~1.0 GB | [Test on hardware] | [Test on hardware] | [Evaluate outputs] | [Yes / Partial / No] | Standard CPU (8 GB RAM) |
| `llama3.2:3b` | ~2.0 GB | [Test on hardware] | [Test on hardware] | [Evaluate outputs] | [Yes / Partial / No] | Mid-tier CPU / GPU (8-16 GB RAM) |

### Recommended Models for Comparison
1. **`llama3.2:1b`** (Meta): Highly optimized for fast CPU inference, small disk footprint, very strong English performance.
2. **`qwen2.5:1.5b`** (Alibaba Cloud): Strong multilingual capabilities with native training on Indic scripts (Hindi, Marathi).
3. **`llama3.2:3b`** (Meta): Higher parameter capacity for complex grammar and nuanced rewriting.

---

## 6. Offline Testing Verification Protocol

To verify complete offline operation for competition evaluation:

1. **Preparation**: Download the desired local model while connected to the internet:
   ```powershell
   ollama run llama3.2:1b
   ```
2. **Launch Application**:
   ```powershell
   streamlit run app.py
   ```
3. **Disconnect Network**: Turn off Wi-Fi and disconnect all Ethernet cables on your laptop.
4. **Execute All 4 Tasks**:
   - Run a Translation (e.g. English to Hindi).
   - Run a Grammar Correction.
   - Run a Text Rewriting task.
   - Run a Text Simplification task.
5. **Verify**:
   - Confirm outputs are generated without connection errors.
   - Confirm processing time is displayed.
   - Check packet monitor / Task Manager to confirm 0 bytes of external network traffic.

---

## 7. Security and Privacy Specification

- **100% Local Execution**: All input text is sent strictly to `http://127.0.0.1:11434`. No user data leaves the machine.
- **No Cloud Inference APIs**: No API keys, tokens, or external accounts are required or supported.
- **No Telemetry Egress**: The application does not collect, log, or transmit user activity to any external server.
- **Repository Safety**: Model weights (GGUF, bin, safetensors) and virtual environments are excluded via `.gitignore` to prevent committing proprietary or large binary files to version control.

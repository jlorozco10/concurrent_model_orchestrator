# Concurrent Model Orchestrator

A small `asyncio` demo that fans a batch of prompts out to several simulated LLM backends (GPT-4, Claude 3, a local Llama) concurrently, with bounded concurrency and per-call timeouts.

No real API calls are made. Each "model" sleeps for a random 0.5–3.0 s to simulate latency.

## How it works

- **Model stubs**: `gpt_4_call`, `claude_3_call` and `local_llama_call` each take a prompt and a shared `asyncio.Semaphore`, and return a result dict.
- **Concurrency limit**: `models_call_batch` creates `asyncio.Semaphore(2)`, so at most 2 calls run at once.
- **Timeout**: each call is wrapped in `asyncio.timeout(2.0)`. A call that takes longer returns `{"ok": False, "error": "Timeout for <model>"}`. The timeout only starts once the call has acquired the semaphore, so time spent waiting in the queue does not count.
- **Routing**: each prompt is assigned to a random model with `random.choice`.
- **Gathering**: `asyncio.gather(..., return_exceptions=True)` runs everything and keeps going if a task raises.
- **Reporting**: `main` sends 10 prompts (`document_0` … `document_9`), then prints the number of successes, total elapsed time, and each failure.

### Result shape

```python
{"text": "document_3", "result": "Yes", "ok": True}
{"text": "document_5", "ok": False, "error": "Timeout for Llama"}
```

## Requirements

- Python 3.11+ (uses `asyncio.timeout`)
- No third-party dependencies

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python concurrent_model_orchestrator.py
```

Example output:

```
GPT-4 started: document_0
Llama started: document_1
...
Processed OK: 6/10 in 6.42s
Fail: document_4 -> Timeout for Claude 3
```

Results vary between runs because both latency and model choice are random.

## Customizing

| What | Where |
|------|-------|
| Max concurrent calls | `asyncio.Semaphore(2)` in `models_call_batch` |
| Per-call timeout | `asyncio.timeout(2.0)` in each model function |
| Simulated latency | `random.uniform(0.5, 3.0)` in each model function |
| Batch size | `range(10)` in `main` |
| Add a model | Write a new `async def` with the same signature and add it to `models_call_functions` |

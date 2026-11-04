import asyncio
import random
import time

async def gpt_4_call(prompt: str, sem: asyncio.Semaphore):
    async with sem:
        try:
            async with asyncio.timeout(2.0):
                print(f"GPT-4 started: {prompt}")
                latency = random.uniform(0.5, 3.0)
                await asyncio.sleep(latency)
                return {"text": prompt, "result": len(prompt), "ok": True}

        except TimeoutError:
            return {"text": prompt, "ok": False, "error": "Timeout for GPT-4"}

async def claude_3_call(prompt: str, sem: asyncio.Semaphore):
    async with sem:
        try:
            async with asyncio.timeout(2.0):
                print(f"Claude 3 started: {prompt}")
                latency = random.uniform(0.5, 3.0)
                await asyncio.sleep(latency)
                return {"text": prompt, "result": "Yes", "ok": True}

        except TimeoutError:
            return {"text": prompt, "ok": False, "error": "Timeout for Claude 3"}

async def local_llama_call(prompt: str, sem: asyncio.Semaphore):
    async with sem:
        try:
            async with asyncio.timeout(2.0):
                print(f"Llama started: {prompt}")
                latency = random.uniform(0.5, 3.0)
                await asyncio.sleep(latency)
                return {"text": prompt, "result": "No", "ok": True}

        except TimeoutError:
            return {"text": prompt, "ok": False, "error": "Timeout for Llama"}


async def models_call_batch(texts: list[str]):
    models_call_functions = [gpt_4_call, claude_3_call, local_llama_call]
    sem = asyncio.Semaphore(2)
    tasks = []
    for t in texts:
        selected_model = random.choice(models_call_functions)
        tasks.append(selected_model(t,sem))
    return await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    texts = [f"document_{i}" for i in range(10)]
    start_time = time.perf_counter()
    results = await models_call_batch(texts)
    elapsed_time = time.perf_counter() - start_time

    ok = [r for r in results if isinstance(r, dict) and r.get("ok")]
    failed = [r for r in results if isinstance(r, dict) and not r.get("ok")]

    print(f"Processed OK: {len(ok)}/{len(texts)} in {elapsed_time}s")
    for f in failed:
        print(f"Fail: {f['text']} -> {f['error']}")

    pass

if __name__ == "__main__":
    asyncio.run(main())
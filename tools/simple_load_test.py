import asyncio
import httpx
import time
import statistics

# Simple asyncio-based load tester for POST /api/calculate-tax
# Edit HOST and API_KEY as needed.
HOST = "http://localhost:8000"
API_KEY = "MYXfWcOW5vBi86n1TaiL569bUIJt7MXA"
CONCURRENCY = 5  # number of concurrent tasks
REQUESTS_PER_WORKER = 20  # how many requests each concurrent worker will do

payload_template = {
    "registration": "01/2020",
    "power": 10,
    # use int emission to match the Pydantic model
    "emission": 120,
    # must be one of the model's energy keys (e.g. "ES", "EL", "GO", ...)
    "energy": "ES",
    "weight": 1500,
    "region": 75,
    "price": 20000.0
}

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

async def worker(client: httpx.AsyncClient, id: int, results: list):
    for i in range(REQUESTS_PER_WORKER):
        start = time.monotonic()
        try:
            r = await client.post("/api/calculate-tax", json=payload_template, headers=headers, timeout=30.0)
            latency = time.monotonic() - start
            # capture response status and body for easier debugging
            text = None
            try:
                text = r.text
            except Exception:
                text = "<no body>"
            results.append((r.status_code, latency, text))
        except Exception as e:
            latency = time.monotonic() - start
            results.append((None, latency, str(e)))

async def main():
    results = []
    async with httpx.AsyncClient(base_url=HOST) as client:
        tasks = [asyncio.create_task(worker(client, i, results)) for i in range(CONCURRENCY)]
        await asyncio.gather(*tasks)

    status_ok = [lat for (s, lat, _) in results if s == 200]
    status_err = [s for (s, _, _) in results if s != 200]
    latencies = [lat for (_, lat, _) in results]
    # collect up to 10 distinct error samples
    error_samples = []
    for (s, lat, body) in results:
        if s != 200:
            error_samples.append((s, body))
            if len(error_samples) >= 10:
                break

    print(f"Total requests: {len(results)}")
    print(f"Successes (200): {len(status_ok)}")
    print(f"Errors/non-200: {len(status_err)}")
    if latencies:
        print(f"Median latency: {statistics.median(latencies):.3f}s")
        print(f"P95 latency: {statistics.quantiles(latencies, n=100)[94]:.3f}s")
        print(f"Mean latency: {statistics.mean(latencies):.3f}s")
    if error_samples:
        print('\nSample errors (status, body):')
        for s, body in error_samples:
            print(f"- {s}: {body[:400]}")

if __name__ == '__main__':
    asyncio.run(main())

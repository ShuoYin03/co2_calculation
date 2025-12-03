import asyncio
import httpx
import time
import statistics
import os
import sys

# Simple asyncio-based load tester for POST /api/calculate-tax
# 可通过环境变量或命令行参数配置

HOST = os.getenv("TEST_HOST", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "MYXfWcOW5vBi86n1TaiL569bUIJt7MXA")
CONCURRENCY = int(os.getenv("TEST_CONCURRENCY", "10"))  # 并发数
REQUESTS_PER_WORKER = int(os.getenv("TEST_REQUESTS", "20"))

# 命令行参数支持 (覆盖环境变量)
if len(sys.argv) > 1:
    CONCURRENCY = int(sys.argv[1])
if len(sys.argv) > 2:
    REQUESTS_PER_WORKER = int(sys.argv[2])

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
    print("=" * 60)
    print("🧪 并发负载测试")
    print("=" * 60)
    print(f"目标服务器: {HOST}")
    print(f"并发数: {CONCURRENCY}")
    print(f"每个worker请求数: {REQUESTS_PER_WORKER}")
    print(f"总请求数: {CONCURRENCY * REQUESTS_PER_WORKER}")
    print("=" * 60)
    print("")

    results = []
    start_time = time.monotonic()
    async with httpx.AsyncClient(base_url=HOST) as client:
        tasks = [asyncio.create_task(worker(client, i, results)) for i in range(CONCURRENCY)]
        await asyncio.gather(*tasks)

    total_time = time.monotonic() - start_time

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

    print("\n📊 测试结果:")
    print("-" * 60)
    print(f"总请求数: {len(results)}")
    print(f"成功 (200): {len(status_ok)} ({len(status_ok)/len(results)*100:.1f}%)")
    print(f"失败/非200: {len(status_err)} ({len(status_err)/len(results)*100:.1f}%)")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"吞吐量 (RPS): {len(results)/total_time:.2f} 请求/秒")

    if latencies:
        print("\n⏱️  响应时间统计:")
        print("-" * 60)
        print(f"平均响应时间: {statistics.mean(latencies):.3f}秒")
        print(f"中位数响应时间: {statistics.median(latencies):.3f}秒")
        print(f"最小响应时间: {min(latencies):.3f}秒")
        print(f"最大响应时间: {max(latencies):.3f}秒")
        if len(latencies) >= 100:
            print(f"P95响应时间: {statistics.quantiles(latencies, n=100)[94]:.3f}秒")

    if error_samples:
        print('\n❌ 错误样本 (status, body):')
        print("-" * 60)
        for s, body in error_samples:
            print(f"状态码 {s}: {body[:200]}...")

    print("\n" + "=" * 60)
    if len(status_err) == 0:
        print("✅ 测试通过! 所有请求成功")
    elif len(status_err) / len(results) < 0.05:
        print("⚠️  测试基本通过, 但有少量失败")
    else:
        print("❌ 测试失败, 错误率过高")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())

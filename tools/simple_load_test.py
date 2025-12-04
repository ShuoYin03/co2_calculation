import asyncio
import httpx
import time
import statistics
import os
import sys
import dotenv
dotenv.load_dotenv()
# Simple asyncio-based load tester for POST /api/calculate-tax
# 针对 2GB RAM + 1 CPU Render 实例优化

HOST = os.getenv("TEST_HOST", "https://co2-calculation-9ciy.onrender.com")
# HOST = os.getenv("TEST_HOST", "http://localhost:8000")  # 本地测试时使用
API_KEY = os.getenv("API_KEY", "")  # 必须设置你的真实API_KEY
CONCURRENCY = int(os.getenv("TEST_CONCURRENCY", "3"))  # 保守模式: 1个并发
REQUESTS_PER_WORKER = int(os.getenv("TEST_REQUESTS", "10"))  # 减少请求数
REQUEST_DELAY = float(os.getenv("TEST_DELAY", "0"))  # 请求间隔2秒

# 命令行参数支持: python simple_load_test.py [concurrency] [requests] [delay]
if len(sys.argv) > 1:
    CONCURRENCY = int(sys.argv[1])
if len(sys.argv) > 2:
    REQUESTS_PER_WORKER = int(sys.argv[2])
if len(sys.argv) > 3:
    REQUEST_DELAY = float(sys.argv[3])

payload_template = {
    "registration": "01/2020",
    "power": 100,
    "emission": 120,
    "energy": "ES",  # 1 = Essence (汽油)
    "weight": 1500,
    "region": "75",  # 75 = Paris
    "price": 25000.0
}

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

async def worker(client: httpx.AsyncClient, id: int, results: list):
    for i in range(REQUESTS_PER_WORKER):
        # 在请求前添加延迟,避免服务器过载和限流
        if i > 0 or id > 0:  # 第一个worker的第一个请求不延迟
            await asyncio.sleep(REQUEST_DELAY)

        start = time.monotonic()
        try:
            r = await client.post("/api/calculate-tax", json=payload_template, headers=headers, timeout=120.0)
            latency = time.monotonic() - start
            text = None
            try:
                text = r.text
            except Exception:
                text = "<no body>"
            results.append((r.status_code, latency, text))
            print(f"Worker {id} - 请求 {i+1}/{REQUESTS_PER_WORKER}: {r.status_code} ({latency:.2f}s)")
        except Exception as e:
            latency = time.monotonic() - start
            results.append((None, latency, str(e)))
            print(f"Worker {id} - 请求 {i+1}/{REQUESTS_PER_WORKER}: ERROR ({latency:.2f}s) - {str(e)[:100]}")

async def main():
    if not API_KEY:
        print("❌ 错误: 必须设置 API_KEY 环境变量!")
        print("使用方法: set API_KEY=your_key && python simple_load_test.py")
        sys.exit(1)

    print("=" * 60)
    print("🧪 Render 部署 - 负载测试 (2GB RAM + 1 CPU)")
    print("=" * 60)
    print(f"目标服务器: {HOST}")
    print(f"并发数: {CONCURRENCY}")
    print(f"每个worker请求数: {REQUESTS_PER_WORKER}")
    print(f"请求间隔: {REQUEST_DELAY}秒")
    print(f"总请求数: {CONCURRENCY * REQUESTS_PER_WORKER}")
    print(f"预计耗时: ~{CONCURRENCY * REQUESTS_PER_WORKER * REQUEST_DELAY / CONCURRENCY:.0f}秒")
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

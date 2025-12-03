import uvicorn
from config import WORKERS, HOST, PORT, LOG_LEVEL
import platform

if __name__ == "__main__":
    # Windows不支持Playwright多worker,强制使用单worker
    workers = WORKERS
    if platform.system() == "Windows" and WORKERS > 1:
        print(f"⚠️  警告: Windows平台不支持多worker模式 (Playwright限制)")
        print(f"⚠️  将WORKERS从 {WORKERS} 降为 1")
        print(f"💡 提示: 在Windows上请调整MAX_CONCURRENT_BROWSERS来提升并发能力")
        print("")
        workers = 1

    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        workers=workers,
        log_level=LOG_LEVEL,
        reload=False
    )
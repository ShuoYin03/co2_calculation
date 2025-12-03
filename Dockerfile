FROM mcr.microsoft.com/playwright/python:v1.54.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

COPY . .

EXPOSE 8000

# 环境变量默认值 (可在运行时覆盖)
ENV MAX_CONCURRENT_BROWSERS=1
ENV WORKERS=1
ENV LOG_LEVEL=info

CMD ["python", "run.py"]
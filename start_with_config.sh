#!/bin/bash

# 快速启动脚本 - 可轻松切换不同配置

echo "选择运行配置:"
echo "1) 本地开发 (10并发, 4 workers)"
echo "2) 生产环境 - 小型 (3并发, 1 worker)"
echo "3) 生产环境 - 中型 (5并发, 2 workers)"
echo "4) 生产环境 - 大型 (10并发, 4 workers)"
echo "5) 自定义配置"

read -p "请输入选项 (1-5): " choice

case $choice in
  1)
    echo "🚀 启动本地开发配置..."
    export MAX_CONCURRENT_BROWSERS=10
    export WORKERS=4
    export LOG_LEVEL=debug
    ;;
  2)
    echo "🚀 启动小型生产配置..."
    export MAX_CONCURRENT_BROWSERS=3
    export WORKERS=1
    export LOG_LEVEL=warning
    ;;
  3)
    echo "🚀 启动中型生产配置..."
    export MAX_CONCURRENT_BROWSERS=5
    export WORKERS=2
    export LOG_LEVEL=info
    ;;
  4)
    echo "🚀 启动大型生产配置..."
    export MAX_CONCURRENT_BROWSERS=10
    export WORKERS=4
    export LOG_LEVEL=info
    ;;
  5)
    read -p "并发浏览器数 (MAX_CONCURRENT_BROWSERS): " browsers
    read -p "Worker数量 (WORKERS): " workers
    read -p "日志级别 (debug/info/warning/error): " loglevel
    export MAX_CONCURRENT_BROWSERS=$browsers
    export WORKERS=$workers
    export LOG_LEVEL=$loglevel
    ;;
  *)
    echo "❌ 无效选项"
    exit 1
    ;;
esac

echo ""
echo "📋 当前配置:"
echo "   MAX_CONCURRENT_BROWSERS: $MAX_CONCURRENT_BROWSERS"
echo "   WORKERS: $WORKERS"
echo "   LOG_LEVEL: $LOG_LEVEL"
echo "   预期最大并发: $((MAX_CONCURRENT_BROWSERS * WORKERS)) 个请求"
echo ""

python run.py

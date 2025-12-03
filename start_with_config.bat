@echo off
chcp 65001 >nul
echo 选择运行配置:
echo 1) 本地开发 (10并发, 4 workers)
echo 2) 生产环境 - 小型 (3并发, 1 worker)
echo 3) 生产环境 - 中型 (5并发, 2 workers)
echo 4) 生产环境 - 大型 (10并发, 4 workers)
echo 5) 自定义配置
echo.

set /p choice=请输入选项 (1-5):

if "%choice%"=="1" goto config1
if "%choice%"=="2" goto config2
if "%choice%"=="3" goto config3
if "%choice%"=="4" goto config4
if "%choice%"=="5" goto config5
goto invalid

:config1
echo 启动本地开发配置 (保守模式 - 避免限流)...
set MAX_CONCURRENT_BROWSERS=4
set WORKERS=1
set MIN_REQUEST_DELAY=1.0
set MAX_REQUEST_DELAY=3.0
set LOG_LEVEL=debug
echo (4并发, 1-3秒延迟)
goto run

:config2
echo 启动小型生产配置 (极保守 - Render Free)...
set MAX_CONCURRENT_BROWSERS=1
set WORKERS=1
set MIN_REQUEST_DELAY=2.0
set MAX_REQUEST_DELAY=4.0
set LOG_LEVEL=warning
echo (1并发, 2-4秒延迟)
goto run

:config3
echo 启动中型生产配置 (推荐)...
set MAX_CONCURRENT_BROWSERS=2
set WORKERS=1
set MIN_REQUEST_DELAY=0.5
set MAX_REQUEST_DELAY=2.0
set LOG_LEVEL=info
echo (2并发, 0.5-2秒延迟)
goto run

:config4
echo 启动大型生产配置 (激进 - 可能被限流)...
set MAX_CONCURRENT_BROWSERS=3
set WORKERS=1
set MIN_REQUEST_DELAY=0.5
set MAX_REQUEST_DELAY=1.5
set LOG_LEVEL=info
echo 警告: 此配置可能触发限流!
goto run

:config5
set /p MAX_CONCURRENT_BROWSERS=并发浏览器数 (MAX_CONCURRENT_BROWSERS):
set /p WORKERS=Worker数量 (WORKERS):
set /p LOG_LEVEL=日志级别 (debug/info/warning/error):
goto run

:invalid
echo 无效选项
pause
exit /b 1

:run
echo.
echo 当前配置:
echo    MAX_CONCURRENT_BROWSERS: %MAX_CONCURRENT_BROWSERS%
echo    WORKERS: %WORKERS%
echo    LOG_LEVEL: %LOG_LEVEL%
set /a max_concurrent=%MAX_CONCURRENT_BROWSERS% * %WORKERS%
echo    预期最大并发: %max_concurrent% 个请求
echo.

python run.py

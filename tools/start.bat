@chcp 65001 >nul
@echo off
:loop
set /p args=<C:\Users\Zebaro\AppData\Roaming\HotSpot\StreamDock\plugins\dev.zebaro.testVersion.sdPlugin\plugin\arguments.txt
.\.venv\Scripts\python.exe .\main.py %args%
echo Перезапуск через 2 секунды...
timeout /t 2 /nobreak >nul
goto loop
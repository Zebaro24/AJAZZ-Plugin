@echo off

set /p args=<C:\Users\Zebaro\AppData\Roaming\HotSpot\StreamDock\plugins\dev.zebaro.testVersion.sdPlugin\plugin\arguments.txt
.\.venv\Scripts\python.exe .\main.py %args%
@echo off

set "config_file=config.txt"
set "debug_value="

REM Проверяем наличие строки с debug= в файле config.txt
for /f "tokens=2 delims==" %%A in ('findstr /b "debug=" "%config_file%"') do set "debug_value=%%A"

REM Если debug=1, выполняем одну команду
if "%debug_value%"=="1" (
    echo %* > arguments.txt
) else (
    cd /d D:\Python\AJAZZ-Plugin\
    .\.venv\Scripts\python.exe .\main.py %*
)

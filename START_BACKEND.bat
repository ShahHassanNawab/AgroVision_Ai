@echo off
setlocal EnableExtensions EnableDelayedExpansion
title AgroVision AI - Backend Server
chcp 65001 >nul

rem ====================================================================
rem   AgroVision AI / NovaMind - Backend Startup Script
rem ====================================================================

rem 1. Switch to project root directory
cd /d "%~dp0"

echo ======================================================================
echo   AgroVision AI - Crop Disease Detection Platform
echo   Backend Service Launcher (FastAPI + Uvicorn + MobileNetV2)
echo ======================================================================
echo.

rem 2. Read configuration from .env if present
set "BACKEND_HOST=127.0.0.1"
set "BACKEND_PORT=8000"

if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        set "KEY=%%A"
        set "VAL=%%B"
        for /f "tokens=* delims= " %%K in ("!KEY!") do set "KEY=%%K"
        for /f "tokens=* delims= " %%V in ("!VAL!") do set "VAL=%%V"
        if /i "!KEY!"=="HOST" set "BACKEND_HOST=!VAL!"
        if /i "!KEY!"=="PORT" set "BACKEND_PORT=!VAL!"
    )
) else (
    if exist ".env.example" (
        echo [INFO] Initializing .env from .env.example...
        copy /y ".env.example" ".env" >nul
    )
)

echo [Config] Host: %BACKEND_HOST%  ^|  Port: %BACKEND_PORT%

rem 3. Detect Python Environment
set "PYTHON_CMD="
set "ENV_TYPE="

if exist "%~dp0.venv\Scripts\activate.bat" (
    set "PYTHON_CMD=%~dp0.venv\Scripts\python.exe"
    set "ENV_TYPE=Virtual Environment [.venv]"
    call "%~dp0.venv\Scripts\activate.bat"
) else if exist "%~dp0venv\Scripts\activate.bat" (
    set "PYTHON_CMD=%~dp0venv\Scripts\python.exe"
    set "ENV_TYPE=Virtual Environment [venv]"
    call "%~dp0venv\Scripts\activate.bat"
) else if exist "%~dp0env\Scripts\activate.bat" (
    set "PYTHON_CMD=%~dp0env\Scripts\python.exe"
    set "ENV_TYPE=Virtual Environment [env]"
    call "%~dp0env\Scripts\activate.bat"
) else (
    where python >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=python"
        set "ENV_TYPE=Installed Python [System PATH]"
    ) else (
        where py >nul 2>&1
        if not errorlevel 1 (
            set "PYTHON_CMD=py -3"
            set "ENV_TYPE=Python Launcher [py -3]"
        ) else if exist "C:\Python314\python.exe" (
            set "PYTHON_CMD=C:\Python314\python.exe"
            set "ENV_TYPE=Installed Python [C:\Python314]"
        )
    )
)

if not defined PYTHON_CMD (
    echo.
    echo [ERROR] No Python installation or virtual environment could be found!
    echo         Please install Python 3.10+ and ensure it is added to your PATH.
    echo.
    pause
    exit /b 1
)

echo [Python] Using %ENV_TYPE%
for /f "delims=" %%V in ('"%PYTHON_CMD%" --version 2^>^&1') do echo [Python] %%V

rem 4. Verify Backend Entry Point and Files
if not exist "run.py" (
    if not exist "backend\app.py" (
        echo.
        echo [ERROR] Backend entry point not found!
        echo         Neither run.py nor backend\app.py exists in "%~dp0".
        echo.
        pause
        exit /b 1
    )
)

if exist "weights\plantvillage_mobilenet_93.h5" (
    echo [Weights] Found MobileNetV2 model in weights\plantvillage_mobilenet_93.h5
) else if exist "plantvillage_mobilenet_93.h5" (
    echo [Weights] Found MobileNetV2 model in plantvillage_mobilenet_93.h5
) else (
    echo [Weights] NOTICE: Model file plantvillage_mobilenet_93.h5 not found.
    echo           Backend will run in simulation / demo fallback mode.
)

rem 5. Check for Port Conflict / Duplicate Server Process
set "OCCUPIED_PID="
for /f "tokens=5" %%P in ('netstat -ano ^| findstr :%BACKEND_PORT% ^| findstr LISTENING 2^>nul') do (
    set "OCCUPIED_PID=%%P"
)

if not defined OCCUPIED_PID goto :PORT_CHECK_OK

echo.
echo ======================================================================
echo   [WARNING] PORT CONFLICT DETECTED
echo   Port %BACKEND_PORT% is already in use by process PID: %OCCUPIED_PID%
echo ======================================================================
echo   An existing server or process is already listening on this port.
echo   Starting a duplicate server would fail with [Errno 10048].
echo.
echo   Choose an option:
echo     [1] Terminate existing process (PID %OCCUPIED_PID%) and start backend
echo     [2] Keep existing server running and exit launcher safely
echo.
set /p "CONFLICT_CHOICE=Enter choice [1 or 2, default 2]: "
if "!CONFLICT_CHOICE!"=="1" (
    echo Terminating process %OCCUPIED_PID%...
    taskkill /F /PID %OCCUPIED_PID% >nul 2>&1
    ping -n 2 127.0.0.1 >nul
    echo Port %BACKEND_PORT% released. Proceeding with startup...
) else (
    echo.
    echo [INFO] Exiting safely without modifying the existing server.
    echo        Existing backend remains accessible at http://%BACKEND_HOST%:%BACKEND_PORT%/
    echo.
    pause
    exit /b 0
)

:PORT_CHECK_OK

rem 6. Check Core Dependencies
"%PYTHON_CMD%" -c "import fastapi, uvicorn, PIL, numpy, dotenv" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Required Python packages are missing.
    echo         Run: pip install -r backend/requirements.txt
    echo.
    pause
    exit /b 1
)

rem 7. Configure UTF-8 and Unbuffered Environment
set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

echo.
echo ======================================================================
echo   STARTING AGROVISION AI BACKEND
echo ======================================================================
echo   API Server:   http://%BACKEND_HOST%:%BACKEND_PORT%
echo   API Docs:     http://%BACKEND_HOST%:%BACKEND_PORT%/docs
echo   Health Check: http://%BACKEND_HOST%:%BACKEND_PORT%/api/health
echo   Frontend UI:  http://%BACKEND_HOST%:%BACKEND_PORT%/
echo.
echo   Press CTRL+C at any time to shut down the server.
echo ======================================================================
echo.

rem Run the official application entry point
if exist "run.py" (
    "%PYTHON_CMD%" run.py
) else (
    "%PYTHON_CMD%" -m uvicorn backend.app:app --host %BACKEND_HOST% --port %BACKEND_PORT% --reload
)

set "EXIT_CODE=%ERRORLEVEL%"
echo.
echo ======================================================================
echo   AgroVision AI Backend server has stopped. (Exit code: %EXIT_CODE%)
echo ======================================================================
echo.
pause

@echo off
setlocal EnableExtensions EnableDelayedExpansion
title AgroVision AI - Frontend Interface
chcp 65001 >nul

rem ====================================================================
rem   AgroVision AI / NovaMind - Frontend Startup Script
rem ====================================================================

rem 1. Switch to project root directory
cd /d "%~dp0"

echo ======================================================================
echo   AgroVision AI - Crop Disease Detection Platform
echo   Frontend Interface Launcher
echo ======================================================================
echo.

rem 2. Read configuration from .env if present
set "FRONTEND_HOST=127.0.0.1"
set "FRONTEND_PORT=8000"

if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        set "KEY=%%A"
        set "VAL=%%B"
        for /f "tokens=* delims= " %%K in ("!KEY!") do set "KEY=%%K"
        for /f "tokens=* delims= " %%V in ("!VAL!") do set "VAL=%%V"
        if /i "!KEY!"=="HOST" set "FRONTEND_HOST=!VAL!"
        if /i "!KEY!"=="PORT" set "FRONTEND_PORT=!VAL!"
    )
)

set "TARGET_URL=http://%FRONTEND_HOST%:%FRONTEND_PORT%/"
set "HEALTH_URL=http://%FRONTEND_HOST%:%FRONTEND_PORT%/api/health"
set "DOCS_URL=http://%FRONTEND_HOST%:%FRONTEND_PORT%/docs"

rem 3. Detect Frontend Architecture & Framework
if exist "%~dp0frontend\package.json" (
    echo [Framework] Node.js package.json detected in frontend\
    where node >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Node.js is required but not installed or not in PATH.
        pause
        exit /b 1
    )
    where npm >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] npm is required but not installed or not in PATH.
        pause
        exit /b 1
    )
    cd /d "%~dp0frontend"
    if not exist "node_modules" (
        echo [INFO] Installing frontend dependencies...
        call npm install
    )
    echo [INFO] Starting Node.js frontend server...
    call npm start
    goto :EXIT_SCRIPT
)

if exist "%~dp0frontend\app.py" (
    echo [Framework] Python Streamlit frontend detected in frontend\
    cd /d "%~dp0frontend"
    streamlit run app.py
    goto :EXIT_SCRIPT
)

rem Actual project frontend: FastAPI-Integrated Responsive HTML5/CSS3/ES6 SPA
if not exist "%~dp0frontend\index.html" (
    echo [ERROR] Frontend file "frontend\index.html" not found in "%~dp0"!
    echo         Please ensure the frontend directory is present.
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0frontend"
echo [Framework] Responsive HTML5 / CSS3 / ES6 Single-Page Application
echo [Frontend]  %~dp0frontend\index.html (Verified)
echo [Host Port] Matching Backend Port: %FRONTEND_PORT%
echo.

rem 4. Verify Backend Service Availability (No blind sleep delay)
echo Checking connection to AgroVision AI Backend at %HEALTH_URL%...

set "IS_ONLINE=0"
set "MAX_TRIES=15"
set "TRY_COUNT=0"

:CHECK_LOOP
curl -s -f -m 2 -o nul "%HEALTH_URL%" 2>nul
if %ERRORLEVEL% EQU 0 (
    set "IS_ONLINE=1"
    goto :BACKEND_READY
)

set /a TRY_COUNT+=1
if %TRY_COUNT% EQU 1 (
    echo.
    echo ======================================================================
    echo   [NOTICE] Backend is not responding yet on port %FRONTEND_PORT%.
    echo ======================================================================
    echo   The AgroVision AI frontend connects to the backend API service for:
    echo     - MobileNetV2 deep learning leaf disease diagnosis
    echo     - Grad-CAM heatmap explainability
    echo     - Google Gemini Vision ^& Agronomy Chatbot
    echo.
    echo   Please make sure START_BACKEND.bat is running.
    echo   Waiting for backend to finish loading model weights...
    echo ======================================================================
)

if %TRY_COUNT% LSS %MAX_TRIES% (
    echo   [Wait] Attempt %TRY_COUNT% of %MAX_TRIES% - checking %HEALTH_URL%...
    ping -n 3 127.0.0.1 >nul
    goto :CHECK_LOOP
)

rem If backend didn't respond after retries
echo.
echo ======================================================================
echo   [WARNING] Backend server is currently offline or unreachable.
echo ======================================================================
echo   Expected backend endpoint: %HEALTH_URL%
echo.
echo   How to fix:
echo     1. Double-click START_BACKEND.bat in the project root.
echo     2. Wait until the backend reports:
echo        "Uvicorn running on http://%FRONTEND_HOST%:%FRONTEND_PORT%"
echo     3. Press [R] below to retry connection.
echo ======================================================================
echo.
:PROMPT_RETRY
set "USER_ACTION="
set /p "USER_ACTION=Enter [R] to retry connection, [O] to open anyway, or [Q] to quit: "
if not defined USER_ACTION exit /b 0
if /i "!USER_ACTION!"=="R" (
    set "TRY_COUNT=0"
    goto :CHECK_LOOP
)
if /i "!USER_ACTION!"=="O" (
    goto :OPEN_BROWSER
)
if /i "!USER_ACTION!"=="Q" (
    exit /b 0
)
goto :PROMPT_RETRY

:BACKEND_READY
echo.
echo ======================================================================
echo   [SUCCESS] Backend connection verified (Online ^& Healthy)
echo ======================================================================

:OPEN_BROWSER
echo.
echo   Frontend Application URL:
echo      %TARGET_URL%
echo.
echo   Launching default browser...
start "" "%TARGET_URL%"

echo.
echo ======================================================================
echo   AgroVision AI is running!
echo ======================================================================
echo   Console Controls:
echo     [O] Re-open application in default browser
echo     [D] Open API Documentation (Swagger Docs)
echo     [H] Run instant Backend Health Check
echo     [Q] Exit frontend launcher
echo ======================================================================
echo.

:INTERACTIVE_MENU
set "MENU_CHOICE="
set /p "MENU_CHOICE=Select an option [O/D/H/Q]: "
if not defined MENU_CHOICE (
    echo.
    echo Exiting frontend launcher. Note: Backend server continues running.
    exit /b 0
)

if /i "!MENU_CHOICE!"=="O" (
    echo Opening %TARGET_URL%...
    start "" "%TARGET_URL%"
    echo.
    goto :INTERACTIVE_MENU
)

if /i "!MENU_CHOICE!"=="D" (
    echo Opening %DOCS_URL%...
    start "" "%DOCS_URL%"
    echo.
    goto :INTERACTIVE_MENU
)

if /i "!MENU_CHOICE!"=="H" (
    echo.
    echo Testing %HEALTH_URL%...
    curl -s -m 3 "%HEALTH_URL%"
    echo.
    echo.
    goto :INTERACTIVE_MENU
)

if /i "!MENU_CHOICE!"=="Q" (
    echo.
    echo Exiting frontend launcher. Note: Backend server continues running.
    ping -n 2 127.0.0.1 >nul
    exit /b 0
)

echo Unknown command. Please enter O, D, H, or Q.
goto :INTERACTIVE_MENU

:EXIT_SCRIPT
pause

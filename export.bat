@echo off
setlocal enabledelayedexpansion

:: Set console title
title Export NC Bat

cd /d "%~dp0"

echo ===================================================
echo               Exporting NC Bat
echo ===================================================
echo.

:: 1. Determine python executable to use and ensure virtualenv integrity
if exist ".venv\Scripts\python.exe" if exist ".venv\pyvenv.cfg" (
    echo [NC Bat] Found virtual environment. Using .venv\Scripts\python.exe
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    if exist ".venv\Scripts\activate.bat" (
        echo [NC Bat] Activating virtual environment...
        call ".venv\Scripts\activate.bat"
    )
) else (
    echo [NC Bat] Virtual environment not found or broken. Using system python to recreate .venv
    set "PYTHON_EXE=python"
    "!PYTHON_EXE!" -V >nul 2>&1
    if !ERRORLEVEL! neq 0 (
        echo [NC Bat] ERROR: No usable python interpreter found on PATH.
        pause
        exit /b 1
    )
    if exist ".venv" (
        echo [NC Bat] Removing broken .venv and recreating...
        rd /s /q ".venv"
    )
    echo [NC Bat] Creating virtual environment in .venv...
    "!PYTHON_EXE!" -m venv .venv
    if !ERRORLEVEL! neq 0 (
        echo [NC Bat] ERROR: Failed to create virtual environment with !PYTHON_EXE!.
        pause
        exit /b 1
    )
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    if exist ".venv\Scripts\activate.bat" (
        echo [NC Bat] Activating newly created virtual environment...
        call ".venv\Scripts\activate.bat"
    )
)

:: 2. Ensure Assets directory exists
:: Ensure Assets directory exists in project root
if not exist "Assets" (
    mkdir "Assets"
)

:: 3. Copy NC Bat Blue.png to icon.png if it doesn't exist
if not exist "Assets\icon.png" (
    if exist "Assets\NC Bat Blue.png" (
        echo [NC Bat] Copying Assets\NC Bat Blue.png to Assets\icon.png...
        copy "Assets\NC Bat Blue.png" "Assets\icon.png" >nul
    ) else (
        echo [NC Bat] WARNING: Assets\NC Bat Blue.png not found. icon.png cannot be copied.
    )
)

:: If we have a PNG icon but not an ICO, attempt conversion using Pillow
if not exist "Assets\icon.ico" (
    if exist "Assets\icon.png" (
        echo [NC Bat] Found Assets\icon.png; attempting to convert to icon.ico
        "!PYTHON_EXE!" -c "from PIL import Image; Image.open('Assets\\icon.png').save('Assets\\icon.ico', sizes=[(256,256)])" 2>nul
        if !ERRORLEVEL! neq 0 (
            echo [NC Bat] Pillow not available; installing Pillow to convert icon...
            "!PYTHON_EXE!" -m pip install --upgrade pip setuptools wheel
            "!PYTHON_EXE!" -m pip install pillow
            "!PYTHON_EXE!" -c "from PIL import Image; Image.open('Assets\\icon.png').save('Assets\\icon.ico', sizes=[(256,256)])"
            if !ERRORLEVEL! neq 0 (
                echo [NC Bat] WARNING: Failed to convert icon.png to icon.ico. PyInstaller may require an .ico file.
            ) else (
                echo [NC Bat] Converted Assets\icon.png to Assets\icon.ico
            )
        ) else (
            echo [NC Bat] Converted Assets\icon.png to Assets\icon.ico
        )
    )
)

:: 4. Verify PyInstaller installation
echo [NC Bat] Verifying pip and PyInstaller installation...
"%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel
"%PYTHON_EXE%" -c "import PyInstaller" 2>nul
if %ERRORLEVEL% neq 0 (
    echo [NC Bat] PyInstaller is not installed in the target environment.
    echo [NC Bat] Installing PyInstaller...
    "!PYTHON_EXE!" -m pip install pyinstaller
    if !ERRORLEVEL! neq 0 (
        echo [NC Bat] Error: Failed to install PyInstaller.
        echo [NC Bat] Please make sure you have internet access or install it manually.
        pause
        exit /b 1
    )
)

:: 5. Run PyInstaller
echo.
echo [NC Bat] Building NC Bat standalone executable...
if exist "Assets\icon.ico" (
    echo [NC Bat] Commands: "!PYTHON_EXE!" -m PyInstaller with custom icon ...
    "!PYTHON_EXE!" -m PyInstaller --noconfirm --onefile --windowed --icon="Assets\icon.ico" --add-data "Assets;Assets" --name "NC Bat" "main.py"
) else (
    echo [NC Bat] Commands: "!PYTHON_EXE!" -m PyInstaller without custom icon ...
    "!PYTHON_EXE!" -m PyInstaller --noconfirm --onefile --windowed --add-data "Assets;Assets" --name "NC Bat" "main.py"
)

if %ERRORLEVEL% equ 0 (
    echo.
    echo ===================================================
    echo [NC Bat] Export completed successfully!
    echo [NC Bat] Executable location: dist\NC Bat.exe
    echo ===================================================
) else (
    echo.
    echo ===================================================
    echo [NC Bat] ERROR: Packaging failed.
    echo ===================================================
)

echo.
pause

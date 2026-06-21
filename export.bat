@echo off
setlocal enabledelayedexpansion

:: Set console title
title Export NC Bat

cd /d "%~dp0"

echo ===================================================
echo               Exporting NC Bat
echo ===================================================
echo.

:: 1. Determine python executable to use
if exist ".venv\Scripts\python.exe" (
    echo [NC Bat] Found virtual environment. Using .venv\Scripts\python.exe
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    echo [NC Bat] Virtual environment not found. Using system python.
    set "PYTHON_EXE=python"
)

:: 2. Ensure Assets directory exists
if not exist ".venv\Assets" (
    mkdir ".venv\Assets"
)

:: 3. Copy NC Bat Blue.png to icon.png if it doesn't exist
if not exist ".venv\Assets\icon.png" (
    if exist ".venv\Assets\NC Bat Blue.png" (
        echo [NC Bat] Copying NC Bat Blue.png to icon.png...
        copy ".venv\Assets\NC Bat Blue.png" ".venv\Assets\icon.png" >nul
    ) else (
        echo [NC Bat] WARNING: NC Bat Blue.png not found. icon.png cannot be copied.
    )
)

:: 4. Verify PyInstaller installation
echo [NC Bat] Verifying PyInstaller installation...
!PYTHON_EXE! -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [NC Bat] PyInstaller is not installed in the target environment.
    echo [NC Bat] Installing PyInstaller...
    !PYTHON_EXE! -m pip install pyinstaller
    if errorlevel 1 (
        echo [NC Bat] Error: Failed to install PyInstaller.
        echo [NC Bat] Please make sure you have internet access or install it manually.
        pause
        exit /b 1
    )
)

:: 5. Run PyInstaller
echo.
echo [NC Bat] Building NC Bat standalone executable...
echo [NC Bat] Commands: !PYTHON_EXE! -m PyInstaller ...
!PYTHON_EXE! -m PyInstaller --noconfirm --onefile --windowed --icon=".venv\Assets\icon.ico" --add-data ".venv\Assets;Assets" --name "NC Bat" "main.py"

if errorlevel 0 (
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

@echo off
echo 🔒 Encrypted Notes Manager
echo ==========================
echo.
echo Choose interface:
echo 1. GUI (Graphical Interface) - Default
echo 2. CLI (Command Line Interface)  
echo 3. Run Demo
echo 4. Setup Dependencies
echo 5. Exit
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" (
    echo Starting GUI mode...
    python main.py --gui 2>nul || py main.py --gui
) else if "%choice%"=="2" (
    echo Starting CLI mode...
    python main.py --cli 2>nul || py main.py --cli
) else if "%choice%"=="3" (
    echo Running demo...
    python demo.py 2>nul || py demo.py
) else if "%choice%"=="4" (
    echo Setting up dependencies...
    python setup.py 2>nul || py setup.py
) else if "%choice%"=="5" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Starting GUI mode by default...
    python main.py --gui 2>nul || py main.py --gui
)

pause

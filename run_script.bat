@echo off
cd /d "%~dp0"
echo Activating virtual environment...
call venv\Scripts\activate
echo Running main.py...
python main.py
echo.
echo Press any key to exit...
pause >nul
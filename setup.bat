@echo off
chcp 65001 >nul
echo ======================================================================
echo   GoPay Supabase Setup Assistant
echo ======================================================================
echo.
echo This will help you set up Supabase for your GoPay project.
echo.
pause

python setup_supabase.py

if errorlevel 1 (
    echo.
    echo Setup encountered an error. Please check the output above.
    pause
    exit /b 1
)

echo.
echo Setup complete! Run verify_setup.py to check your configuration.
pause

@echo off
:menu
cls
echo =========================
echo  Floyy Gen Control Panel
echo =========================
echo 1. Start Bot
echo 2. Restart Bot
echo 3. Kill Bot
echo 4. Exit
echo.

set /p choice=Select an option: 

if "%choice%"=="1" goto start
if "%choice%"=="2" goto restart
if "%choice%"=="3" goto kill
if "%choice%"=="4" exit

:start
start cmd /k "python bot.py"
pause
goto menu

:restart
taskkill /F /IM python.exe /T
timeout /t 2 >nul
start cmd /k "python bot.py"
pause
goto menu

:kill
taskkill /F /IM python.exe /T
pause
goto menu

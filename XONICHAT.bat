@echo off
title XONICHAT 2026 - Cliente Gemini para Terminal
color 0A

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo           XONICHAT 2026 - Cliente Gemini
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo Iniciando XONICHAT...
echo.
echo [INFO] Cliente Gemini optimizado para equipos de bajos recursos
echo [INFO] Modelo: gemini-2.5-flash
echo [INFO] Las API keys se guardan en: %USERPROFILE%\.xonichat\keys.txt
echo.
echo [COMANDOS]
echo   Escribe tu mensaje y presiona Enter
echo   /salir   - Terminar conversacion
echo   Ctrl+C   - Salir del programa
echo.
echo ============================================================
echo.

python start.py

pause

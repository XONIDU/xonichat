@echo off
title XONICHAT 2026 - Cliente Gemini para Terminal
color 0A

:: ============================================================
:: IR AL DIRECTORIO DONDE ESTA EL SCRIPT .BAT
:: ============================================================
cd /d "%~dp0"

:: ============================================================
:: VERIFICAR QUE start.py EXISTE
:: ============================================================
if not exist "%~dp0start.py" (
    echo [ERROR] No se encuentra start.py en esta carpeta
    echo.
    echo Ruta actual: %~dp0
    echo.
    echo Asegurate de que start.py esta en la misma carpeta que este .bat
    echo.
    pause
    exit /B
)

:: ============================================================
:: EJECUTAR start.py
:: ============================================================
cls
echo ============================================================
echo           XONICHAT 2026 - Cliente Gemini
echo ============================================================
echo.
echo [INFO] Directorio de trabajo: %~dp0
echo.
echo Iniciando XONICHAT...
echo.
echo [INFO] Cliente Gemini optimizado para equipos de bajos recursos
echo [INFO] Modelo: gemini-2.5-flash
echo [INFO] API keys: %USERPROFILE%\.xonichat\keys.txt
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
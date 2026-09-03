@echo off
title Lanzador - Estacion Terrena CubeCount
echo ===============================
echo    Iniciando Estacion Terrena 
echo ===============================
echo.

echo [1/2] Limpiando procesos fantasma y levantando Mosquitto

net stop mosquitto > NUL 2>&1
taskkill /F /IM mosquitto.exe > NUL 2>&1

start "Broker Mosquitto" cmd /k ""C:\Program Files\mosquitto\mosquitto.exe" -v -c mosquitto.conf"

echo [2/2] Iniciando el Motor de IA (YOLOv8)...

start "AI Subscriber" cmd /k "python ai_subscriber.py"

echo.
echo ¡Sistema lanzado exitosamente! 
echo Ya puedes iniciar el publicador en la Raspberry Pi.
echo.
pause
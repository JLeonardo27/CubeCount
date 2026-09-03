@echo off
title Lanzador - Estacion Terrena CubeCount
echo ===============================
echo    Iniciando Estacion Terrena 
echo ===============================
echo.

echo [1/2] Levantando el Broker MQTT (Mosquitto)...

start "Broker Mosquitto" cmd /k ""C:\Program Files\mosquitto\mosquitto.exe" -v"


timeout /t 2 /nobreak > NUL

echo [2/2] Iniciando el Motor de IA (YOLOv8)...

start "AI Subscriber" cmd /k "python ai_subscriber.py"

echo.
echo ¡Sistema lanzado exitosamente! 
echo Ya puedes iniciar el publicador en la Raspberry Pi.
echo.
pause
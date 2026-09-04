# CubeCount - Sistema de Visión Distribuida

**Fase 1/3:** Arquitectura de inferencia híbrida (Off-board) para detección de objetivos mediante telemetría de video sobre MQTT.

Este repositorio contiene la implementación inicial del sistema de visión por computadora para un dron autónomo. Para optimizar los recursos del hardware de vuelo y minimizar la latencia, el sistema desacopla la captura de video de la carga matemática de la red neuronal, comunicando ambos nodos mediante un broker local.

## Arquitectura del Sistema
* **Nodo Publicador (Raspberry Pi Zero 2W):** Accede al hardware de la cámara vía `Picamera2` (ISP nativo), comprime los fotogramas en JPEG y los transmite por un socket TCP usando Paho-MQTT con Calidad de Servicio (QoS) 0 para privilegiar la velocidad sobre la retención.
* **Nodo Suscriptor (Estación Terrena - Laptop):** Escucha el *topic* de video, decodifica los bytes en arreglos de Numpy y ejecuta inferencia en tiempo real utilizando un modelo YOLOv8 entrenado específicamente para detectar cubos Rubik.

## Stack Tecnológico
* **Lenguaje:** Python 3
* **Visión & IA:** OpenCV, Ultralytics YOLOv8, Roboflow (Dataset Augmentation).
* **Redes:** Mosquitto MQTT Broker, Paho-MQTT v2 API.
* **Hardware:** Raspberry Pi Zero 2W, Módulo de Cámara OV5647 (V4L2/libcamera).

## Despliegue Rápido

1. **Configurar el Broker (Estación Terrena):**
   Asegúrate de tener Mosquitto instalado y el puerto `1883` abierto en tu firewall local.
   
2. **Iniciar la Estación Terrena (Windows):**
   ```bash
   pip install -r requirements_laptop.txt
   cd mqtt_stream_src/laptop_node
   iniciar_estacion.bat
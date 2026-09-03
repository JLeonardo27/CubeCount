import paho.mqtt.client as mqtt
from common.config import MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE

class MQTTClientBase:
    def __init__(self, client_id):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[{client._client_id.decode()}] Conectado al broker exitosamente.")
        else:
            print(f"[{client._client_id.decode()}] Error de conexión. Código: {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"[{client._client_id.decode()}] Desconectado del broker.")

    def connect(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
            self.client.loop_start() 
        except Exception as e:
            print(f"Error al conectar con {MQTT_BROKER}: {e}")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

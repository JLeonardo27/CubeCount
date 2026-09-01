import cv2
import sys
import os
from ultralytics import YOLO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from common.config import TOPIC_VIDEO_STREAM
from common.utils import decode_frame
from common.mqtt_base import MQTTClientBase

class VideoSubscriber(MQTTClientBase):
    def __init__(self, client_id, model_path):
        super().__init__(client_id)

        self.model = YOLO(model_path)
        self.frame_to_process = None
    
        self.client.on_message = self.on_message
        self.connect()

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            # Suscripción con QoS 0 para evitar latencia de confirmación
            self.client.subscribe(TOPIC_VIDEO_STREAM, qos=0)
            print(f"Suscrito exitosamente al topic: {TOPIC_VIDEO_STREAM}")

    def on_message(self, client, userdata, msg):
        if msg.topic == TOPIC_VIDEO_STREAM:
            # Descomprimir los bytes a un arreglo numpy/OpenCV
            self.frame_to_process = decode_frame(msg.payload)

def main():
    # Inicializar el nodo usando el modelo entrenado
    subscriber = VideoSubscriber("Laptop_AI_Node", "best.pt")
    
    print("Esperando video desde la Raspberry Pi Zero 2W. Presiona 'q' para salir.")

    try:
        while True:
            # Si hay un fotograma nuevo en el buffer
            if subscriber.frame_to_process is not None:
                # Copiar el frame y limpiar el buffer para no bloquear el hilo de red
                frame = subscriber.frame_to_process.copy()
                subscriber.frame_to_process = None
                
                resultados = subscriber.model(frame, verbose=False)
                
                conteo = len(resultados[0].boxes)
                
                frame_anotado = resultados[0].plot()
                cv2.putText(frame_anotado, f'Cubos Rubik: {conteo}', (20, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                cv2.imshow('Estacion Terrena - Procesamiento Hibrido', frame_anotado)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nProcesamiento detenido por el usuario.")
    finally:
        cv2.destroyAllWindows()
        subscriber.stop()

if __name__ == "__main__":
    main()

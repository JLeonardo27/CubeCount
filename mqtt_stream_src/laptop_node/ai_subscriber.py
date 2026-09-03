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
    subscriber = VideoSubscriber("Laptop_AI_Node", "yolov8n.pt")
    
    dataset_dir = "dataset_rubik"
    os.makedirs(dataset_dir, exist_ok=True)
    img_counter = 0

    try:
        while True:
            if subscriber.frame_to_process is not None:
                frame = subscriber.frame_to_process.copy()
                subscriber.frame_to_process = None 

                cv2.imshow('Estacion Terrena - Recoleccion de Datos', frame)

            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                img_name = os.path.join(dataset_dir, f"rubik_frame_{img_counter:04d}.jpg")
                cv2.imwrite(img_name, frame)
                print(f"Foto guardada: {img_name}")
                img_counter += 1
                
    except KeyboardInterrupt:
        print("\nRecolección detenida por el usuario.")
    finally:
        cv2.destroyAllWindows()
        subscriber.stop()
                
if __name__ == "__main__":
    main()

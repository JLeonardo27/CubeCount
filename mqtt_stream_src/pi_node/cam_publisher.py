import cv2
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from common.config import TOPIC_VIDEO_STREAM, JPEG_QUALITY
from common.utils import encode_frame
from common.mqtt_base import MQTTClientBase

class VideoPublisher(MQTTClientBase):
    def __init__(self, client_id):
        super().__init__(client_id)
        self.connect()

    def publish_frame(self, frame_bytes):
        # QoS 0 (Fire and forget): Vital para no generar latencia en video
        self.client.publish(TOPIC_VIDEO_STREAM, frame_bytes, qos=0)

def main():
    publisher = VideoPublisher("PiZero_Cam")
    
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    print("Iniciando transmisión MQTT.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Esperando a la cámara")
                time.sleep(1)
                continue

            frame_bytes = encode_frame(frame, quality=JPEG_QUALITY)
            
            if frame_bytes:
                publisher.publish_frame(frame_bytes)
                
            time.sleep(0.03) 

    except KeyboardInterrupt:
        print("\nTransmisión detenida.")
    finally:
        cap.release()
        publisher.stop()

if __name__ == "__main__":
    main()

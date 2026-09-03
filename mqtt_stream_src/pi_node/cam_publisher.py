import cv2
import time
import sys
import os
from picamera2 import Picamera2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from common.config import TOPIC_VIDEO_STREAM, JPEG_QUALITY
from common.utils import encode_frame
from common.mqtt_base import MQTTClientBase

class VideoPublisher(MQTTClientBase):
    def __init__(self, client_id):
        super().__init__(client_id)
        self.connect()

    def publish_frame(self, frame_bytes):
        self.client.publish(TOPIC_VIDEO_STREAM, frame_bytes, qos=0)

def main():
    publisher = VideoPublisher("PiZero_Cam")
    
    # Inicializar la cámara nativa
    picam2 = Picamera2()
    

    config = picam2.create_video_configuration({"main": {"format": "BGR888", "size": (320, 240)}})
    picam2.configure(config)
    picam2.start()

    print("Iniciando transmisión MQTT con Picamera2... Presiona Ctrl+C para detener.")

    try:
        while True:

            frame = picam2.capture_array()

            frame_bytes = encode_frame(frame, quality=JPEG_QUALITY)
            
            if frame_bytes:
                publisher.publish_frame(frame_bytes)
                
            time.sleep(0.03) 

    except KeyboardInterrupt:
        print("\nTransmisión detenida por el usuario.")
    finally:
        picam2.stop()
        picam2.close()
        publisher.stop()

if __name__ == "__main__":
    main()

import cv2
import numpy as np

def encode_frame(frame, quality=60):
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    ret, buffer = cv2.imencode('.jpg', frame, encode_param)
    if not ret:
        return None
    return buffer.tobytes()

def decode_frame(payload):
    
    nparr = np.frombuffer(payload, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return frame

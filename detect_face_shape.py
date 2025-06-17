import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

mp_face_mesh = mp.solutions.face_mesh

# Key landmark indices
JAW_LEFT = 234
JAW_RIGHT = 454
FOREHEAD = 10
CHIN = 152

def detect_face_shape(image: Image.Image) -> str:
    img = np.array(image)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(img_rgb)
        if not results.multi_face_landmarks:
            return "unknown"

        face_landmarks = results.multi_face_landmarks[0]

        def get_point(index):
            h, w, _ = img.shape
            pt = face_landmarks.landmark[index]
            return np.array([int(pt.x * w), int(pt.y * h)])

        jaw_left = get_point(JAW_LEFT)
        jaw_right = get_point(JAW_RIGHT)
        forehead = get_point(FOREHEAD)
        chin = get_point(CHIN)

        jaw_width = np.linalg.norm(jaw_left - jaw_right)
        face_height = np.linalg.norm(forehead - chin)
        ratio = jaw_width / face_height

        # Basic shape rules
        if ratio > 0.9:
            return "round"
        elif 0.75 < ratio <= 0.9:
            return "square"
        else:
            return "oval"

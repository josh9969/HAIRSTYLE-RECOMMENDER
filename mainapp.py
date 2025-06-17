import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import json
from PIL import Image

def detect_face_shape(image):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)

    if not results.multi_face_landmarks:
        return None

    landmarks = results.multi_face_landmarks[0].landmark

    forehead = np.array([landmarks[10].x, landmarks[10].y])
    chin = np.array([landmarks[152].x, landmarks[152].y])
    left_cheek = np.array([landmarks[234].x, landmarks[234].y])
    right_cheek = np.array([landmarks[454].x, landmarks[454].y])
    jaw_left = np.array([landmarks[127].x, landmarks[127].y])
    jaw_right = np.array([landmarks[356].x, landmarks[356].y])

    face_height = np.linalg.norm(forehead - chin)
    face_width = np.linalg.norm(left_cheek - right_cheek)
    jaw_width = np.linalg.norm(jaw_left - jaw_right)

    ratio = face_height / face_width

    if ratio < 1.1:
        if jaw_width > face_width * 0.95:
            return "square"
        else:
            return "round"
    elif ratio > 1.5:
        return "oblong"
    elif jaw_width < face_width * 0.85:
        return "heart"
    elif jaw_width > face_width * 0.9:
        return "oval"
    else:
        return "diamond"

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="Hairstyle Recommender", layout="centered")
st.title("📸 Hairstyle Recommender Using Webcam")

captured_image = st.camera_input("Take a clear front-facing photo")

if captured_image:
    # Convert to OpenCV image
    img = Image.open(captured_image)
    img = np.array(img)
    image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    st.image(image, caption="Captured Photo", use_column_width=True)

    detected_shape = detect_face_shape(image)

    if detected_shape:
        st.success(f"Detected Face Shape: **{detected_shape.capitalize()}**")

        hairstyles = json.load(open("hairstyles.json"))

        if detected_shape in hairstyles:
            st.subheader(f"Recommended Hairstyles for {detected_shape.capitalize()} Face:")
            for style in hairstyles[detected_shape]:
                st.markdown(f"- {style}")
        else:
            st.warning("No hairstyle recommendations found for this face shape.")
    else:
        st.error("Couldn't detect a face in the photo. Please try again.")


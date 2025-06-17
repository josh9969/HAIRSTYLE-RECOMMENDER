import streamlit as st
import json
from PIL import Image
from detect_face_shape import detect_face_shape
import os

# Load recommendations
def load_recommendations():
    with open("hairstyles.json", "r") as file:
        return json.load(file)

st.set_page_config(page_title="Face Shape Hairstyle Recommender", layout="centered")
st.title("📸 AI Hairstyle Recommender")
st.markdown("Take a selfie and let the app detect your face shape to recommend styles!")

# Upload or capture
img_file = st.camera_input("Take a selfie")

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Detecting face shape..."):
        face_shape = detect_face_shape(image)
    
    if face_shape == "unknown":
        st.error("Face not detected. Try a clearer photo.")
    else:
        st.success(f"Detected Face Shape: **{face_shape.capitalize()}**")
        data = load_recommendations()
        styles = data.get(face_shape, [])

        if not styles:
            st.warning("No hairstyle recommendations found.")
        else:
            for style in styles:
                image_path = style["image"]
                if os.path.exists(image_path):
                    style_img = Image.open(image_path)
                    st.image(style_img, caption=style["name"], use_column_width=True)
                else:
                    st.warning(f"Image not found: {style['image']}")

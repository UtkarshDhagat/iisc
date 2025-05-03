import cv2
import numpy as np
import streamlit as st
from PIL import Image
from filters import (
    simulate_glaucoma,
    simulate_cataract_yellow,
    simulate_cataract_blur,
    simulate_retinopathy,
    simulate_macular_degeneration,
)

st.set_page_config(page_title="Retinal Disease Vision Simulator", layout="wide")
st.markdown("""
    <style>
        .title-style {
            font-size:36px;
            font-weight:700;
            color:#1f77b4;
        }
        .desc-style {
            font-size:18px;
            color:#333;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            color: gray;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-style'>🧠 Retinal Disease Vision Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='desc-style'>Simulate the effects of common retinal diseases in real-time using your webcam.</div>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.title("⚙️ Controls")
disease = st.sidebar.radio("Select Disease", [
    "Normal Vision",
    "Glaucoma",
    "Cataract",
    "Diabetic Retinopathy",
    "Macular Degeneration"
])
severity = st.sidebar.slider("Severity", 0.0, 1.0, 0.5, 0.05)
start_cam = st.sidebar.button("🎥 Start Camera")

FRAME_WINDOW = st.empty()

if disease == "Cataract":
    cataract_mode = st.selectbox(
        "Cataract Type",
        ["yellow", "blur"],
        format_func=lambda x: {
            "yellow": "Dull or Yellow Vision",
            "blur": "Blurry or Dim Vision",
        }[x]
    )
else:
    cataract_mode = None

def apply_filter(frame):
    if disease == "Glaucoma":
        return simulate_glaucoma(frame, severity)
    elif disease == "Cataract":
        mode = cataract_mode
        if mode == "yellow":
            return simulate_cataract_yellow(frame, severity)
        elif mode == "blur":
            return simulate_cataract_blur(frame, severity)
    elif disease == "Diabetic Retinopathy":
        return simulate_retinopathy(frame, severity)
    elif disease == "Macular Degeneration":
        return simulate_macular_degeneration(frame, severity)
    return frame

if start_cam:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access camera.")
            break
        frame = cv2.resize(frame, (640, 480))
        processed = apply_filter(frame)
        orig_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        proc_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        stacked = np.hstack((orig_rgb, proc_rgb))
        FRAME_WINDOW.image(stacked, channels="RGB")
    cap.release()

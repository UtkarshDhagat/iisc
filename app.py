import streamlit as st
import numpy as np
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
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

if disease == "Cataract":
    cataract_mode = st.sidebar.selectbox(
        "Cataract Type",
        ["yellow", "blur"],
        format_func=lambda x: {
            "yellow": "Dull or Yellow Vision",
            "blur": "Blurry or Dim Vision",
        }[x]
    )
else:
    cataract_mode = None

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.severity = severity
        self.static_mask = [None]

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if disease == "Glaucoma":
            return simulate_glaucoma(img, self.severity)
        elif disease == "Cataract":
            if cataract_mode == "yellow":
                return simulate_cataract_yellow(img, self.severity)
            elif cataract_mode == "blur":
                return simulate_cataract_blur(img, self.severity)
        elif disease == "Diabetic Retinopathy":
            return simulate_retinopathy(img, self.severity, self.static_mask)
        elif disease == "Macular Degeneration":
            return simulate_macular_degeneration(img, self.severity)
        return img

webrtc_streamer(
    key="live",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
    async_transform=True
)


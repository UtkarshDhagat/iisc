# 🧠 Retinal Disease Vision Simulator

This is a real-time webcam-based simulator that visually mimics the effects of various retinal diseases such as **Glaucoma**, **Cataract**, **Diabetic Retinopathy**, and **Macular Degeneration**. Built using **Streamlit**, **OpenCV**, and **streamlit-webrtc**, it lets users adjust disease severity and observe its impact on vision.

---

## 🧰 Features

- Live webcam stream directly in your browser
- Simulates:
  - Glaucoma (tunnel vision)
  - Cataract (yellow tint and blur)
  - Diabetic Retinopathy (random black blotches)
  - Macular Degeneration (central black spot)
- Adjustable severity slider for each condition
- Lightweight and easy to run locally

---

## 🔧 Installation & Running Locally

1. **Clone the repository**

   git clone https://github.com/yourusername/retinal-vision-simulator.git
   cd retinal-vision-simulator

2. **Create a virtual environment (optional but recommended)**

   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate

3. **Install dependencies**

   pip install -r requirements.txt

4. **Run the application**

   streamlit run app.py

5. **Open your browser** and visit:

   http://localhost:8501

You should now see the live simulation with webcam access.

---

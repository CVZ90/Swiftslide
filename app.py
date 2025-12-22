import streamlit as st
from pptx import Presentation
import google.generativeai as genai
import io
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="SwiftSlide AI | Premium Presentations", page_icon="🚀", layout="centered")

# 2. Custom CSS for Luxury Design
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-image: linear-gradient(to right, #00d4ff, #007bff);
        color: white;
        border: none;
        font-weight: bold;
        transition: 0.5s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
    }
    .whatsapp-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        text-decoration: none;
        border-radius: 15px;
        font-weight: bold;
        font-size: 18px;
        margin-top: 20px;
        transition: 0.3s;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        transform: translateY(-2px);
    }
    .title-text {
        text-align: center;
        background: -webkit-linear-gradient(#00d4ff, #007bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 55px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 1.2rem;'>High-End AI Presentations in Seconds</p>", unsafe_allow_html=True)
st.divider()

# 4. Logic & Setup
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 

# التصحيح هنا: نستدعي المفتاح باسمه البرمجي GEMINI_API_KEY
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets Configuration Error. Please check Streamlit Advanced Settings.")
    st.stop()

# 5. User Input Section
topic = st.text_input("", placeholder="Enter your presentation topic (e.g. Cyber Security Trends)")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('Magic is happening... Generating your slides'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Create high-quality presentation content about {topic}. Provide 5 slides with professional titles and 3 detailed bullet points each."
                response = model.generate_content(prompt)
                
                st.balloons()
                st.success("✅ Content Generated Successfully!")
                
                # Locked Section Design
                st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff;">
                    <h3 style="color: white; margin-top:0;">🔒 File Status: Locked</h3>
                    <p style="color: #cbd5e1;">Your professional PPTX file is ready for download.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.info(f"💳 **Payment Required:** Transfer **$4** via Whish Money to: **{WHISH_NUMBER}**")
                
                # WhatsApp Premium Button
                whatsapp_msg = f"Hello SwiftSlide! I just generated a presentation about '{topic}'. I've sent the $4 via Whish. Please unlock my file!"
                encoded_msg = urllib.parse.quote(whatsapp_msg)
                whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_msg}"
                
                st.markdown(f"""
                    <a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="25" style="margin-right:10px;">
                        Chat with us to Unlock & Download
                    </a>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("The AI is currently busy. Please try again in a few seconds.")
    else:
        st.warning("Please enter a topic to start.")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #4b5563; font-size: 0.8rem;'>SwiftSlide AI Lebanon © 2025 | Premium Service</p>", unsafe_allow_html=True)

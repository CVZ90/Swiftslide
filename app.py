import streamlit as st
from pptx import Presentation
import google.generativeai as genai
import io
import urllib.parse

# 1. Page Configuration (The "Tab" info)
st.set_page_config(page_title="SwiftSlide AI | Premium Presentations", page_icon="🚀", layout="centered")

# 2. Custom CSS for Luxury Design
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #007bff;
        color: white;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border: 1px solid #00d4ff;
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
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
    }
    .title-text {
        text-align: center;
        background: -webkit-linear-gradient(#00d4ff, #007bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>The Fastest Way to Create Professional Presentations in Lebanon</p>", unsafe_allow_html=True)
st.divider()

# 4. Logic & Setup
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 

try:
    api_key = st.secrets["AIzaSyDOx1zkGMZVnxbBcy4WdmwCiI4ArzSVi2M"]
except:
    st.error("Configuration Error: API Key not found.")
    st.stop()

# 5. User Input Section
topic = st.text_input("Enter your presentation topic:", placeholder="e.g. The Future of AI in Medicine")

if st.button("Generate Presentation ✨"):
    if topic:
        with st.spinner('Crafting your professional slides...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Create high-quality presentation content about {topic}. Provide 5 slides with professional titles and 3 detailed bullet points each."
                response = model.generate_content(prompt)
                
                # Success UI
                st.balloons()
                st.success("✅ Your presentation is ready!")
                
                # Locked Section Design
                st.markdown("---")
                st.markdown("### 🔒 File Status: Locked")
                st.info(f"To unlock and download the **.pptx** file, please transfer **$4** via Whish Money to: **{WHISH_NUMBER}**")
                
                # WhatsApp Premium Button with Icon
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
                st.error("Connection Error. Please check your API settings.")
    else:
        st.warning("Please enter a topic first.")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #4b5563;'>Powered by SwiftSlide Lebanon © 2025</p>", unsafe_allow_html=True)

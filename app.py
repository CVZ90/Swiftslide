import streamlit as st
from pptx import Presentation
import google.generativeai as genai
import io
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="SwiftSlide AI | Premium", page_icon="🚀", layout="centered")

# 2. Luxury CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text {
        text-align: center;
        background: -webkit-linear-gradient(#00d4ff, #007bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px; font-weight: bold;
    }
    .whatsapp-btn {
        display: flex; align-items: center; justify-content: center;
        background-color: #25D366; color: white !important;
        padding: 15px; text-decoration: none; border-radius: 15px;
        font-weight: bold; font-size: 18px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.divider()

# 3. Logic & API Setup
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 

# جلب المفتاح مع فحص الأخطاء
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 Missing API Key in Streamlit Secrets!")
    st.stop()

# 4. Input Section
topic = st.text_input("Enter your topic:", placeholder="e.g. Artificial Intelligence")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('Magic is happening...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                # توليد المحتوى
                response = model.generate_content(f"Create a 5-slide presentation about {topic}. Provide Title and 3 bullets per slide.")
                
                if response.text:
                    st.balloons()
                    st.success("✅ Content Generated!")
                    st.markdown(f"### Preview:\n{response.text}") # عرض المحتوى للتأكد من أنه يعمل
                    
                    # Locked Section & WhatsApp
                    st.markdown("---")
                    st.warning("🔒 File is Locked. Pay $4 via Whish to unlock.")
                    
                    whatsapp_msg = f"Hello SwiftSlide! I generated a presentation about '{topic}'. I've sent $4 to {WHISH_NUMBER}. Please unlock!"
                    whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={urllib.parse.quote(whatsapp_msg)}"
                    
                    st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">Chat to Unlock & Download</a>', unsafe_allow_html=True)
            
            except Exception as e:
                # هذا السطر سيخبرنا بالخطأ الحقيقي
                st.error(f"⚠️ Technical Error: {str(e)}")
    else:
        st.warning("Please enter a topic.")

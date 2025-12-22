import streamlit as st
from groq import Groq
import urllib.parse

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="SwiftSlide AI | Fast", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text {
        text-align: center;
        background: -webkit-linear-gradient(#00d4ff, #007bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 55px; font-weight: bold;
    }
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3.5em;
        background-image: linear-gradient(to right, #00d4ff, #007bff);
        color: white; border: none; font-weight: bold; font-size: 18px;
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
st.markdown("<p style='text-align: center; color: #9ca3af;'>Super-Fast AI Presentations (Powered by Groq)</p>", unsafe_allow_html=True)
st.divider()

# 2. الثوابت وإعدادات Groq
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 

# احصل على المفتاح من إعدادات Streamlit Secrets باسم GROQ_API_KEY
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("🚨 Configuration Error: GROQ_API_KEY not found in Secrets.")
    st.stop()

# 3. واجهة المستخدم
topic = st.text_input("Enter topic:", placeholder="e.g. Future of Tech in Lebanon", key="groq_topic")

if st.button("Generate Fast Presentation ✨"):
    if topic:
        with st.spinner('Groq is thinking at light speed...'):
            try:
                # إنشاء اتصال مع Groq
                client = Groq(api_key=api_key)
                
                # طلب المحتوى باستخدام نموذج Llama 3 القوي
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional presentation assistant. Provide a 5-slide outline with Title and 3 detailed bullets per slide."
                        },
                        {
                            "role": "user",
                            "content": f"Create a presentation about: {topic}",
                        }
                    ],
                    model="llama-3.3-70b-versatile", # أحدث وأقوى نموذج في Groq
                )
                
                content = chat_completion.choices[0].message.content
                
                if content:
                    st.balloons()
                    st.success("✅ Content Generated in Milliseconds!")
                    
                    with st.expander("👁️ Preview Slide Content"):
                        st.markdown(content)
                    
                    st.markdown("---")
                    st.warning("🔒 File is Locked. Pay $4 via Whish to unlock.")
                    
                    # رابط الواتساب
                    msg = urllib.parse.quote(f"Hello! I generated a presentation about '{topic}'. I've sent $4 to {WHISH_NUMBER}. Send me the file!")
                    st.markdown(f'<a href="https://wa.me/{MY_PHONE_NUMBER}?text={msg}" class="whatsapp-btn">Chat to Unlock & Download</a>', unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"⚠️ Technical Error: {str(e)}")
    else:
        st.warning("Please enter a topic.")

st.markdown("<br><p style='text-align: center; color: #4b5563;'>SwiftSlide AI Lebanon © 2025</p>", unsafe_allow_html=True)

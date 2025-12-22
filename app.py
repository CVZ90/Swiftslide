import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="SwiftSlide AI", page_icon="🚀", layout="centered")

# 2. تصميم الواجهة
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3.5em; background-image: linear-gradient(to right, #00d4ff, #007bff); color: white; border: none; font-weight: bold; font-size: 18px; }
    .whatsapp-btn { display: flex; align-items: center; justify-content: center; background-color: #25D366; color: white !important; padding: 15px; text-decoration: none; border-radius: 15px; font-weight: bold; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.divider()

# 3. إعدادات الاتصال
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key is missing!")
    st.stop()

# 4. واجهة المستخدم
topic = st.text_input("Enter your topic:", key="user_topic_input")

if st.button("Generate Presentation ✨"):
    if topic:
        with st.spinner('AI is generating content...'):
            try:
                # إعداد المكتبة
                genai.configure(api_key=api_key)
                
                # استخدام النموذج الذي ظهر في القائمة رقم 3 لديك
                # هذا الاسم هو الأكثر حداثة وتوافقاً مع حسابك
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                response = model.generate_content(f"Create a 5-slide outline about {topic}. Title and 3 bullets per slide.")
                
                if response and response.text:
                    st.balloons()
                    st.success("✅ Content Generated!")
                    with st.expander("👁️ Preview Content"):
                        st.markdown(response.text)
                    
                    st.divider()
                    st.info(f"💳 Whish Money: {WHISH_NUMBER}")
                    
                    msg = urllib.parse.quote(f"Hello! I generated a slide about {topic}. I sent $4 to {WHISH_NUMBER}. Unlock please!")
                    st.markdown(f'<a href="https://wa.me/{MY_PHONE_NUMBER}?text={msg}" class="whatsapp-btn">Chat to Unlock</a>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"⚠️ Technical Error: {str(e)}")
                st.info("Tip: If you see 'Model not found', try using a new API Key from a different Google account.")
    else:
        st.warning("Please enter a topic.")

st.markdown("<br><p style='text-align: center; color: #4b5563;'>SwiftSlide AI Lebanon © 2025</p>", unsafe_allow_html=True)

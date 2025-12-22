import streamlit as st
from google import genai
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="SwiftSlide AI | v2", page_icon="🚀")

# تصميم فخم
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: bold; }
    .whatsapp-btn { display: flex; align-items: center; justify-content: center; background-color: #25D366; color: white !important; padding: 15px; text-decoration: none; border-radius: 15px; font-weight: bold; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)

# الروابط والأرقام
MY_PHONE_NUMBER = "96181950506"
WHISH_NUMBER = "81950506"

# جلب المفتاح
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing!")
    st.stop()

topic = st.text_input("Enter Topic (e.g. Modern Architecture):")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('Using New Google GenAI SDK...'):
            try:
                # الطريقة الجديدة للمكتبة التي أرسلتها
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # أحدث نموذج متاح
                    contents=f"Create a 5-slide outline for a presentation about {topic}. Provide Title and 3 bullets per slide."
                )
                
                if response.text:
                    st.balloons()
                    st.success("✅ Content Generated with v2 SDK!")
                    
                    with st.expander("Preview Content"):
                        st.write(response.text)
                    
                    st.divider()
                    st.info(f"💳 Whish Money: {WHISH_NUMBER}")
                    
                    msg = urllib.parse.quote(f"Hello! I generated a slide about {topic}. I sent $4 to {WHISH_NUMBER}. Unlock please!")
                    st.markdown(f'<a href="https://wa.me/{MY_PHONE_NUMBER}?text={msg}" class="whatsapp-btn">Chat to Unlock & Download</a>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Technical Error: {str(e)}")
    else:
        st.warning("Please enter a topic.")

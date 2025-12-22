import streamlit as st
from google import genai
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="SwiftSlide AI", page_icon="🚀", layout="centered")

# 2. تصميم الواجهة
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
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
    .title-text {
        text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 55px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Premium AI Presentations</p>", unsafe_allow_html=True)
st.divider()

# 3. المعلومات
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing!")
    st.stop()

# 4. المدخلات
topic = st.text_input("", placeholder="What is your topic?")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('AI is crafting your slides...'):
            try:
                # إنشاء العميل
                client = genai.Client(api_key=api_key)
                
                # التعديل الحاسم هنا: نكتب الاسم "gemini-1.5-flash" مباشرة بدون إضافات
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=f"Create a 5-slide presentation about {topic}. Title and 3 bullets each."
                )
                
                if response.text:
                    st.balloons()
                    st.success("✅ Success!")
                    with st.expander("Preview"):
                        st.write(response.text)
                    
                    st.divider()
                    st.info(f"💳 Whish: {WHISH_NUMBER}")
                    
                    whatsapp_msg = f"Hello SwiftSlide! I generated a presentation about '{topic}'. Payed $4 to {WHISH_NUMBER}."
                    st.markdown(f'<a href="https://wa.me/{MY_PHONE_NUMBER}?text={urllib.parse.quote(whatsapp_msg)}" class="whatsapp-btn">Chat to Unlock</a>', unsafe_allow_html=True)
                
            except Exception as e:
                # معالجة الخطأ لإظهار رسالة واضحة
                st.error(f"⚠️ Technical Detail: {str(e)}")
    else:
        st.warning("Please enter a topic.")

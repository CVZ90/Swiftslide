import streamlit as st
import google.generativeai as genai
import urllib.parse

# إعدادات الصفحة والتصميم
st.set_page_config(page_title="SwiftSlide AI", page_icon="🚀")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: bold; }
    .whatsapp-btn { display: flex; align-items: center; justify-content: center; background-color: #25D366; color: white !important; padding: 15px; text-decoration: none; border-radius: 15px; font-weight: bold; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)

# البيانات 
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing in Secrets!")
    st.stop()

topic = st.text_input("Presentation Topic:", placeholder="e.g. Quantum Computing")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('Connecting to Google AI Studio...'):
            try:
                # إعداد المكتبة
                genai.configure(api_key=api_key)
                
                # استخدام النموذج الأكثر استقراراً وتوافقاً
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # محاولة توليد المحتوى
                response = model.generate_content(f"Create a 5-slide outline about {topic}. Title and 3 bullets per slide.")
                
                if response.text:
                    st.balloons()
                    st.success("✅ Content Generated Successfully!")
                    with st.expander("Preview Content"):
                        st.write(response.text)
                    
                    st.divider()
                    st.info(f"💳 Transfer $4 to Whish: {WHISH_NUMBER}")
                    
                    msg = urllib.parse.quote(f"Hello! I generated a slide about {topic}. I sent $4 to {WHISH_NUMBER}. Unlock please!")
                    st.markdown(f'<a href="https://wa.me/{MY_PHONE_NUMBER}?text={msg}" class="whatsapp-btn">Chat to Unlock</a>', unsafe_allow_html=True)
                
            except Exception as e:
                # في حال استمر الخطأ، سنقوم بطباعة قائمة النماذج المتاحة لك لتعرف ماذا تختار
                st.error(f"Technical Error: {str(e)}")
                if "404" in str(e):
                    st.info("Searching for available models on your account...")
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    st.write("Available models on your key:", available_models)
    else:
        st.warning("Please enter a topic.")

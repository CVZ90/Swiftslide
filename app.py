import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="SwiftSlide AI", page_icon="🚀", layout="centered")

# 2. تصميم الواجهة المحترف
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 55px; font-weight: bold; }
    .whatsapp-btn { display: flex; align-items: center; justify-content: center; background-color: #25D366; color: white !important; padding: 15px; text-decoration: none; border-radius: 15px; font-weight: bold; margin-top: 20px; transition: 0.3s; }
    .whatsapp-btn:hover { background-color: #128C7E; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.divider()

# 3. المعلومات الأساسية
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing!")
    st.stop()

# 4. المدخلات
topic = st.text_input("Enter Topic:", placeholder="e.g. Computer Science in Lebanon")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('AI is generating your content using Gemini 2.0...'):
            try:
                genai.configure(api_key=api_key)
                
                # استخدام الاسم الصحيح تماماً من القائمة التي ظهرت لك
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                response = model.generate_content(f"Create a professional 5-slide presentation about {topic}. Provide a title and 3 detailed bullets per slide. Language: English.")
                
                if response.text:
                    st.balloons()
                    st.success("✅ Presentation Created Successfully!")
                    
                    with st.expander("👁️ Preview Your Content"):
                        st.markdown(response.text)
                    
                    st.markdown("---")
                    st.warning("🔒 File is Locked. Pay $4 via Whish to unlock.")
                    st.info(f"💳 Whish Number: {WHISH_NUMBER}")
                    
                    whatsapp_msg = f"Hello SwiftSlide! I generated a presentation about '{topic}'. I've sent the $4 to {WHISH_NUMBER}. Please send me the file!"
                    st.markdown(f'<a href="https://wa.me/{MY_PHONE_NUMBER}?text={urllib.parse.quote(whatsapp_msg)}" class="whatsapp-btn">Chat to Unlock & Download</a>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"⚠️ Technical Error: {str(e)}")
    else:
        st.warning("Please enter a topic.")

st.markdown("<br><p style='text-align: center; color: #4b5563;'>SwiftSlide AI Lebanon © 2025</p>", unsafe_allow_html=True)

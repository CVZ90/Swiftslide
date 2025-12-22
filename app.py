import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. إعدادات الصفحة والتصميم الفخم (Luxury Dark UI)
st.set_page_config(page_title="SwiftSlide AI | Premium", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text {
        text-align: center;
        background: -webkit-linear-gradient(#00d4ff, #007bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 55px; font-weight: bold;
        margin-bottom: 5px;
    }
    .subtitle-text {
        text-align: center; color: #9ca3af; font-size: 1.1rem; margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3.5em;
        background-image: linear-gradient(to right, #00d4ff, #007bff);
        color: white; border: none; font-weight: bold; font-size: 18px; transition: 0.4s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3); }
    .whatsapp-btn {
        display: flex; align-items: center; justify-content: center;
        background-color: #25D366; color: white !important;
        padding: 15px; text-decoration: none; border-radius: 15px;
        font-weight: bold; font-size: 18px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الهيدر
st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Your Premium AI Presentation Partner in Lebanon</p>', unsafe_allow_html=True)
st.divider()

# 3. الثوابت (الإعدادات)
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 
api_key = st.secrets.get("GEMINI_API_KEY")

# 4. منطق العمل
if not api_key:
    st.error("🚨 API Key is missing! Please add it to Streamlit Secrets.")
    st.stop()

topic = st.text_input("What is your presentation topic?", placeholder="e.g. Artificial Intelligence in 2025")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('AI is crafting your slides...'):
            try:
                # إعداد الاتصال بالذكاء الاصطناعي
                genai.configure(api_key=api_key)
                
                # استخدام النموذج المستقر 1.5-flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # طلب المحتوى
                prompt = f"Create a professional 5-slide presentation about {topic}. For each slide, provide a Title and 3-4 detailed bullet points. Language: English."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.balloons()
                    st.success("✅ Content Generated Successfully!")
                    
                    # معاينة المحتوى
                    with st.expander("👁️ Preview Slide Content"):
                        st.markdown(response.text)
                    
                    st.markdown("---")
                    st.markdown("### 🔒 File Status: Locked")
                    st.info(f"To download the PPTX file, please transfer **$4** via Whish Money to: **{WHISH_NUMBER}**")
                    
                    # زر الواتساب
                    whatsapp_msg = f"Hello SwiftSlide! I generated a presentation about '{topic}'. I've sent the $4 to {WHISH_NUMBER}. Please send me the file!"
                    encoded_msg = urllib.parse.quote(whatsapp_msg)
                    whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_msg}"
                    
                    st.markdown(f"""
                        <a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">
                            Chat with us to Unlock & Download
                        </a>
                    """, unsafe_allow_html=True)
            
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ Server is busy (Quota Limit). Please wait 1 minute and try again.")
                else:
                    st.error(f"⚠️ Technical Error: {str(e)}")
    else:
        st.warning("Please enter a topic.")

# الفوتر
st.markdown("<br><hr><p style='text-align: center; color: #4b5563; font-size: 0.8rem;'>SwiftSlide AI Lebanon © 2025</p>", unsafe_allow_html=True)

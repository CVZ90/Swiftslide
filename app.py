import streamlit as st
from google import genai
import urllib.parse

# 1. إعدادات الصفحة (Tab Configuration)
st.set_page_config(
    page_title="SwiftSlide AI | Premium Presentations", 
    page_icon="🚀", 
    layout="centered"
)

# 2. تصميم الواجهة (Luxury Neon Design)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3.5em;
        background-image: linear-gradient(to right, #00d4ff, #007bff);
        color: white;
        border: none;
        font-weight: bold;
        font-size: 18px;
        transition: 0.5s;
        cursor: pointer;
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
    .subtitle-text {
        text-align: center;
        color: #9ca3af;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قسم الهيدر (Header Section)
st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">High-End AI Presentations in Seconds</p>', unsafe_allow_html=True)
st.divider()
 

# جلب المفتاح السري من الإعدادات
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 Configuration Error: GEMINI_API_KEY not found in Secrets.")
    st.stop()

# 5. مدخلات المستخدم (User Input)
topic = st.text_input("", placeholder="What is your presentation topic? (e.g. Cybersecurity)")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('AI is crafting your slides... Please wait.'):
            try:
                # استخدام المكتبة الجديدة v2
                client = genai.Client(api_key=api_key)
                
                # استخدام نموذج 1.5 flash لأنه الأكثر استقراراً للحسابات المجانية
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"Create a professional 5-slide presentation about {topic}. Provide a title and 3-4 detailed bullets for each slide. Language: English."
                )
                
                if response.text:
                    st.balloons()
                    st.success("✅ Content Generated Successfully!")
                    
                    # عرض المحتوى للمستخدم (Preview)
                    with st.expander("👁️ View Slide Content"):
                        st.markdown(response.text)
                    
                    # قسم الدفع المقفل
                    st.markdown("""
                    <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; margin-top: 20px;">
                        <h3 style="color: white; margin-top:0;">🔒 File Status: Locked</h3>
                        <p style="color: #cbd5e1;">Your professional PPTX file is ready. Pay to unlock.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"💳 **Payment:** Transfer **$4** via Whish Money to: **{WHISH_NUMBER}**")
                    
                    # زر الواتساب الاحترافي
                    whatsapp_msg = f"Hello SwiftSlide! I generated a presentation about '{topic}'. I've sent the $4 to {WHISH_NUMBER}. Please send me the file!"
                    encoded_msg = urllib.parse.quote(whatsapp_msg)
                    whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_msg}"
                    
                    st.markdown(f"""
                        <a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="25" style="margin-right:10px;">
                            Chat with us to Unlock & Download
                        </a>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                # التعامل مع خطأ الزحمة (Quota) بشكل لبق
                if "429" in str(e):
                    st.error("⚠️ Server Busy: Google's AI is on break for 60 seconds. Please wait a minute and click Generate again.")
                else:
                    st.error(f"⚠️ Technical Error: {str(e)}")
    else:
        st.warning("Please enter a topic to start.")

# 6. الفوتر (Footer)
st.markdown("<br><hr><p style='text-align: center; color: #4b5563; font-size: 0.8rem;'>SwiftSlide AI Lebanon © 2025 | Premium Service</p>", unsafe_allow_html=True)

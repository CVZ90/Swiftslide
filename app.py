import streamlit as st
from groq import Groq
from pptx import Presentation
import io
import urllib.parse

# 1. إعدادات الصفحة والتصميم الفخم (Blue Dark UI)
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
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3.5em;
        background-image: linear-gradient(to right, #00d4ff, #007bff);
        color: white; border: none; font-weight: bold; font-size: 18px;
    }
    .unlock-box { 
        background-color: #161b22; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #007bff;
        margin-top: 20px;
    }
    .whatsapp-btn {
        display: flex; align-items: center; justify-content: center;
        background-color: #25D366; color: white !important;
        padding: 15px; text-decoration: none; border-radius: 12px;
        font-weight: bold; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. الدالة المحسنة لصناعة البوربوينت (بدون أخطاء)
def create_pptx(text_content, topic_name):
    prs = Presentation()
    
    # سلايد العنوان
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = str(topic_name).upper()
    slide.placeholders[1].text = "Professional AI Generated Presentation"

    # تقسيم المحتوى بناءً على كلمة Slide
    sections = text_content.split("Slide")
    for section in sections:
        if len(section).strip() > 10:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            lines = section.strip().split("\n")
            
            # وضع العنوان (أول سطر بعد كلمة Slide)
            slide.shapes.title.text = str(lines[0]).replace(":", "").strip()
            
            # إضافة النقاط
            body = slide.placeholders[1].text_frame
            for line in lines[1:]:
                clean_line = str(line).strip("-*• ")
                if clean_line:
                    p = body.add_paragraph()
                    p.text = clean_line

    binary_io = io.BytesIO()
    prs.save(binary_io)
    return binary_io.getvalue()

# 3. الثوابت والاتصال
ADMIN_UNLOCK_CODE = "SWIFT2025" 
WHISH_NUMBER = "81950506"
MY_PHONE = "96181950506"

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Create Professional PowerPoint in Seconds</p>", unsafe_allow_html=True)
st.divider()

# 4. منطق التطبيق
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

topic = st.text_input("What is your presentation about?", placeholder="e.g. Future of AI", key="main_input")

if st.button("Generate Presentation ✨"):
    if topic:
        with st.spinner("🚀 Designing your slides..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Create a 5-slide presentation. Use 'Slide X: Title' format followed by bullets. English language."},
                        {"role": "user", "content": f"Topic: {topic}"}
                    ]
                )
                content = response.choices[0].message.content
                st.session_state['content'] = content
                st.session_state['pptx'] = create_pptx(content, topic)
                st.session_state['active'] = True
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 5. عرض النتائج ونظام القفل
if st.session_state.get('active'):
    st.success("✅ Presentation Ready!")
    with st.expander("👁️ View Outline"):
        st.markdown(st.session_state['content'])
    
    st.markdown('<div class="unlock-box">', unsafe_allow_html=True)
    st.markdown("### 🔒 Unlock PPTX File")
    st.write(f"Send **$4** via Whish to **{WHISH_NUMBER}** to get your code.")
    
    code = st.text_input("Enter Activation Code:", key="unlock_key")
    
    if code == ADMIN_UNLOCK_CODE:
        st.balloons()
        st.download_button(
            label="📥 Download PowerPoint File",
            data=st.session_state['pptx'],
            file_name=f"{topic}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    elif code != "":
        st.error("Incorrect code.")
        
    msg = urllib.parse.quote(f"I paid $4 for '{topic}'. Send code!")
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text={msg}" class="whatsapp-btn">Chat to Get Code</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

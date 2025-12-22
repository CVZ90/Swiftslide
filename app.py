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

# 2. الدالة المحسنة لصناعة البوربوينت (تم إصلاح خطأ strip)
def create_pptx(text_content, topic_name):
    prs = Presentation()
    
    # سلايد العنوان
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = str(topic_name).upper()
    slide.placeholders[1].text = "Professional AI Generated Presentation\nPremium Edition"

    # تقسيم المحتوى بناءً على كلمة Slide
    sections = str(text_content).split("Slide")
    for section in sections:
        clean_section = section.strip()
        if len(clean_section) > 10:
            slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(slide_layout)
            lines = clean_section.split("\n")
            
            # وضع العنوان بأمان
            title_line = str(lines[0]).replace(":", "").strip()
            # إزالة أي أرقام زائدة في بداية العنوان لتجنب التكرار
            slide.shapes.title.text = "".join([i for i in title_line if not i.isdigit()]).strip()
            
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
if not api_key:
    st.error("Missing GROQ_API_KEY in Secrets!")
    st.stop()

client = Groq(api_key=api_key)

topic = st.text_input("What is your presentation about?", placeholder="e.g. Life on Mars", key="main_topic_input")

if st.button("Generate Presentation ✨"):
    if topic:
        with st.spinner("🚀 AI is crafting your slides..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Create a 5-slide professional presentation. Use 'Slide X: Title' format followed by 3-4 bullet points. English language only."},
                        {"role": "user", "content": f"Topic: {topic}"}
                    ]
                )
                content = response.choices[0].message.content
                st.session_state['content'] = content
                st.session_state['pptx_file'] = create_pptx(content, topic)
                st.session_state['generated'] = True
            except Exception as e:
                st.error(f"Technical Error: {str(e)}")

# 5. نظام القفل والتحميل
if st.session_state.get('generated'):
    st.success("✅ Content Generated Successfully!")
    with st.expander("👁️ Preview Content"):
        st.markdown(st.session_state['content'])
    
    st.markdown('<div class="unlock-box">', unsafe_allow_html=True)
    st.markdown("### 🔒 Unlock PowerPoint (.pptx)")
    st.write(f"To download the file, please send **$4** to Whish: **{WHISH_NUMBER}**")
    
    unlock_code = st.text_input("Enter Activation Code:", key="user_unlock_code")
    
    if unlock_code == ADMIN_UNLOCK_CODE:
        st.balloons()
        st.download_button(
            label="📥 Download PowerPoint File",
            data=st.session_state['pptx_file'],
            file_name=f"{topic}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True
        )
    elif unlock_code != "":
        st.error("Invalid activation code.")
        
    # زر الواتساب
    whatsapp_url = f"https://wa.me/{MY_PHONE}?text=" + urllib.parse.quote(f"I paid $4 for '{topic}'. Send me the code!")
    st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn">Chat with Admin for Code</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #4b5563; font-size: 0.8rem;'>SwiftSlide AI Lebanon © 2025</p>", unsafe_allow_html=True)

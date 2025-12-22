import streamlit as st
from groq import Groq
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import io
import requests
import urllib.parse

# 1. إعدادات الواجهة (Dark Luxury)
st.set_page_config(page_title="SwiftSlide AI", page_icon="🚀")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .title-text { text-align: center; color: #00d4ff; font-size: 45px; font-weight: bold; }
    .unlock-box { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #007bff; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 2. دالة صناعة البوربوينت (ألوان فخمة + معالجة أخطاء)
def create_luxury_pptx(text_content, topic_name):
    prs = Presentation()
    
    # سلايد العنوان (خلفية داكنة)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(14, 17, 23)
    
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(2))
    p = title_box.text_frame.add_paragraph()
    p.text = str(topic_name).upper()
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(0, 212, 255)

    # معالجة السلايدات
    sections = str(text_content).split("Slide")
    for section in sections:
        if len(section.strip()) > 10:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = RGBColor(30, 30, 30) # رمادي غامق جداً
            
            lines = section.strip().split("\n")
            title_text = str(lines[0]).replace(":", "").strip()
            
            # العنوان
            t_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1))
            tp = t_box.text_frame.add_paragraph()
            tp.text = title_text
            tp.font.size = Pt(28)
            tp.font.color.rgb = RGBColor(0, 212, 255)

            # محاولة جلب صورة (إذا فشلت لا يتوقف الكود)
            try:
                img_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=400&auto=format&fit=crop"
                response = requests.get(img_url, timeout=3)
                if response.status_code == 200:
                    slide.shapes.add_picture(io.BytesIO(response.content), Inches(5.5), Inches(1.5), width=Inches(3.8))
            except:
                pass # يكمل السلايد بدون صورة إذا حدث خطأ

            # النقاط
            b_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5))
            tf = b_box.text_frame
            tf.word_wrap = True
            for line in lines[1:]:
                if line.strip():
                    lp = tf.add_paragraph()
                    lp.text = "• " + str(line).strip("-*• ")
                    lp.font.size = Pt(18)
                    lp.font.color.rgb = RGBColor(255, 255, 255)

    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()

# 3. واجهة المستخدم والمنطق
st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.divider()

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("Missing API Key in Secrets!")
    st.stop()

client = Groq(api_key=api_key)
topic = st.text_input("Enter your topic:", placeholder="e.g. Modern Lebanon", key="input_main")

if st.button("Generate Premium Slides ✨"):
    if topic:
        with st.spinner("💎 AI is crafting your luxury file..."):
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Create 5 slides about {topic}. Format: Slide X: Title then bullets."}]
                )
                content = res.choices[0].message.content
                st.session_state['file_data'] = create_luxury_pptx(content, topic)
                st.session_state['topic_name'] = topic
                st.session_state['is_ready'] = True
            except Exception as e:
                st.error(f"Error: {e}")

# 4. منطقة التحميل والقفل
if st.session_state.get('is_ready'):
    st.markdown('<div class="unlock-box">', unsafe_allow_html=True)
    st.markdown(f"### 🔒 '{st.session_state['topic_name']}' is Secured")
    st.write("To unlock, send $4 via Whish to 81950506")
    
    # نظام الرمز
    code = st.text_input("Activation Code:", type="password", key="active_code")
    if code == "SWIFT2025":
        st.balloons()
        st.download_button("📥 Download PPTX", st.session_state['file_data'], f"{st.session_state['topic_name']}.pptx")
    
    # رابط الواتساب
    wa_url = f"https://wa.me/96181950506?text=I paid for {st.session_state['topic_name']}"
    st.markdown(f'<a href="{wa_url}" style="color:#25D366; font-weight:bold; text-decoration:none;">Chat with Admin for Code</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

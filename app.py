import streamlit as st
from groq import Groq
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import io
import requests
import urllib.parse

# 1. تصميم الموقع (الواجهة الزرقاء الفخمة)
st.set_page_config(page_title="SwiftSlide AI Premium", page_icon="🚀")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: bold; }
    .unlock-box { background-color: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #007bff; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 2. دالة صناعة البوربوينت الفخم (خلفية سوداء + صور)
def create_luxury_pptx(text_content, topic_name):
    prs = Presentation()
    
    # دالة لجلب صورة من الإنترنت بناءً على الموضوع
    def get_image(query):
        try:
            img_url = f"https://source.unsplash.com/800x600/?{query}"
            response = requests.get(img_url)
            if response.status_code == 200:
                return io.BytesIO(response.content)
        except: return None
        return None

    # سلايد العنوان (خلفية داكنة)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # سلايد فارغ للتصميم المخصص
    # تلوين الخلفية بالأسود
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(14, 17, 23)

    title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(2))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = str(topic_name).upper()
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(0, 212, 255)
    p.alignment = PP_ALIGN.CENTER

    # تقسيم السلايدات
    sections = str(text_content).split("Slide")
    for i, section in enumerate(sections):
        if len(section).strip() > 10:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            # تلوين الخلفية
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = RGBColor(20, 20, 20)
            
            lines = section.strip().split("\n")
            title_text = str(lines[0]).replace(":", "").strip()
            
            # إضافة العنوان
            title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1))
            title_p = title_box.text_frame.add_paragraph()
            title_p.text = title_text
            title_p.font.size = Pt(32)
            title_p.font.color.rgb = RGBColor(0, 212, 255)

            # إضافة صورة فخمة في السلايد (يمين)
            img = get_image(topic_name.split()[0])
            if img:
                slide.shapes.add_picture(img, Inches(5.5), Inches(1.5), width=Inches(4))

            # إضافة النقاط (يسار)
            body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5))
            tf = body_box.text_frame
            tf.word_wrap = True
            for line in lines[1:]:
                clean_line = str(line).strip("-*• ")
                if clean_line:
                    p = tf.add_paragraph()
                    p.text = "• " + clean_line
                    p.font.size = Pt(18)
                    p.font.color.rgb = RGBColor(255, 255, 255)
                    p.space_after = Pt(10)

    binary_io = io.BytesIO()
    prs.save(binary_io)
    return binary_io.getvalue()

# 3. المنطق التشغيلي
ADMIN_UNLOCK_CODE = "SWIFT2025"
MY_PHONE = "96181950506"
WHISH_NUMBER = "81950506"

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.divider()

api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

topic = st.text_input("What is your topic?", placeholder="e.g. Artificial Intelligence in 2025")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner("🎨 AI is generating luxury slides with images..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Create a 5-slide presentation about {topic}. Use 'Slide X: Title' then bullets."}]
                )
                content = response.choices[0].message.content
                # توليد الملف وحفظه
                st.session_state['pptx_file'] = create_luxury_pptx(content, topic)
                st.session_state['topic'] = topic
                st.session_state['done'] = True
                st.success("🎉 Your premium presentation is ready!")
            except Exception as e:
                st.error(f"Error: {e}")

# 4. واجهة القفل
if st.session_state.get('done'):
    st.markdown('<div class="unlock-box">', unsafe_allow_html=True)
    st.markdown(f"### 🔒 The file '{st.session_state['topic']}' is locked")
    st.write(f"Send **$4** to Whish **{WHISH_NUMBER}** to unlock.")
    
    code = st.text_input("Enter Activation Code:", type="password")
    
    if code == ADMIN_UNLOCK_CODE:
        st.balloons()
        st.download_button("📥 Download Premium PPTX", st.session_state['pptx_file'], f"{st.session_state['topic']}.pptx")
    
    whatsapp_url = f"https://wa.me/{MY_PHONE}?text=" + urllib.parse.quote(f"Hi! I paid $4 for {st.session_state['topic']}. Send code!")
    st.markdown(f'<br><a href="{whatsapp_url}" style="color:#25D366; font-weight:bold;">Contact Admin for Activation Code</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #4b5563;'>SwiftSlide AI Lebanon © 2025</p>", unsafe_allow_html=True)

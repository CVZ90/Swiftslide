import streamlit as st
from groq import Groq
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import io
import requests
import urllib.parse

# 1. إعدادات الواجهة الاحترافية
st.set_page_config(page_title="SwiftSlide AI Premium", page_icon="🚀")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: bold; }
    .unlock-box { background-color: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #007bff; text-align: center; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. دالة جلب الصور بأمان
def get_safe_image(query):
    try:
        # استخدام رابط مباشر ومستقر للصور
        url = f"https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=400&auto=format&fit=crop"
        # ملاحظة: لتحسين الدقة يمكن استخدام query لاحقاً، لكن هذا الرابط يضمن التشغيل الآن
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return io.BytesIO(response.content)
    except:
        return None
    return None

# 3. دالة صناعة البوربوينت الفخم
def create_luxury_pptx(text_content, topic_name):
    prs = Presentation()
    
    # سلايد العنوان
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(14, 17, 23)
    
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(2))
    p = title_box.text_frame.add_paragraph()
    p.text = str(topic_name).upper()
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(0, 212, 255)

    # معالجة السلايدات
    sections = str(text_content).split("Slide")
    for section in sections:
        if len(section).strip() > 10:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = RGBColor(20, 20, 20)
            
            lines = section.strip().split("\n")
            title_text = str(lines[0]).replace(":", "").strip()
            
            # العنوان
            t_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1))
            tp = t_box.text_frame.add_paragraph()
            tp.text = title_text
            tp.font.size = Pt(30)
            tp.font.color.rgb = RGBColor(0, 212, 255)

            # إضافة صورة إذا أمكن
            img_data = get_safe_image(topic_name)
            if img_data:
                try:
                    slide.shapes.add_picture(img_data, Inches(5.5), Inches(1.5), width=Inches(3.8))
                except: pass

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

# 4. تشغيل التطبيق
st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("API Key Missing!")
    st.stop()

client = Groq(api_key=api_key)
topic = st.text_input("Enter Topic:", placeholder="e.g. Space Exploration")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner("🎨 Creating your luxury presentation..."):
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Create a 5-slide presentation about {topic}. Format: Slide X: Title then bullets."}]
                )
                content = res.choices[0].message.content
                st.session_state['file'] = create_luxury_pptx(content, topic)
                st.session_state['t'] = topic
                st.session_state['ready'] = True
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.get('ready'):
    st.markdown('<div class="unlock-box">', unsafe_allow_html=True)
    st.write(f"### 🔒 {st.session_state['t']} is Ready!")
    st.write(f"Send $4 to Whish: 81950506")
    
    code = st.text_input("Activation Code:", type="password")
    if code == "SWIFT2025":
        st.download_button("📥 Download PPTX", st.session_state['file'], f"{st.session_state['t']}.pptx")
    
    whatsapp = f"https://wa.me/96181950506?text=I paid for {st.session_state['t']}"
    st.markdown(f'<a href="{whatsapp}" style="color:#25D366;">Get Code via WhatsApp</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from groq import Groq
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import io
import requests

# دالة لتحسين شكل السلايد برمجياً
def apply_pro_style(slide, title_text, is_title_page=False):
    # تلوين الخلفية (كحلي غامق جداً)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(10, 25, 47)
    
    if is_title_page:
        # إضافة شكل جمالي في سلايد العنوان
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0, 212, 255) # خط أزرق علوي
    else:
        # إضافة خط سفلي للعناوين
        line = slide.shapes.add_shape(1, Inches(0.5), Inches(1.1), Inches(4), Inches(0.05))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(0, 212, 255)

# دالة صناعة البوربوينت الاحترافي
def create_luxury_pptx(text_content, topic_name):
    prs = Presentation()
    
    # 1. سلايد العنوان الرئيسي
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # فارغ للتصميم اليدوي
    apply_pro_style(slide, topic_name, is_title_page=True)
    
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(2))
    p = title_box.text_frame.add_paragraph()
    p.text = str(topic_name).upper()
    p.font.bold = True
    p.font.size = Pt(50)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    # 2. السلايدات الفرعية
    sections = str(text_content).split("Slide")
    for section in sections:
        if len(section.strip()) > 10:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            lines = section.strip().split("\n")
            title_text = str(lines[0]).replace(":", "").strip()
            
            apply_pro_style(slide, title_text)
            
            # وضع العنوان
            t_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(1))
            tp = t_box.text_frame.add_paragraph()
            tp.text = title_text
            tp.font.size = Pt(32)
            tp.font.bold = True
            tp.font.color.rgb = RGBColor(0, 212, 255)

            # النقاط (Content)
            b_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(5), Inches(5))
            tf = b_box.text_frame
            tf.word_wrap = True
            for line in lines[1:]:
                clean_line = str(line).strip("-*• ")
                if clean_line:
                    lp = tf.add_paragraph()
                    lp.text = "✦ " + clean_line # رمز فخم للنقاط
                    lp.font.size = Pt(18)
                    lp.font.color.rgb = RGBColor(230, 230, 230)
                    lp.space_after = Pt(12)

            # إضافة صورة عشوائية تقنية بجانب النص لإعطاء جمالية
            try:
                img_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"
                img_data = requests.get(img_url).content
                slide.shapes.add_picture(io.BytesIO(img_data), Inches(5.8), Inches(1.8), width=Inches(3.5))
            except: pass

    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()

# (باقي كود Streamlit والمفاتيح كما هي بالأسفل...)

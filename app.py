import streamlit as st
from pptx import Presentation
import google.generativeai as genai
import io
import urllib.parse

# إعدادات الصفحة
st.set_page_config(page_title="SwiftSlide AI", page_icon="🚀")

# تصميم الواجهة
st.markdown("<h1 style='text-align: center; color: #007bff;'>SwiftSlide AI 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>أسرع طريقة في لبنان لإنشاء عروض PowerPoint احترافية بالذكاء الاصطناعي</p>", unsafe_allow_html=True)

st.divider()

# معلوماتك الشخصية
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 
api_key = "AIzaSyDOx1zkGMZVnxbBcy4WdmwCiI4ArzSVi2M" 

topic = st.text_input("ما هو موضوع العرض المطلوب؟")

if st.button("تجهيز العرض الآن"):
    if topic:
        with st.spinner('جاري تصميم العرض...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                # طلب المحتوى
                prompt = f"Create content for a 5-slide PowerPoint about {topic}. Provide a Title and 3 detailed bullets for each slide."
                response = model.generate_content(prompt)
                
                st.success(f"✅ تم تجهيز عرض '{topic}' بنجاح!")
                
                # رسالة واتساب تلقائية
                whatsapp_msg = f"مرحباً SwiftSlide، لقد قمت بإنشاء عرض حول '{topic}' وأريد فك القفل وتحميله. لقد قمت بتحويل الـ 4$ إلى رقم الـ Whish."
                encoded_msg = urllib.parse.quote(whatsapp_msg)
                whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_msg}"
                
                # واجهة الدفع
                st.warning("🔒 الملف مقفل حالياً")
                st.info(f"للحصول على الملف، يرجى تحويل **4$** إلى رقم الـ Whish: **{WHISH_NUMBER}**")
                
                # زر التحويل للواتساب
                st.markdown(f"""
                    <a href="{whatsapp_url}" target="_blank">
                        <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-size:18px; cursor:pointer;">
                            تواصل معي عبر واتساب لاستلام الملف 💬
                        </button>
                    </a>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("يرجى التأكد من إعداد المفتاح بشكل صحيح.")
    else:
        st.error("يرجى كتابة موضوع أولاً")

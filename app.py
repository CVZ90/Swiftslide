import streamlit as st
from pptx import Presentation
import google.generativeai as genai
import io
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="SwiftSlide AI | Premium", page_icon="🚀", layout="centered")

# 2. Luxury CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text {
        text-align: center;
        background: -webkit-linear-gradient(#00d4ff, #007bff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px; font-weight: bold;
    }
    .whatsapp-btn {
        display: flex; align-items: center; justify-content: center;
        background-color: #25D366; color: white !important;
        padding: 15px; text-decoration: none; border-radius: 15px;
        font-weight: bold; font-size: 18px; margin-top: 20px;
        transition: 0.3s;
    }
    .whatsapp-btn:hover { background-color: #128C7E; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Premium AI Presentations in Seconds</p>", unsafe_allow_html=True)
st.divider()

# 3. Logic & API Setup
MY_PHONE_NUMBER = "96181950506" 
WHISH_NUMBER = "81950506" 

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 Configuration Error: API Key missing in Secrets.")
    st.stop()

# 4. User Input
topic = st.text_input("What is your presentation topic?", placeholder="e.g. Benefits of Solar Energy")

if st.button("Generate Premium Presentation ✨"):
    if topic:
        with st.spinner('AI is crafting your slides...'):
            try:
                genai.configure(api_key=api_key)
                
                # التعديل هنا: استخدام نموذج gemini-1.5-flash الأسرع والأحدث
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Create a detailed 5-slide presentation outline about {topic}. Provide a professional title and 3-4 bullet points for each slide. Language: English."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.balloons()
                    st.success("✅ Presentation Content Generated!")
                    
                    # Display Preview
                    with st.expander("👁️ Preview Slide Content"):
                        st.write(response.text)
                    
                    # Locked Section
                    st.markdown("---")
                    st.markdown("### 🔒 File Status: Locked")
                    st.info(f"To download the PPTX file, please transfer **$4** via Whish Money to: **{WHISH_NUMBER}**")
                    
                    # WhatsApp Integration
                    whatsapp_msg = f"Hello SwiftSlide! I just generated a presentation about '{topic}'. I've sent the $4 via Whish. Please send me the file!"
                    encoded_msg = urllib.parse.quote(whatsapp_msg)
                    whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_msg}"
                    
                    st.markdown(f"""
                        <a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="25" style="margin-right:10px;">
                            Chat with us to Unlock & Download
                        </a>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"⚠️ Technical Error: {str(e)}")
                st.info("Tip: If the error persists, try refreshing the page or checking your API Key quota.")
    else:
        st.warning("Please enter a topic first.")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #4b5563; font-size: 0.8rem;'>SwiftSlide AI Lebanon © 2025</p>", unsafe_allow_html=True)

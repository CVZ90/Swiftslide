import streamlit as st
import google.generativeai as genai
import urllib.parse

# Page Setup
st.set_page_config(page_title="SwiftSlide AI", page_icon="🚀")

# Luxury Style
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: bold; }
    .whatsapp-btn { display: flex; align-items: center; justify-content: center; background-color: #25D366; color: white !important; padding: 15px; text-decoration: none; border-radius: 15px; font-weight: bold; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">SwiftSlide AI 🚀</h1>', unsafe_allow_html=True)
st.divider()

# API Key & Numbers
MY_PHONE_NUMBER = "96181950506"
WHISH_NUMBER = "81950506"
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key is missing!")
    st.stop()

topic = st.text_input("Enter topic:", placeholder="e.g. History of Lebanon")

if st.button("Generate Presentation ✨"):
    if topic:
        with st.spinner('Accessing AI Models...'):
            try:
                genai.configure(api_key=api_key)
                
                # مصفوفة النماذج لتجربة المتوفر منها تلقائياً
                model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                response = None
                
                for m_name in model_names:
                    try:
                        model = genai.GenerativeModel(m_name)
                        response = model.generate_content(f"Create a 5-slide outline about {topic}. Title and 3 bullets per slide.")
                        if response: break
                    except:
                        continue

                if response and response.text:
                    st.balloons()
                    st.success("✅ Content Ready!")
                    with st.expander("Preview Content"):
                        st.write(response.text)
                    
                    st.info(f"💳 Transfer $4 to Whish: {WHISH_NUMBER}")
                    
                    msg = urllib.parse.quote(f"Hello! I generated a slide about {topic}. I sent $4 to {WHISH_NUMBER}. Unlock please!")
                    st.markdown(f'<a href="https://wa.me/{MY_PHONE_NUMBER}?text={msg}" class="whatsapp-btn">Chat to Unlock & Download</a>', unsafe_allow_html=True)
                else:
                    st.error("All AI models are currently unavailable. Please check your API Key status at Google AI Studio.")
            
            except Exception as e:
                st.error(f"Technical Error: {str(e)}")
    else:
        st.warning("Please enter a topic.")

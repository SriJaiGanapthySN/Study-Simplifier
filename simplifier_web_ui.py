import os
import base64
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables safely
load_dotenv()

# Map the .env keys to GOOGLE_API_KEY
if "GEMINI_API_KEY3" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY3"]
elif "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

def get_base64_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

@st.cache_resource
def get_llm():
    """Initializes and caches the Gemini model."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.3,
    )

def simplify_content(llm, text_input=None, image_bytes=None, grade_level="Middle School"):
    """Handles multimodal simplification logic."""
    system_prompt = (
        "You are an expert educator, mentor, and simplifier. "
        "Your primary goal is to take complex concepts, dense content, or difficult study questions, "
        "and explain them in simple, easy-to-understand language tailored for a {grade_level} student.\n\n"
        "Rules:\n"
        "1. Never lose the original core meaning or factual accuracy.\n"
        "2. Break down hard words and offer clear, relatable everyday analogies.\n"
        "3. Use structured formatting like bullet points and short paragraphs to enhance readability.\n"
        "4. If answering a study question, give a direct, simple answer followed by the exact 'why' (using easy language).\n"
        "5. Keep the tone encouraging, helpful, and highly accessible.\n"
        "6. Adjust your vocabulary and complexity to perfectly match the {grade_level} level."
    ).format(grade_level=grade_level)

    content = []
    if text_input:
        content.append({"type": "text", "text": f"Please answer or simplify this: {text_input}"})
    
    if image_bytes:
        base64_image = get_base64_image(image_bytes)
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })
        if not text_input:
            content.append({"type": "text", "text": "Please analyze this image and simplify any educational content or questions found within it."})

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=content)
    ]
    
    return llm.invoke(messages).content

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }

        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }

        /* Glassmorphism containers */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
            border: none;
            color: white;
        }

        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #f1f5f9 !important;
            border-radius: 12px !important;
        }

        .stSelectbox div[data-baseweb="select"] {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }

        .stFileUploader section {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 2px dashed rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
        }

        .result-card {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        h1, h2, h3 {
            color: #ffffff;
            font-weight: 700;
        }

        .sidebar .sidebar-content {
            background: rgba(15, 23, 42, 0.95);
        }

        /* Gradient Text */
        .gradient-text {
            background: linear-gradient(90deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fadeIn 0.8s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Study Simplifier", 
        page_icon="🧠", 
        layout="wide"
    )
    
    apply_custom_css()

    # Sidebar for settings
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/brain--v1.png", width=80)
        st.markdown("<h2 class='gradient-text'>Study Simplifier</h2>", unsafe_allow_html=True)
        st.divider()
        st.subheader("Global Settings")
        grade_level = st.selectbox(
            "Target Audience",
            ["Elementary School (Grade 1-5)", "Middle School (Grade 6-8)", "High School (Grade 9-12)", "College/University", "Expert/Professional"],
            index=2
        )
        st.info(f"The AI will explain concepts specifically for **{grade_level}** levels.")
        
        st.divider()
        st.caption("Powered by Gemini 1.5 Flash")

    # Header Area
    st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'><span class='gradient-text'>Study Simplifier</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #94a3b8; margin-bottom: 2rem;'>Master any topic with AI-powered simplification. Paste text, upload documents, or share a photo.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # API Key Validation
    if "GOOGLE_API_KEY" not in os.environ:
        st.error("Missing Gemini API Key. Please add `GEMINI_API_KEY` to your .env file.")
        st.stop()

    try:
        llm = get_llm()
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")
        st.stop()

    # Main Input Layout
    input_col, preview_col = st.columns([1, 1], gap="large")

    with input_col:
        st.markdown("### Input Sources")
        
        tabs = st.tabs([" Text", " Document", " Photo"])
        
        final_text = ""
        final_image = None
        
        with tabs[0]:
            user_text = st.text_area(
                "Paste complex paragraphs or questions:", 
                height=250, 
                placeholder="E.g. Explain the theory of relativity in simple terms..."
            )
            if user_text:
                final_text = user_text

        with tabs[1]:
            uploaded_doc = st.file_uploader("Upload .txt or .md files", type=["txt", "md"])
            if uploaded_doc:
                file_content = uploaded_doc.read().decode("utf-8")
                st.success(f"Loaded: {uploaded_doc.name}")
                final_text = file_content if not final_text else final_text + "\n\n" + file_content

        with tabs[2]:
            uploaded_photo = st.file_uploader("Upload a photo of your notes or textbook", type=["jpg", "jpeg", "png"])
            if uploaded_photo:
                final_image = uploaded_photo.read()
                st.image(final_image, caption="Uploaded Preview", use_container_width=True)

    with preview_col:
        st.markdown("### Actions")
        st.write("Click the button below to start the magic. Our AI will analyze your input and create a beautifully structured explanation.")
        
        if st.button("Simplify Now", use_container_width=True):
            if not final_text and not final_image:
                st.warning("Please provide some text or an image to simplify.")
            else:
                with st.spinner(f"Magic in progress for {grade_level}..."):
                    try:
                        response = simplify_content(
                            llm=llm,
                            text_input=final_text,
                            image_bytes=final_image,
                            grade_level=grade_level
                        )
                        
                        st.markdown(f"""
                        <div class="result-card animate-fade-in">
                            <h3 class='gradient-text'>Analysis Result</h3>
                            <p style='color: #cbd5e1; font-size: 0.9rem;'>Target: {grade_level}</p>
                            <hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 1rem 0;'>
                            <div style='color: #f1f5f9; line-height: 1.6;'>
                                {response}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Also provide it in standard markdown for better rendering of bullet points if needed
                        with st.expander("Copyable Version"):
                            st.write(response)
                            
                    except Exception as e:
                        st.error(f"Generation failed: {str(e)}")

if __name__ == "__main__":
    main()

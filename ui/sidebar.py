import streamlit as st
from utils.pdf_extractor import extract_text_from_pdf, extract_text_from_txt

def render_sidebar(question_collector):
    """Render the sidebar UI"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/resume.png", width=100)
        st.markdown("### 📎 Your Resume")
        
        # File upload
        uploaded_file = st.file_uploader("Upload Resume (PDF or TXT)", type=['pdf', 'txt'])
        
        if uploaded_file:
            with st.spinner("Reading resume..."):
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                else:
                    resume_text = extract_text_from_txt(uploaded_file)
                
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.markdown('<div class="success-box">✅ Resume loaded successfully!</div>', 
                               unsafe_allow_html=True)
                    
                    with st.expander("📄 Preview"):
                        st.text(resume_text[:300] + "..." if len(resume_text) > 300 else resume_text)
        
        # Manual input option
        with st.expander("✏️ Or paste your resume"):
            manual_resume = st.text_area("Paste your resume here", height=200)
            if manual_resume:
                st.session_state.resume_text = manual_resume
                st.markdown('<div class="success-box">✅ Resume saved!</div>', 
                           unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Agent information
        st.markdown("### 🤖 Your 3 Agents")
        
        agents_info = [
            ("1️⃣ Resume Reviewer", "Get expert feedback to improve your resume"),
            ("2️⃣ Cover Letter Writer", "Generate customized cover letters"),
            ("3️⃣ Interview Coach", "Practice with real interview questions")
        ]
        
        for title, desc in agents_info:
            with st.container():
                st.markdown(f"**{title}**")
                st.caption(desc)
        
        st.markdown("---")
        
        # Stats
        st.markdown("### 📊 Stats")
        total_q = question_collector.get_total_questions_count()
        st.metric("Questions in Database", f"{total_q}+")
        
        if 'resume_text' in st.session_state and st.session_state.resume_text:
            st.metric("Resume Status", "Loaded ✓")
import streamlit as st
from datetime import datetime

def render_resume_tab(agent):
    """Render the resume reviewer tab"""
    st.markdown("### 🔍 Agent 1: Resume Reviewer")
    st.caption("Get expert feedback to make your resume stand out")
    
    if not st.session_state.get('resume_text'):
        st.markdown('<div class="warning-box">👆 Please upload your resume in the sidebar first</div>', 
                   unsafe_allow_html=True)
        return
    
    job_target = st.text_input("🎯 Target Job Title (optional)", 
                               placeholder="e.g., Software Engineer, Product Manager")
    
    if st.button("🚀 Review My Resume", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing your resume..."):
            review = agent.review(st.session_state.resume_text, job_target)
            
            st.markdown("### 📊 Resume Review Results")
            st.markdown(review)
            
            # Download button
            st.download_button(
                "📥 Download Review",
                review,
                file_name=f"resume_review_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/markdown"
            )
    
    # Tips section
    with st.expander("💡 Resume Tips"):
        st.markdown("""
        **Quick Checklist:**
        - ✅ Use strong action verbs (led, created, improved, achieved)
        - ✅ Quantify achievements with numbers (increased sales by 20%)
        - ✅ Include keywords from job descriptions
        - ✅ Keep formatting simple and ATS-friendly
        - ✅ Proofread for errors
        - ✅ Keep it to 1-2 pages
        """)
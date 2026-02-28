import streamlit as st
from datetime import datetime

def render_cover_letter_tab(agent):
    """Render the cover letter writer tab"""
    st.markdown("### ✍️ Agent 2: Cover Letter Writer")
    st.caption("Generate customized cover letters in seconds")
    
    if not st.session_state.get('resume_text'):
        st.markdown('<div class="warning-box">👆 Please upload your resume in the sidebar first</div>', 
                   unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("📋 Job Title*", placeholder="e.g., Product Manager")
        company = st.text_input("🏢 Company Name*", placeholder="e.g., Google")
        tone = st.selectbox("🎭 Tone", ["professional", "enthusiastic", "creative", "executive"])
    
    with col2:
        job_desc = st.text_area("📝 Job Description*", 
                               placeholder="Paste the job description here...", 
                               height=150)
    
    if st.button("✍️ Generate Cover Letter", type="primary", use_container_width=True):
        if job_title and company and job_desc:
            with st.spinner("Writing your custom cover letter..."):
                letter = agent.write(
                    st.session_state.resume_text,
                    job_title,
                    company,
                    job_desc,
                    tone
                )
                
                st.markdown("### 📝 Your Cover Letter")
                st.markdown(letter)
                
                # Download button
                st.download_button(
                    "📥 Download Cover Letter",
                    letter,
                    file_name=f"cover_letter_{company}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please fill all required fields (*)")
    
    # Template section
    with st.expander("📋 Cover Letter Template Tips"):
        st.markdown("""
        **A good cover letter includes:**
        1. **Opening** - Express interest and mention the role
        2. **Body Paragraph 1** - Why you're qualified (skills match)
        3. **Body Paragraph 2** - Your achievements and impact
        4. **Closing** - Enthusiasm and call to action
        """)
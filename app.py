import streamlit as st
from config import check_api_key, APP_NAME, APP_ICON, APP_LAYOUT
from agents import ResumeReviewerAgent, CoverLetterWriterAgent, InterviewCoachAgent
from utils.question_collector import InterviewQuestionCollector
from ui import apply_custom_styles, header, footer, render_sidebar
from ui.tabs import render_resume_tab, render_cover_letter_tab, render_interview_tab

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=APP_LAYOUT
)

# Apply custom styles
apply_custom_styles()

# Display header
header()

# Check API key
if not check_api_key():
    st.error("⚠️ OpenRouter API Key not found!")
    st.info("""
    Please add your OpenRouter API key to the `.env` file:
    1. Get a free key at: https://openrouter.ai/keys
    2. Add to .env: `OPENROUTER_API_KEY=your_key_here`
    """)
    st.stop()

# Initialize session state
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""

# Initialize components
@st.cache_resource
def init_components():
    """Initialize all agents and collectors (cached)"""
    question_collector = InterviewQuestionCollector()
    resume_agent = ResumeReviewerAgent()
    cover_letter_agent = CoverLetterWriterAgent()
    interview_agent = InterviewCoachAgent()
    
    return {
        'question_collector': question_collector,
        'resume_agent': resume_agent,
        'cover_letter_agent': cover_letter_agent,
        'interview_agent': interview_agent
    }

# Load components
components = init_components()

# Render sidebar
render_sidebar(components['question_collector'])

# Main content with tabs
tab1, tab2, tab3 = st.tabs([
    "🔍 Resume Reviewer", 
    "✍️ Cover Letter Writer", 
    "🎤 Interview Coach"
])

with tab1:
    render_resume_tab(components['resume_agent'])

with tab2:
    render_cover_letter_tab(components['cover_letter_agent'])

with tab3:
    render_interview_tab(components['interview_agent'], components['question_collector'])

# Footer
footer()
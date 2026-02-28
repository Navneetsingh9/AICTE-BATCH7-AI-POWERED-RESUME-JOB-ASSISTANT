import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton button {
        width: 100%;
        border-radius: 20px;
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #2980b9;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .question-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #27ae60;
        margin: 10px 0;
    }
    .agent-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def header():
    """Display app header"""
    st.markdown("""
    <div class="main-header">
        <h1>📄 AI Resume & Job Assistant</h1>
        <p>AI-powered resume analysis, interview prep & personalized cover letters</p>
        <p>🤖 3 AI Agents • 🎯 Smart Insights • 💼 Job-Ready Outputs</p>
    </div>
    """, unsafe_allow_html=True)

def footer():
    """Display app footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>📄 AI Resume & Job Assistant | Powered by OpenRouter + Community Interview Questions</p>
        <p>Made with ❤️ for Job Seekers</p>
    </div>
    """, unsafe_allow_html=True)
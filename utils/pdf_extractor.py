import PyPDF2
import streamlit as st

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF resume"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_txt(txt_file):
    """Extract text from uploaded text file"""
    try:
        return txt_file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading text file: {str(e)}")
        return None
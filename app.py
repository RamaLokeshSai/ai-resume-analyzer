import streamlit as st
import os
import fitz
import google.generativeai as genai
from dotenv import load_dotenv
import re

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    api_key = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("📄 AI Resume Analyzer")

st.sidebar.write(
    """
    Analyze resumes using AI.

    Features:
    - ATS Score
    - Resume Review
    - Job Description Matching
    - Missing Skills Detection
    """
)

# =========================
# MAIN TITLE
# =========================

st.title("🚀 AI Resume Analyzer")

st.write(
    "Upload your resume and compare it against a job description using AI."
)

st.divider()

# =========================
# FILE UPLOAD
# =========================

st.header("📤 Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your Resume PDF",
    type=["pdf"]
)

# =========================
# JOB DESCRIPTION INPUT
# =========================

st.header("📝 Paste Job Description")

job_description = st.text_area(
    "Paste the Job Description here",
    height=200
)

st.divider()

# =========================
# PROCESS RESUME
# =========================

if uploaded_file is not None:

    # Create uploads folder
    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Save uploaded file
    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Resume uploaded successfully!")

    # =========================
    # EXTRACT TEXT FROM PDF
    # =========================

    doc = fitz.open(file_path)

    resume_text = ""

    for page in doc:
        resume_text += page.get_text()

    # =========================
    # SHOW EXTRACTED TEXT
    # =========================

    with st.expander("📄 View Extracted Resume Text"):
        st.write(resume_text[:3000])

    # =========================
    # ANALYZE BUTTON
    # =========================

    if st.button("🔍 Analyze Resume"):

        with st.spinner("🤖 AI is analyzing your resume..."):

            prompt = f"""
            You are an expert ATS resume reviewer.

            Compare the resume with the job description.

            Give response in the following format:

            ATS Match Score: <score>/100

            Matching Skills:
            - point
            - point

            Missing Skills:
            - point
            - point

            Resume Strengths:
            - point
            - point

            Improvement Suggestions:
            - point
            - point

            Resume:
            {resume_text}

            Job Description:
            {job_description}
            """

            response = model.generate_content(prompt)

            ai_feedback = response.text

        # =========================
        # DISPLAY RESULTS
        # =========================
        match = re.search(r'(\d+)/100', ai_feedback)

        if match:
            ats_score = int(match.group(1))

            st.subheader("📊 ATS Match Score")

            st.metric(label="ATS Score", value=f"{ats_score}/100")

            st.progress(ats_score)
        st.success("✅ Resume analysis completed!")

        st.divider()

        st.header("📊 AI Analysis Result")

        st.write(ai_feedback)
import streamlit as st
import pandas as pd
from agent import run_agent

if "contents" not in st.session_state:
    st.session_state.contents = []

st.write("# Resume IQ")

st.write("""Welcome to Resume IQ! This app uses Gemini 2.5 to analyze your resume 
        and provide feedback on how to improve it for a specific job description. 
        To get started, upload your resume as a PDF file and 
        the job description. Then, click the 
        button below to see the analysis.""")

job_desc = st.text_input("Enter the job description here:")
if job_desc:
    with open("data/job_desc.txt", "w") as f:
        f.write(job_desc)
    st.write("Job description received. You can now upload your resume.")

resume = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
if resume:
    with open("data/" + resume.name, "wb") as f:
        f.write(resume.getbuffer())
    st.success("Resume uploaded successfully!")

if job_desc and resume:
    st.write("Great! You can now click the button below to analyze your resume.")
    if st.button("Analyze Resume"):
        st.write("Analyzing your resume... This may take a few moments.")
        # Call the agent function here to perform the analysis
        # You can display the results in a user-friendly format using Streamlit components
        with open("data/job_desc.txt", "r") as f:
            job_desc_content = f.read()
        with st.spinner("Analyzing your resume..."):
            result = run_agent("Analyze my resume for this job description: " + job_desc_content, st.session_state.contents)
        st.session_state.result = result

if "result" in st.session_state:
    st.markdown(st.session_state.result)
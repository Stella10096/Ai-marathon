import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load system configurations
load_dotenv()

# 2. Initialize the Chutes Client
client = OpenAI(
    api_key=os.getenv("CHUTES_API_KEY"),
    base_url=os.getenv("CHUTES_BASE_URL")
)

def get_ai_evaluation(job_desc, resume_text):
    system_prompt = (
        "You are an expert HR recruitment specialist. Your job is to analyze the given candidate resume "
        "against the job description. Provide an objective suitability score out of 100, list matching skills, "
        "and point out missing skills in a clear professional format."
    )
    user_content = f"=== JOB DESCRIPTION ===\n{job_desc}\n\n=== CANDIDATE RESUME ===\n{resume_text}"
    
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct-TEE",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    )
    return response.choices[0].message.content

# 3. Streamlit Web UI Layout Setup
st.set_page_config(page_title="AI Intelligent Recruiter", layout="wide")

st.title("AI Intelligent Recruiter Agent")
st.subheader("Hackathon Prototype for AI Marathon 2026")
st.write("Input the job requirement and resume below to get instant AI matching results.")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Job Description")
    job_input = st.text_area(
        "Paste the Job Requirement here:",
        height=250,
        placeholder="e.g., Looking for a Data Analyst proficient in SQL, Python, and Git..."
    )

with col2:
    st.markdown("### 📄 Candidate Resume")
    resume_input = st.text_area(
        "Paste the Candidate Resume here:",
        height=250,
        placeholder="e.g., Name: John Doe. Skills: Advanced Python, SQL queries, GitHub version control..."
    )

st.markdown("---")

# Submit Button
if st.button("🚀 Start Intelligent Matching", type="primary"):
    if not job_input or not resume_input:
        st.warning("Please fill in both the Job Description and the Candidate Resume!")
    else:
        with st.spinner("AI Agent is scanning and analyzing the profiles... Please wait."):
            # Call AI Function
            result = get_ai_evaluation(job_input, resume_input)
            
            # Display Result
            st.success("Analysis Completed successfully!")
            st.markdown("### 📊 AI Evaluation Report")
            st.info(result)
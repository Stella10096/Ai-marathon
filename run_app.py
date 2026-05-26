import os
import sys
import json
import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="4-bits IR", layout="wide")

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
import chutes


if "page_router" not in st.session_state:
    st.session_state.page_router = "landing"

if "pipeline_records" not in st.session_state:
    st.session_state.pipeline_records = None


st.markdown("""
<style>
* {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif !important;
}

.stApp {
    background: #080A12 !important;
    color: #E2E8F0 !important;
}

.block-container {
    max-width: 1480px !important;
    padding-top: 1.2rem !important;
}

button[kind="secondary"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #94A3B8 !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0 !important;
}

button[kind="secondary"]:hover {
    color: #22D3EE !important;
}

div[data-testid="column"]:nth-child(1) button[kind="secondary"] {
    font-weight: 900 !important;
    font-size: 1.6rem !important;
    color: #22D3EE !important;
    letter-spacing: 2px !important;
}

button[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, #0EA5E9 0%, #8B5CF6 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    border-radius: 12px !important;
}

.cyber-title {
    font-size: 4rem;
    font-weight: 900;
    line-height: 1.1;
    background: linear-gradient(90deg, #38BDF8 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-top: 5vh;
    margin-bottom: 1.5rem;
}

.cyber-subtitle {
    color: #94A3B8;
    text-align: center;
    font-size: 1.2rem;
    max-width: 650px;
    margin: 0 auto 3rem auto;
}

.landing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 50vh;
}

.glass-card-node {
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 1.75rem;
    backdrop-filter: blur(20px);
    height: 100%;
}

.command-title {
    text-align: center;
    font-size: 3.3rem;
    font-weight: 950;
    letter-spacing: 1.5px;
    margin-top: 0.8rem;
    margin-bottom: 0.6rem;
    background: linear-gradient(90deg, #38BDF8 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.command-subtitle {
    text-align: center;
    color: #CBD5E1;
    font-size: 1.05rem;
    margin-bottom: 3.4rem;
}

.st-key-job_panel {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.68), rgba(15, 10, 31, 0.88));
    border: 1px solid rgba(6, 182, 212, 0.35);
    border-radius: 18px;
    padding: 2.2rem 2.25rem 2.5rem 2.25rem;
    min-height: 690px;
    box-shadow: 0 0 32px rgba(6, 182, 212, 0.08);
}

.st-key-upload_panel {
    background: linear-gradient(180deg, rgba(25, 11, 43, 0.78), rgba(15, 10, 31, 0.92));
    border: 1px solid rgba(147, 51, 234, 0.45);
    border-radius: 18px;
    padding: 2.2rem 2.25rem 2.5rem 2.25rem;
    min-height: 690px;
    box-shadow: 0 0 36px rgba(168, 85, 247, 0.12);
}

.panel-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 1.8rem;
}

.job-icon {
    width: 45px;
    height: 45px;
    border-radius: 12px;
    background: linear-gradient(135deg, #06B6D4, #2563EB);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    box-shadow: 0 0 24px rgba(6, 182, 212, 0.48);
}

.upload-icon {
    width: 45px;
    height: 45px;
    border-radius: 12px;
    background: linear-gradient(135deg, #A855F7, #EC4899);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    box-shadow: 0 0 24px rgba(217, 70, 239, 0.48);
}

.job-heading {
    font-size: 1.7rem;
    font-weight: 900;
    color: #22D3EE;
}

.upload-heading {
    font-size: 1.7rem;
    font-weight: 900;
    color: #C084FC;
}

label {
    color: #A1AAB8 !important;
    font-weight: 800 !important;
    font-size: 0.92rem !important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: rgba(3, 7, 18, 0.78) !important;
    border: 1px solid rgba(6, 182, 212, 0.60) !important;
    border-bottom: 1px solid rgba(6, 182, 212, 0.95) !important;
    border-radius: 11px !important;
    color: #F8FAFC !important;
    min-height: 55px !important;
    box-shadow: none !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #22D3EE !important;
    box-shadow: 0 0 0 1px rgba(34, 211, 238, 0.32) !important;
}

.stTextArea textarea {
    min-height: 190px !important;
    padding-top: 15px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748B !important;
}

/* Upload panel */
div[data-testid="stFileUploader"] label {
    display: none !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: 2px dashed rgba(147, 51, 234, 0.72) !important;
    border-radius: 16px !important;
    min-height: 285px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p {
    display: none !important;
}

[data-testid="stFileUploaderDropzone"] button {
    font-size: 0 !important;
    color: transparent !important;
    background: transparent !important;
    border: 1px solid rgba(167, 139, 250, 0.75) !important;
    border-radius: 10px !important;
    width: 130px !important;
    height: 48px !important;
}

[data-testid="stFileUploaderDropzone"] button::before {
    content: "Upload";
    font-size: 1rem !important;
    color: #E9D5FF !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploaderDropzone"] button::after {
    content: none !important;
}

.upload-ready {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #CBD5E1;
    font-size: 0.95rem;
    margin-top: 1.4rem;
}

.green-dot {
    width: 10px;
    height: 10px;
    background: #10B981;
    border-radius: 999px;
}

.requirement-badge {
    margin-top: 1rem;
    display: inline-block;
    background: #10B981;
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-size: 0.92rem;
    font-weight: 800;
}

div[data-testid="stExpander"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


def extract_pdf_content(file_asset):
    try:
        reader = PdfReader(file_asset)
        text_output = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_output += text + "\\n"
        return text_output
    except Exception as e:
        st.error(f"PDF extraction failed: {e}")
        return ""


# Navbar
st.markdown("<br>", unsafe_allow_html=True)
nav_c1, nav_spacer, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([1.5, 4.5, 1, 1, 1, 1])

with nav_c1:
    if st.button("4-bits", use_container_width=True):
        st.session_state.page_router = "landing"
        st.rerun()

with nav_c2:
    if st.button("Home", use_container_width=True):
        st.session_state.page_router = "landing"
        st.rerun()

with nav_c3:
    if st.button("Features", use_container_width=True):
        st.session_state.page_router = "inputs"
        st.rerun()

with nav_c4:
    st.button("Technology", use_container_width=True)

with nav_c5:
    st.button("Contact", use_container_width=True)

st.markdown('<hr style="border-color:#1E293B;margin-top:0.5rem;margin-bottom:2rem;">', unsafe_allow_html=True)


if st.session_state.page_router == "landing":

    st.markdown("""
        <div class="landing-container">
            <div class="cyber-title">THE INTELLIGENT<br>RECRUITER</div>
            <div class="cyber-subtitle">AI-powered talent intelligence system for next-generation hiring</div>
        </div>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([2.2, 1.2, 2.2])
    with center_col:
        if st.button("START SCREENING", type="primary", use_container_width=True):
            st.session_state.page_router = "inputs"
            st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Core Engineering Foundations")

    f_c1, f_c2, f_c3 = st.columns(3)

    with f_c1:
        st.markdown("""
        <div class="glass-card-node">
            <div style="font-size:1.8rem;">⚡</div>
            <h4 style="color:white;">Fast Performance</h4>
            <p style="color:#94A3B8;">Optimized architecture with modern frontend technologies and cloud-native deployment.</p>
        </div>
        """, unsafe_allow_html=True)

    with f_c2:
        st.markdown("""
        <div class="glass-card-node">
            <div style="font-size:1.8rem;">🤖</div>
            <h4 style="color:white;">AI Automation</h4>
            <p style="color:#94A3B8;">Integrate intelligent workflows and automation into your business enterprise systems.</p>
        </div>
        """, unsafe_allow_html=True)

    with f_c3:
        st.markdown("""
        <div class="glass-card-node">
            <div style="font-size:1.8rem;">☁️</div>
            <h4 style="color:white;">Cloud Infrastructure</h4>
            <p style="color:#94A3B8;">Deploy scalable applications safely using modern DevOps and secure cloud environments.</p>
        </div>
        """, unsafe_allow_html=True)


elif st.session_state.page_router == "inputs":

    st.markdown("""
        <div class="command-title">AI SCREENING COMMAND CENTER</div>
        <div class="command-subtitle">Configure job requirements and upload candidate resumes</div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        with st.container(key="job_panel"):
            st.markdown("""
                <div class="panel-header">
                    <div class="job-icon">✧</div>
                    <div class="job-heading">Job Requirements</div>
                </div>
            """, unsafe_allow_html=True)

            job_title = st.text_input(
                "Position Title",
                placeholder="e.g., Senior Full Stack Engineer"
            )

            job_skills = st.text_input(
                "Required Skills",
                placeholder="e.g., React, Node.js, TypeScript"
            )

            experience_level = st.selectbox(
                "Experience Level",
                [
                    "Select experience level",
                    "Internship / Entry Level",
                    "Junior",
                    "Mid-Level",
                    "Senior",
                    "Lead / Principal"
                ]
            )

            preferred_technologies = st.text_input(
                "Preferred Technologies",
                placeholder="e.g., AWS, Docker, PostgreSQL"
            )

            job_description = st.text_area(
                "Job Description",
                placeholder="Detailed job description and responsibilities...",
                height=190
            )

    with col_right:
        with st.container(key="upload_panel"):
            st.markdown("""
                <div class="panel-header">
                    <div class="upload-icon">⇧</div>
                    <div class="upload-heading">Upload Resumes</div>
                </div>
            """, unsafe_allow_html=True)

            uploaded_files = st.file_uploader(
                "",
                type=["pdf", "docx"],
                accept_multiple_files=True,
                label_visibility="collapsed"
            )

            st.markdown("""
                <div class="upload-ready">
                    <div class="green-dot"></div>
                    <div>Ready to upload</div>
                </div>

                <div class="requirement-badge">
                    Requirement: PDF or DOCX files only
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("START PROJECT 🚀", type="primary", use_container_width=True):
        if (
            not job_title
            or not job_skills
            or experience_level == "Select experience level"
            or not preferred_technologies
            or not job_description
            or not uploaded_files
        ):
            st.warning("Validation Error: Please complete all job requirement fields and upload candidate files.")
        else:
            full_job_requirements = f"""
Position Title: {job_title}
Required Skills: {job_skills}
Experience Level: {experience_level}
Preferred Technologies: {preferred_technologies}
Job Description: {job_description}
"""

            runtime_cache = {}
            total_items = len(uploaded_files)
            progress_indicator = st.progress(0)

            for idx, item in enumerate(uploaded_files):
                c_name = item.name.rsplit(".", 1)[0]
                st.toast(f"Processing candidate array data stream: {c_name}")

                extracted_text = extract_pdf_content(item)

                ai_payload_json = chutes.analyze_candidate_resume(
                    job_title,
                    full_job_requirements,
                    c_name,
                    extracted_text
                )

                if isinstance(ai_payload_json, str):
                    try:
                        ai_payload_json = json.loads(ai_payload_json)
                    except json.JSONDecodeError:
                        ai_payload_json = {
                            "score": 0,
                            "qualified": ai_payload_json,
                            "languages": "N/A",
                            "competitions": "N/A",
                            "weaknesses": "Invalid AI JSON response.",
                            "interview_questions": []
                        }

                runtime_cache[c_name] = ai_payload_json
                progress_indicator.progress((idx + 1) / total_items)

            st.session_state.pipeline_records = runtime_cache
            st.session_state.page_router = "results"
            st.rerun()


elif st.session_state.page_router == "results":

    st.markdown("## 🏆 Analytical Pipeline Leaderboard Matrix")

    if st.button("↩️ RUN NEW EVALUATION", type="primary", use_container_width=True):
        st.session_state.page_router = "inputs"
        st.session_state.pipeline_records = None
        st.rerun()

    st.markdown("---")

    dataset = st.session_state.pipeline_records

    if not dataset:
        st.info("No functional evaluation records discovered in cache.")
    else:
        for name, data in dataset.items():
            try:
                score_val = int(data.get("score", 0))
            except Exception:
                score_val = 0

            score_val = max(0, min(score_val, 100))

            ui_color = "#10B981" if score_val >= 80 else ("#F59E0B" if score_val >= 60 else "#EF4444")
            tag = "Highly Recommended" if score_val >= 80 else ("Shortlisted Variant" if score_val >= 60 else "Profile Deficient")

            with st.expander(f"👤 {name.upper()} — Match Rating Score: {score_val}/100 ({tag})"):
                left_panel, right_panel = st.columns([1.5, 2.5])

                with left_panel:
                    st.markdown("#### 📊 Suitability Rating Gauge")
                    st.markdown(f"""
                    <div style="background-color:#0F172A;border:1px solid #1E293B;padding:1.5rem;border-radius:8px;text-align:center;">
                        <div style="font-size:2.8rem;font-weight:800;color:{ui_color};">
                            {score_val} <span style="font-size:1rem;color:#475569;">/ 100</span>
                        </div>
                        <div style="background-color:#334155;border-radius:10px;height:10px;width:100%;margin:1.2rem 0;overflow:hidden;">
                            <div style="background:linear-gradient(90deg,#22D3EE,{ui_color});width:{score_val}%;height:100%;border-radius:10px;"></div>
                        </div>
                        <div style="font-size:0.8rem;color:#64748B;font-weight:bold;">MATCH COMPLIANCE SPEED RANGE</div>
                    </div>
                    """, unsafe_allow_html=True)

                with right_panel:
                    st.markdown("#### 🎯 Structural Evaluation Insights")
                    t1, t2, t3 = st.tabs([
                        "Compliance Overview",
                        "Vulnerabilities & Weaknesses",
                        "Generated Interview Scripts"
                    ])

                    with t1:
                        st.markdown(f"**🟢 Qualifications Summary:**\\n{data.get('qualified')}")
                        st.markdown(f"**💻 Identified Language Architecture:**\\n`{data.get('languages')}`")
                        st.markdown(f"**🏆 Competition Benchmarks & Active Repo Records:**\\n{data.get('competitions')}")

                    with t2:
                        st.markdown(f"**🔴 Technical Weaknesses & Missing Stacks:**\\n{data.get('weaknesses')}")

                    with t3:
                        st.markdown("**🤖 AI Automated Target Interview Questions:**")
                        for q_idx, q_text in enumerate(data.get("interview_questions", [])):
                            st.info(f"**Question {q_idx + 1}:** {q_text}")


st.markdown('<br><br><hr style="border-color:#1E293B;">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:#555555;font-size:0.8rem;padding-bottom:1rem;">'
    '© 2026 Intelligent Recruiter Project Inc. All rights reserved.</div>',
    unsafe_allow_html=True
)
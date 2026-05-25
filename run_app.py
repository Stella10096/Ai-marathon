import os
import streamlit as st
from pypdf import PdfReader

# Ensure internal custom packages can be resolved smoothly
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from lib import chutes

# 1. Global Multi-Page Router Cache Memory Configuration
if "page_router" not in st.session_state:
    st.session_state.page_router = "landing"
if "pipeline_records" not in st.session_state:
    st.session_state.pipeline_records = None

# 2. Force Lock Figma Dark Cyber Theme Styles globally via CSS Injection
st.set_page_config(page_title="NEXORA IR", layout="wide")

st.markdown("""
    <style>
        /* Base global dark theme layout configuration */
        .stApp {
            background-color: #0B0F19 !important;
            color: #E2E8F0 !important;
        }
        /* Custom Glowing Title Accent matching your Figma cyber design */
        .cyber-title {
            font-size: 4rem;
            font-weight: 900;
            line-height: 1.1;
            background: linear-gradient(135deg, #22D3EE 0%, #3B82F6 50%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-top: 5vh;
            margin-bottom: 1.5rem;
            letter-spacing: -1px;
        }
        .cyber-subtitle {
            color: #94A3B8;
            text-align: center;
            font-size: 1.2rem;
            max-width: 650px;
            margin: 0 auto 3rem auto;
            line-height: 1.6;
        }
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 50vh;
        }
        div[data-testid="stExpander"] {
            background-color: #1E293B !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
        }
        /* Glass card styling for core engineering foundations matrix */
        .glass-card-node {
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.04);
            border-radius: 16px;
            padding: 1.75rem;
            backdrop-filter: blur(20px);
            height: 100%;
            transition: border-color 0.3s ease;
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
                text_output += text + "\n"
        return text_output
    except Exception:
        return ""

# ==================== CONTROLLER STAGE 1: FIGMA HERO LANDING ====================
if st.session_state.page_router == "landing":
    # Emulated Top Navigation Bar matching Figma layout
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 1rem;">
            <div style="font-weight: 900; font-size: 1.6rem; color: #22D3EE; letter-spacing: 2px;">IR</div>
            <div style="display: flex; gap: 2.5rem; color: #94A3B8; font-size: 0.95rem; font-weight: 500;">
                <span style="color: #22D3EE; font-weight: 600; cursor: pointer;">Home</span>
                <span>Features</span>
                <span>Technology</span>
                <span>Contact</span>
            </div>
        </div>
        <hr style="border-color: #1E293B; margin-top: 0.5rem; margin-bottom: 2rem;">
    """, unsafe_allow_html=True)
    
    # Hero Segment Title Layout Frame
    st.markdown("""
        <div class="landing-container">
            <div class="cyber-title">THE INTELLIGENT<br>RECRUITER</div>
            <div class="cyber-subtitle">AI-powered talent intelligence system for next-generation hiring</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Centered CTA Trigger matching original high-fidelity view
    _, center_col, _ = st.columns([2.2, 1.2, 2.2])
    with center_col:
        if st.button("START SCREENING", type="primary", use_container_width=True):
            st.session_state.page_router = "inputs"
            st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Core Engineering Foundations")
    
    # Render the 3-columns matrix blocks inside the clean landing layout page
    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        st.markdown("""
            <div class="glass-card-node">
                <div style="font-size: 1.8rem; margin-bottom: 0.75rem;">⚡</div>
                <h4 style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem; color: #FFFFFF;">Fast Performance</h4>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin: 0;">Optimized architecture with modern frontend technologies and cloud-native deployment.</p>
            </div>
        """, unsafe_allow_html=True)
    with f_c2:
        st.markdown("""
            <div class="glass-card-node">
                <div style="font-size: 1.8rem; margin-bottom: 0.75rem;">🤖</div>
                <h4 style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem; color: #FFFFFF;">AI Automation</h4>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin: 0;">Integrate intelligent workflows and automation into your business enterprise systems.</p>
            </div>
        """, unsafe_allow_html=True)
    with f_c3:
        st.markdown("""
            <div class="glass-card-node">
                <div style="font-size: 1.8rem; margin-bottom: 0.75rem;">☁️</div>
                <h4 style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem; color: #FFFFFF;">Cloud Infrastructure</h4>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin: 0;">Deploy scalable applications safely using modern DevOps and secure cloud environments.</p>
            </div>
        """, unsafe_allow_html=True)


# ==================== CONTROLLER STAGE 2: CONFIGURATION & UPLOAD ====================
elif st.session_state.page_router == "inputs":
    st.markdown("## ⚙️ Target Profiling Console")
    st.write("Configure position objectives and batch-process multi-candidate documentation data profiles.")
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📝 Job Requirements Specification")
        job_title = st.text_input("Target Job Title", placeholder="e.g., Data Analyst / Software Engineer")
        job_skills = st.text_area(
            "Required Technical Stacks & Competencies",
            height=200,
            placeholder="e.g., Proficient with SQL schema queries, operational Git pipelines, Python data modules..."
        )
        
    with col_right:
        st.markdown("### 📂 Multi-Candidate Asset Deployment")
        uploaded_files = st.file_uploader(
            "Upload multiple candidate PDF resumes here:",
            type=["pdf"],
            accept_multiple_files=True
        )
        
    st.markdown("---")
    
    if st.button("START PROJECT 🚀", type="primary", use_container_width=True):
        if not job_title or not job_skills or not uploaded_files:
            st.warning("Validation Error: Please configure all input parameters and load candidate files.")
        else:
            runtime_cache = {}
            total_items = len(uploaded_files)
            progress_indicator = st.progress(0)
            
            for idx, item in enumerate(uploaded_files):
                c_name = item.name.replace(".pdf", "")
                st.toast(f"Processing candidate array data stream: {c_name}")
                
                extracted_text = extract_pdf_content(item)
                ai_payload_json = chutes.analyze_candidate_resume(job_title, job_skills, c_name, extracted_text)
                
                runtime_cache[c_name] = ai_payload_json
                progress_indicator.progress((idx + 1) / total_items)
                
            st.session_state.pipeline_records = runtime_cache
            st.session_state.page_router = "results"
            st.rerun()


# ==================== CONTROLLER STAGE 3: RESULT LEADERBOARD CARD MATRIX ====================
elif st.session_state.page_router == "results":
    st.markdown("## 🏆 Analytical Pipeline Leaderboard Matrix")
    
    if st.button("↩️ RUN NEW EVALUATION"):
        st.session_state.page_router = "inputs"
        st.session_state.pipeline_records = None
        st.rerun()
        
    st.markdown("---")
    
    dataset = st.session_state.pipeline_records
    if not dataset:
        st.info("No functional evaluation records discovered in cache.")
    else:
        for name, data in dataset.items():
            score_val = data.get("score", 0)
            ui_color = "#10B981" if score_val >= 80 else ("#F59E0B" if score_val >= 60 else "#EF4444")
            tag = "Highly Recommended" if score_val >= 80 else ("Shortlisted Variant" if score_val >= 60 else "Profile Deficient")
            
            with st.expander(f"👤 {name.upper()} — Match Rating Score: {score_val}/100 ({tag})"):
                left_panel, right_panel = st.columns([1.5, 2.5])
                
                with left_panel:
                    st.markdown("#### 📊 Suitability Rating Gauge")
                    st.markdown(f"""
                        <div style="background-color: #0F172A; border: 1px solid #1E293B; padding: 1.5rem; border-radius: 8px; text-align: center;">
                            <div style="font-size: 2.8rem; font-weight: 800; color: {ui_color};">{score_val} <span style="font-size: 1rem; color: #475569;">/ 100</span></div>
                            <div style="background-color: #334155; border-radius: 10px; height: 10px; width: 100%; margin: 1.2rem 0; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #22D3EE, {ui_color}); width: {score_val}%; height: 100%; border-radius: 10px;"></div>
                            </div>
                            <div style="font-size: 0.8rem; color: #64748B; font-weight: bold;">MATCH COMPLIANCE SPEED RANGE</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 🛠️ Direct Pipeline Engagement Actions")
                    st.markdown(
                        f'<a href="https://t.me/chimshiqi" target="_blank" style="text-decoration: none;">'
                        f'<div style="background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%); color: white; text-align: center; '
                        f'padding: 0.75rem; border-radius: 6px; font-weight: bold; cursor: pointer; margin-bottom: 0.5rem; font-size: 0.85rem;">'
                        f'💬 CONNECT VIA INSTANT TELEGRAM CHANNELS</div></a>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<a href="mailto:hr-test@university.edu?subject=Interview Call - {name}" target="_blank" style="text-decoration: none;">'
                        f'<div style="background-color: transparent; color: #E2E8F0; text-align: center; border: 1px solid #334155;'
                        f'padding: 0.75rem; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 0.85rem;">'
                        f'✉️ DISPATCH FORMAL EMAIL OUTREACH</div></a>',
                        unsafe_allow_html=True
                    )
                    
                with right_panel:
                    st.markdown("#### 🎯 Structural Evaluation Insights")
                    t1, t2, t3 = st.tabs(["Compliance Overview", "Vulnerabilities & Weaknesses", "Generated Interview Scripts"])
                    
                    with t1:
                        st.markdown(f"**🟢 Qualifications Summary:**\n{data.get('qualified')}")
                        st.markdown(f"**💻 Identified Language Architecture:**\n` {data.get('languages')} `")
                        st.markdown(f"**🏆 Competition Benchmarks & Active Repo Records:**\n{data.get('competitions')}")
                    with t2:
                        st.markdown(f"**🔴 Technical Weaknesses & Missing Stacks:**\n{data.get('weaknesses')}")
                    with t3:
                        st.markdown("**🤖 AI Automated Target Interview Questions (Dynamic Script):**")
                        for q_idx, q_text in enumerate(data.get("interview_questions", [])):
                            st.info(f"**Question {q_idx+1}:** {q_text}")

# Shared Persistent Footer Node
st.markdown('<br><br><hr style="border-color: #1E293B;">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align: center; color: #555555; font-size: 0.8rem; padding-bottom: 1rem;">'
    '© 2026 Intelligent Recruiter Project Inc. All rights reserved.</div>',
    unsafe_allow_html=True
)
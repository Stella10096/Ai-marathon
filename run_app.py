import os
import sys
import json
import re
import html
import textwrap
from urllib.parse import quote
import streamlit as st
from pypdf import PdfReader
import zipfile
import xml.etree.ElementTree as ET

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

/* Homepage START SCREENING button - exact reference style */
.st-key-home_start_button button,
.st-key-home_start_button div.stButton > button {
    background: linear-gradient(135deg, #38D1DF 0%, #0A7BFF 100%) !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 12px !important;
    height: 68px !important;
    min-height: 68px !important;
    width: 100% !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 18px 42px rgba(31, 180, 230, 0.28), 0 0 38px rgba(14, 124, 255, 0.18) !important;
}

.st-key-home_start_button button p,
.st-key-home_start_button div.stButton > button p {
    color: #FFFFFF !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
}

.st-key-home_start_button button:hover,
.st-key-home_start_button div.stButton > button:hover {
    transform: translateY(-1px) !important;
    filter: brightness(1.08) !important;
    box-shadow: 0 22px 48px rgba(31, 180, 230, 0.36), 0 0 46px rgba(14, 124, 255, 0.25) !important;
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

.core-section-title {
    text-align: center;
    font-size: 2.45rem;
    font-weight: 850;
    letter-spacing: -0.035em;
    line-height: 1.08;
    margin: 0 0 3.2rem 0;
    background: linear-gradient(90deg, #42D9F5 0%, #6EA8FF 48%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.glass-card-node {
    position: relative;
    min-height: 320px;
    height: 100%;
    border-radius: 22px;
    padding: 2.25rem 2.35rem;
    background: linear-gradient(180deg, rgba(12, 22, 36, 0.84), rgba(9, 13, 27, 0.92));
    border: 1px solid rgba(56, 189, 248, 0.23);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 24px 70px rgba(0, 0, 0, 0.24);
    backdrop-filter: blur(22px);
}

.glass-card-node.purple-card {
    background: linear-gradient(180deg, rgba(33, 12, 45, 0.86), rgba(22, 10, 31, 0.94));
    border-color: rgba(168, 85, 247, 0.27);
}

.core-card-icon {
    width: 72px;
    height: 72px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    background: linear-gradient(135deg, #22D3EE 0%, #0A84FF 100%);
    box-shadow: 0 18px 44px rgba(14, 165, 233, 0.22), 0 0 38px rgba(34, 211, 238, 0.12);
}

.core-card-icon.purple-icon {
    background: linear-gradient(135deg, #C084FC 0%, #EC4899 100%);
    box-shadow: 0 18px 44px rgba(192, 132, 252, 0.22), 0 0 38px rgba(236, 72, 153, 0.14);
}

.core-card-icon svg {
    width: 33px;
    height: 33px;
    stroke: #FFFFFF;
    stroke-width: 2.2;
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.core-card-title {
    margin: 0 0 1.25rem 0;
    font-size: 1.62rem;
    font-weight: 820;
    line-height: 1.22;
    letter-spacing: -0.035em;
}

.core-card-title.cyan {
    color: #22D3EE;
}

.core-card-title.blue {
    color: #60A5FA;
}

.core-card-title.purple {
    color: #C084FC;
}

.core-card-text {
    margin: 0;
    color: #A8B3C2;
    font-size: 1.03rem;
    line-height: 1.55;
    letter-spacing: -0.015em;
    max-width: 260px;
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

/* Apple-style form typography and fields */
label {
    color: #D6DEE9 !important;
    font-weight: 500 !important;
    font-size: 1.02rem !important;
    letter-spacing: -0.015em !important;
    margin-bottom: 0.35rem !important;
}

.stTextInput,
.stTextArea,
.stSelectbox {
    margin-bottom: 1.05rem !important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(5, 10, 22, 0.92) !important;
    border: 1px solid rgba(6, 182, 212, 0.78) !important;
    border-bottom: 1px solid rgba(6, 182, 212, 0.78) !important;
    outline: none !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
    min-height: 52px !important;
    box-shadow: inset 0 0 0 1px rgba(15, 23, 42, 0.28) !important;
    font-size: 1.02rem !important;
    font-weight: 400 !important;
    letter-spacing: -0.02em !important;
}

.stTextInput input:hover,
.stTextArea textarea:hover,
.stSelectbox div[data-baseweb="select"] > div:hover {
    border-color: rgba(34, 211, 238, 0.90) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: #22D3EE !important;
    border-bottom-color: #22D3EE !important;
    box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.18), inset 0 0 0 1px rgba(15, 23, 42, 0.28) !important;
}

.stTextArea textarea {
    min-height: 190px !important;
    padding-top: 15px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: rgba(148, 163, 184, 0.72) !important;
    font-weight: 400 !important;
}

.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] div {
    color: #F8FAFC !important;
    font-weight: 500 !important;
    letter-spacing: -0.02em !important;
}

.stSelectbox div[data-baseweb="select"] svg {
    color: #D6DEE9 !important;
    fill: #D6DEE9 !important;
}

/* Upload panel */
div[data-testid="stFileUploader"] label {
    display: none !important;
}

[data-testid="stFileUploaderDropzone"] {
    position: relative !important;
    background: transparent !important;
    border: 2px dashed rgba(147, 51, 234, 0.72) !important;
    border-radius: 16px !important;
    min-height: 285px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    overflow: hidden !important;
}

/* Hide Streamlit default uploader wording */
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] svg {
    display: none !important;
}

/* Center upload icon */
[data-testid="stFileUploaderDropzone"]::before {
    content: "⇧";
    position: absolute;
    top: 58px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 4rem;
    line-height: 1;
    color: #8B5CF6;
    font-weight: 800;
    text-shadow: 0 0 22px rgba(168, 85, 247, 0.42);
    pointer-events: none;
}

/* Center custom uploader text - Apple-like soft UI */
[data-testid="stFileUploaderDropzone"]::after {
    content: "Drag & drop resumes here\\A or click to browse\\A PDF and DOCX only";
    white-space: pre-line;
    position: absolute;
    top: 154px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    text-align: center;
    color: rgba(226, 232, 240, 0.72);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif !important;
    font-size: 1.05rem;
    font-weight: 500;
    letter-spacing: -0.01em;
    line-height: 1.95;
    pointer-events: none;
}

/* Make whole dropzone clickable while keeping button invisible */
[data-testid="stFileUploaderDropzone"] button {
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
    z-index: 10 !important;
}

.upload-ready {
    display: none !important;
}

.requirement-badge {
    display: none !important;
}

div[data-testid="stExpander"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}


/* AI analysis button: darker when incomplete, bright when ready */
.st-key-analysis_button_ready button {
    height: 76px !important;
    border-radius: 15px !important;
    background: linear-gradient(90deg, #0891B2 0%, #2563EB 48%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    font-size: 1.28rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.8px !important;
    border: none !important;
    box-shadow: 0 0 28px rgba(14, 165, 233, 0.22), 0 0 34px rgba(124, 58, 237, 0.18) !important;
}

.st-key-analysis_button_ready button:hover {
    filter: brightness(1.15) !important;
    transform: translateY(-1px);
}

.st-key-analysis_button_disabled button,
.st-key-analysis_button_disabled button:disabled {
    height: 76px !important;
    border-radius: 15px !important;
    background: linear-gradient(90deg, rgba(8, 145, 178, 0.38) 0%, rgba(37, 99, 235, 0.34) 48%, rgba(109, 40, 217, 0.40) 100%) !important;
    color: rgba(226, 232, 240, 0.48) !important;
    font-size: 1.28rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.8px !important;
    border: none !important;
    box-shadow: none !important;
    opacity: 1 !important;
    cursor: not-allowed !important;
}


/* Results page - Candidate Match Analysis */
.results-title {
    text-align:center;
    font-size:3.5rem;
    font-weight:950;
    letter-spacing:-0.035em;
    margin-top:0.6rem;
    margin-bottom:0.45rem;
    background:linear-gradient(90deg,#38BDF8 0%,#60A5FA 45%,#A78BFA 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.results-subtitle {
    text-align:center;
    color:#A7B0C0;
    font-size:1.05rem;
    letter-spacing:-0.01em;
    margin-bottom:3.2rem;
}
.metric-card {
    min-height:118px;
    border-radius:16px;
    padding:1.55rem 1.75rem;
    background:rgba(15,23,42,0.44);
    border:1px solid rgba(34,211,238,0.22);
    box-shadow:0 20px 60px rgba(0,0,0,0.16);
}
.metric-card.blue { border-color:rgba(34,211,238,0.32); background:linear-gradient(135deg,rgba(8,47,73,0.42),rgba(15,23,42,0.38)); }
.metric-card.indigo { border-color:rgba(99,102,241,0.32); background:linear-gradient(135deg,rgba(30,27,75,0.42),rgba(15,23,42,0.38)); }
.metric-card.purple { border-color:rgba(168,85,247,0.32); background:linear-gradient(135deg,rgba(59,7,100,0.30),rgba(24,14,38,0.42)); }
.metric-card.pink { border-color:rgba(236,72,153,0.28); background:linear-gradient(135deg,rgba(83,12,43,0.32),rgba(24,14,38,0.36)); }
.metric-label {
    color:#AAB2C0;
    font-size:0.98rem;
    font-weight:500;
    display:flex;
    gap:0.8rem;
    align-items:center;
    margin-bottom:1.3rem;
}
.metric-value {
    color:#F8FAFC;
    font-size:2.25rem;
    font-weight:900;
    letter-spacing:-0.04em;
}
.results-filter-bar {
    margin-top:3.4rem;
    margin-bottom:2.2rem;
    border-radius:16px;
    padding:1.6rem 1.75rem;
    background:linear-gradient(135deg,rgba(8,47,73,0.28),rgba(30,27,75,0.25));
    border:1px solid rgba(34,211,238,0.22);
}
.results-filter-bar input, .results-filter-bar div[data-baseweb="select"] > div {
    background:#070B16 !important;
    border:1px solid rgba(34,211,238,0.35) !important;
    border-radius:10px !important;
    color:#F8FAFC !important;
}
.candidate-card {
    margin:1.8rem 0;
    padding:1.75rem;
    border-radius:16px;
    background:linear-gradient(135deg,rgba(15,23,42,0.60),rgba(10,9,19,0.82));
    border:1px solid rgba(34,211,238,0.22);
    box-shadow:0 22px 70px rgba(0,0,0,0.18);
}
.candidate-top {
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    gap:1rem;
}
.candidate-name {
    color:#F8FAFC;
    font-size:1.65rem;
    font-weight:900;
    letter-spacing:-0.03em;
}
.candidate-meta {
    color:#AAB2C0;
    font-size:0.95rem;
    margin-top:0.35rem;
}
.candidate-score {
    font-size:2.45rem;
    font-weight:950;
    letter-spacing:-0.04em;
    background:linear-gradient(90deg,#22D3EE,#A78BFA);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    text-align:right;
}
.candidate-score-label {
    color:#7A8497;
    font-size:0.82rem;
    text-align:right;
}
.score-track {
    height:13px;
    border-radius:999px;
    background:#080711;
    overflow:hidden;
    margin:1rem 0 1.1rem 0;
}
.score-fill {
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#16C7D8 0%,#1479FF 70%,#A78BFA 100%);
}
.pill-row {
    display:flex;
    flex-wrap:wrap;
    gap:0.7rem;
    margin:0.8rem 0 1.3rem 0;
}
.skill-pill {
    color:#22D3EE;
    background:rgba(8,145,178,0.12);
    border:1px solid rgba(34,211,238,0.34);
    border-radius:999px;
    padding:0.35rem 0.85rem;
    font-size:0.82rem;
    font-weight:700;
}
.result-btn-link {
    display:block;
    width:100%;
    text-align:center;
    padding:0.78rem 1rem;
    border-radius:10px;
    text-decoration:none !important;
    color:#FFFFFF !important;
    font-weight:900;
    background:linear-gradient(90deg,#0EA5E9,#2563EB,#7C3AED);
}
.contact-link {
    display:block;
    text-align:center;
    padding:0.78rem 1rem;
    border-radius:10px;
    text-decoration:none !important;
    color:#FFFFFF !important;
    font-weight:900;
    background:linear-gradient(90deg,#A855F7,#C026D3);
}
.details-panel {
    margin-top:1.6rem;
    padding:1.5rem;
    border-top:1px solid rgba(34,211,238,0.18);
}
.detail-heading-green { color:#22C55E; font-weight:900; font-size:1.08rem; margin-bottom:0.8rem; }
.detail-heading-orange { color:#F59E0B; font-weight:900; font-size:1.08rem; margin:1.5rem 0 0.8rem 0; }
.detail-line { color:#D6D9E0; font-size:1rem; line-height:1.8; }
.ai-assessment-box {
    margin-top:1.5rem;
    border:1px solid rgba(168,85,247,0.34);
    background:rgba(88,28,135,0.10);
    border-radius:12px;
    padding:1.2rem;
}
.ai-title { color:#C084FC; font-weight:900; font-size:1.08rem; margin-bottom:0.7rem; }
.st-key-back_results button {
    background:rgba(15,23,42,0.72) !important;
    border:1px solid rgba(34,211,238,0.28) !important;
    color:#CBD5E1 !important;
    border-radius:12px !important;
}


/* Final Results Page Upgrade - Apple style candidate analysis */
.results-title {
    text-align:center;
    font-size:3.55rem;
    font-weight:950;
    letter-spacing:-0.045em;
    margin-top:0.4rem;
    margin-bottom:0.55rem;
    background:linear-gradient(90deg,#38BDF8 0%,#60A5FA 44%,#A78BFA 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.results-subtitle {
    text-align:center;
    color:#B4BDCC;
    font-size:1.06rem;
    font-weight:450;
    letter-spacing:-0.012em;
    margin-bottom:3.1rem;
}
.results-top-space { margin-top:0.4rem; }
.metric-card {
    min-height:118px;
    border-radius:17px;
    padding:1.6rem 1.75rem;
    background:rgba(13,18,32,0.62);
    border:1px solid rgba(34,211,238,0.26);
    box-shadow:0 22px 70px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.035);
}
.metric-card.blue { border-color:rgba(34,211,238,0.32); background:linear-gradient(135deg,rgba(8,47,73,0.44),rgba(15,23,42,0.50)); }
.metric-card.indigo { border-color:rgba(99,102,241,0.35); background:linear-gradient(135deg,rgba(30,27,75,0.43),rgba(15,23,42,0.48)); }
.metric-card.purple { border-color:rgba(168,85,247,0.34); background:linear-gradient(135deg,rgba(59,7,100,0.34),rgba(24,14,38,0.47)); }
.metric-card.pink { border-color:rgba(236,72,153,0.32); background:linear-gradient(135deg,rgba(83,12,43,0.38),rgba(24,14,38,0.44)); }
.metric-label {
    color:#AAB3C2;
    font-size:0.96rem;
    font-weight:550;
    display:flex;
    gap:0.8rem;
    align-items:center;
    margin-bottom:1.25rem;
    letter-spacing:-0.01em;
}
.metric-icon {
    width:22px;
    height:22px;
    stroke:currentColor;
    stroke-width:2.2;
    fill:none;
    stroke-linecap:round;
    stroke-linejoin:round;
}
.metric-card.blue .metric-label { color:#22D3EE; }
.metric-card.indigo .metric-label { color:#60A5FA; }
.metric-card.purple .metric-label { color:#C084FC; }
.metric-card.pink .metric-label { color:#F472B6; }
.metric-label span { color:#AAB3C2; }
.metric-value {
    color:#FFFFFF;
    font-size:2.25rem;
    font-weight:920;
    letter-spacing:-0.055em;
    line-height:1;
}
.results-filter-bar {
    margin-top:3.35rem;
    margin-bottom:2.25rem;
    border-radius:17px;
    padding:1.65rem 1.75rem;
    background:linear-gradient(135deg,rgba(8,47,73,0.25),rgba(30,27,75,0.22));
    border:1px solid rgba(34,211,238,0.24);
    box-shadow:0 20px 70px rgba(0,0,0,0.16), inset 0 1px 0 rgba(255,255,255,0.025);
}
.results-filter-bar input,
.results-filter-bar div[data-baseweb="select"] > div {
    background:#070B16 !important;
    border:1px solid rgba(34,211,238,0.42) !important;
    border-radius:11px !important;
    color:#F8FAFC !important;
    min-height:56px !important;
    box-shadow:none !important;
}
.candidate-card {
    margin:1.85rem 0;
    border-radius:17px;
    background:linear-gradient(135deg,rgba(12,18,31,0.70),rgba(10,8,18,0.88));
    border:1px solid rgba(34,211,238,0.24);
    box-shadow:0 24px 72px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.025);
    overflow:hidden;
}
.candidate-main {
    padding:1.75rem 1.75rem 1.65rem 1.75rem;
}
.candidate-top {
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    gap:1rem;
}
.candidate-name {
    color:#FFFFFF;
    font-size:1.65rem;
    font-weight:880;
    letter-spacing:-0.04em;
    line-height:1.1;
}
.candidate-meta {
    color:#AAB3C2;
    font-size:0.96rem;
    margin-top:0.48rem;
    letter-spacing:-0.01em;
}
.candidate-score {
    font-size:2.45rem;
    font-weight:950;
    letter-spacing:-0.055em;
    line-height:1;
    background:linear-gradient(90deg,#22D3EE 0%,#60A5FA 48%,#A78BFA 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    text-align:right;
}
.candidate-score-label {
    color:#7B8494;
    font-size:0.82rem;
    text-align:right;
    margin-top:0.25rem;
}
.score-track {
    height:14px;
    border-radius:999px;
    background:#080711;
    overflow:hidden;
    margin:1.1rem 0 1.1rem 0;
}
.score-fill {
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#16C7D8 0%,#1479FF 70%,#A78BFA 100%);
}
.pill-row {
    display:flex;
    flex-wrap:wrap;
    gap:0.68rem;
    margin:0.82rem 0 1.35rem 0;
}
.skill-pill {
    color:#22D3EE;
    background:rgba(8,145,178,0.13);
    border:1px solid rgba(34,211,238,0.38);
    border-radius:999px;
    padding:0.36rem 0.82rem;
    font-size:0.81rem;
    font-weight:700;
    letter-spacing:-0.01em;
}
.card-action-row {
    display:grid;
    grid-template-columns:minmax(0,1fr) 128px;
    gap:0.85rem;
    align-items:center;
}
details.analysis-details > summary {
    list-style:none;
    cursor:pointer;
    text-align:center;
    padding:0.82rem 1rem;
    border-radius:10px;
    color:#FFFFFF;
    font-weight:900;
    letter-spacing:-0.015em;
    background:linear-gradient(90deg,#0EA5E9 0%,#2563EB 55%,#7C3AED 100%);
    user-select:none;
}
details.analysis-details > summary::-webkit-details-marker { display:none; }
details.analysis-details > summary::after { content:"  ⌄"; font-size:0.95rem; }
details.analysis-details[open] > summary::after { content:"  ⌃"; font-size:0.95rem; }
.contact-link {
    display:block;
    text-align:center;
    padding:0.82rem 1rem;
    border-radius:10px;
    text-decoration:none !important;
    color:#FFFFFF !important;
    font-weight:900;
    letter-spacing:-0.015em;
    background:linear-gradient(90deg,#A855F7,#C026D3);
    box-shadow:0 12px 34px rgba(168,85,247,0.18);
}
.contact-email-hint {
    margin-top:0.42rem;
    color:#7B8494;
    font-size:0.76rem;
    text-align:center;
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
}
.details-panel {
    margin-top:1.65rem;
    padding:1.65rem 0 0.1rem 0;
    border-top:1px solid rgba(34,211,238,0.18);
}
.detail-heading-green,
.detail-heading-orange,
.detail-heading-blue {
    font-weight:900;
    font-size:1.08rem;
    margin-bottom:0.9rem;
    letter-spacing:-0.02em;
}
.detail-heading-green { color:#22C55E; }
.detail-heading-orange { color:#F59E0B; margin-top:1.55rem; }
.detail-heading-blue { color:#38BDF8; margin-top:1.55rem; }
.detail-line {
    color:#D7DBE4;
    font-size:1rem;
    line-height:2.05;
    letter-spacing:-0.012em;
}
.detail-prefix { font-weight:900; }
.detail-grid {
    display:grid;
    grid-template-columns:repeat(2,minmax(0,1fr));
    gap:0.9rem 1.2rem;
    margin-top:0.8rem;
}
.detail-info-card {
    border:1px solid rgba(34,211,238,0.18);
    background:rgba(8,13,24,0.52);
    border-radius:12px;
    padding:0.95rem 1rem;
}
.detail-info-label {
    color:#7B8494;
    font-size:0.78rem;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:0.06em;
    margin-bottom:0.35rem;
}
.detail-info-value {
    color:#F8FAFC;
    font-size:0.98rem;
    line-height:1.55;
}
.ai-assessment-box {
    margin-top:1.55rem;
    border:1px solid rgba(168,85,247,0.36);
    background:rgba(88,28,135,0.10);
    border-radius:13px;
    padding:1.2rem;
}
.ai-title {
    color:#C084FC;
    font-weight:900;
    font-size:1.08rem;
    margin-bottom:0.72rem;
    letter-spacing:-0.02em;
}
.interview-box {
    margin-top:1.2rem;
    border-radius:13px;
    padding:1rem 1.15rem;
    background:linear-gradient(90deg,rgba(236,72,153,0.16),rgba(168,85,247,0.14));
    border:1px solid rgba(192,38,211,0.28);
}

details.analysis-details .open-label { display:none; }
details.analysis-details[open] .closed-label { display:none; }
details.analysis-details[open] .open-label { display:inline; }
.generate-question-btn {
    margin-top:1.45rem;
    padding:0.9rem 1rem;
    border-radius:11px;
    text-align:center;
    color:#FFFFFF;
    font-weight:900;
    letter-spacing:-0.02em;
    background:linear-gradient(90deg,#EC4899 0%,#A855F7 55%,#7C3AED 100%);
    box-shadow:0 14px 36px rgba(168,85,247,0.18);
}
.st-key-back_results button {
    height:50px !important;
    border-radius:14px !important;
    background:rgba(12,18,31,0.72) !important;
    border:1px solid rgba(34,211,238,0.28) !important;
    color:#E5E7EB !important;
    font-size:0.96rem !important;
    font-weight:800 !important;
    letter-spacing:-0.02em !important;
    box-shadow:0 14px 34px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.04) !important;
}
.st-key-back_results button:hover {
    color:#FFFFFF !important;
    border-color:rgba(34,211,238,0.52) !important;
    box-shadow:0 18px 42px rgba(34,211,238,0.12) !important;
    transform:translateY(-1px) !important;
}



/* Apple-style result page controls: no emoji/icon prefixes */
.st-key-back_results button {
    height: 52px !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, rgba(12,18,31,0.84), rgba(15,23,42,0.68)) !important;
    border: 1px solid rgba(34,211,238,0.30) !important;
    color: #EAF2FF !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    font-size: 0.98rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.022em !important;
    text-transform: none !important;
    box-shadow: 0 14px 34px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.045) !important;
}
.st-key-back_results button p,
.st-key-back_results button span,
.st-key-back_results button div {
    color: #EAF2FF !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    font-size: 0.98rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.022em !important;
    text-transform: none !important;
}
.st-key-back_results button:hover {
    color: #FFFFFF !important;
    border-color: rgba(34,211,238,0.54) !important;
    background: linear-gradient(135deg, rgba(14,165,233,0.24), rgba(124,58,237,0.24)) !important;
    box-shadow: 0 18px 42px rgba(34,211,238,0.12), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    transform: translateY(-1px) !important;
}

/* View Analysis / Hide Details button - Apple style, no leading icon */
div[class*="st-key-view_analysis_"] button {
    height: 46px !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.024em !important;
    text-transform: none !important;
    border: 0 !important;
    background: linear-gradient(90deg, #0EA5E9 0%, #2563EB 56%, #7C3AED 100%) !important;
    box-shadow: 0 14px 36px rgba(37,99,235,0.18), inset 0 1px 0 rgba(255,255,255,0.12) !important;
}
div[class*="st-key-view_analysis_"] button p,
div[class*="st-key-view_analysis_"] button span,
div[class*="st-key-view_analysis_"] button div {
    color: #FFFFFF !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.024em !important;
    text-transform: none !important;
}
div[class*="st-key-view_analysis_"] button:hover {
    filter: brightness(1.08) !important;
    transform: translateY(-1px) !important;
}

/* Generate Interview Questions button - Apple style, answer appears only after click */
div[class*="st-key-generate_questions_"] button {
    min-height: 54px !important;
    border-radius: 13px !important;
    background: linear-gradient(90deg, #EC4899 0%, #A855F7 55%, #7C3AED 100%) !important;
    border: 0 !important;
    color: #FFFFFF !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    font-size: 1.03rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.024em !important;
    text-transform: none !important;
    box-shadow: 0 14px 36px rgba(168,85,247,0.20), inset 0 1px 0 rgba(255,255,255,0.12) !important;
}
div[class*="st-key-generate_questions_"] button p,
div[class*="st-key-generate_questions_"] button span,
div[class*="st-key-generate_questions_"] button div {
    color: #FFFFFF !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    font-size: 1.03rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.024em !important;
    text-transform: none !important;
}
div[class*="st-key-generate_questions_"] button:hover {
    filter: brightness(1.08) !important;
    transform: translateY(-1px) !important;
}

/* Result page text refinements */
.results-title,
.results-subtitle,
.candidate-name,
.candidate-meta,
.candidate-score,
.candidate-score-label,
.metric-label,
.metric-value,
.skill-pill,
.detail-heading-green,
.detail-heading-orange,
.detail-heading-blue,
.detail-line,
.detail-info-label,
.detail-info-value,
.ai-title,
.contact-link,
.contact-email-hint {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif !important;
}
.contact-link {
    font-weight: 650 !important;
    letter-spacing: -0.024em !important;
}

@media (max-width: 900px) {
    .card-action-row { grid-template-columns:1fr; }
    .detail-grid { grid-template-columns:1fr; }
    .results-title { font-size:2.35rem; }
}

/* Native Streamlit candidate card fix: prevents raw HTML from appearing */
div[class*="st-key-candidate_card_"] {
    margin: 1.85rem 0 !important;
    padding: 1.75rem !important;
    border-radius: 17px !important;
    background: linear-gradient(135deg, rgba(12,18,31,0.70), rgba(10,8,18,0.88)) !important;
    border: 1px solid rgba(34,211,238,0.24) !important;
    box-shadow: 0 24px 72px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.025) !important;
    overflow: hidden !important;
}

div[class*="st-key-view_analysis_"] button {
    height: 46px !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
    letter-spacing: -0.015em !important;
    border: none !important;
    background: linear-gradient(90deg, #0EA5E9 0%, #2563EB 55%, #7C3AED 100%) !important;
    box-shadow: none !important;
}

div[class*="st-key-view_analysis_"] button:hover {
    filter: brightness(1.08) !important;
    transform: translateY(-1px) !important;
}

div[class*="st-key-contact_link_"] a {
    height: 46px !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
    letter-spacing: -0.015em !important;
    border: none !important;
    background: linear-gradient(90deg, #A855F7, #C026D3) !important;
    box-shadow: 0 12px 34px rgba(168,85,247,0.18) !important;
}

div[class*="st-key-contact_link_"] a p {
    color: #FFFFFF !important;
    font-weight: 900 !important;
}

div[class*="st-key-generate_questions_"] button {
    height: 52px !important;
    border-radius: 11px !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
    letter-spacing: -0.02em !important;
    border: none !important;
    background: linear-gradient(90deg, #EC4899 0%, #A855F7 55%, #7C3AED 100%) !important;
    box-shadow: 0 14px 36px rgba(168,85,247,0.18) !important;
}

.candidate-divider {
    height: 1px;
    background: rgba(34,211,238,0.18);
    margin: 1.55rem -1.75rem 1.55rem -1.75rem;
}

.candidate-section-gap {
    height: 0.45rem;
}


/* Contact Page - Apple style */
.contact-title {
    text-align:center;
    font-size:3.35rem;
    font-weight:950;
    letter-spacing:-0.045em;
    margin-top:0.6rem;
    margin-bottom:0.65rem;
    background:linear-gradient(90deg,#38BDF8 0%,#2563EB 48%,#8B5CF6 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.contact-subtitle {
    text-align:center;
    color:#B8C2D4;
    font-size:1.18rem;
    font-weight:450;
    letter-spacing:-0.018em;
    margin-bottom:4rem;
}
.contact-info-card {
    min-height:170px;
    border-radius:18px;
    padding:1.75rem 1.5rem;
    background:linear-gradient(180deg,rgba(12,22,36,0.74),rgba(9,13,27,0.88));
    border:1px solid rgba(34,211,238,0.22);
    box-shadow:0 22px 64px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.035);
    text-align:center;
}
.contact-info-icon {
    width:62px;
    height:62px;
    border-radius:16px;
    margin:0 auto 1.25rem auto;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#22D3EE 0%,#0A84FF 100%);
    box-shadow:0 18px 44px rgba(14,165,233,0.24), 0 0 36px rgba(34,211,238,0.14);
}
.contact-info-icon svg {
    width:31px;
    height:31px;
    stroke:#FFFFFF;
    stroke-width:2.1;
    fill:none;
    stroke-linecap:round;
    stroke-linejoin:round;
}
.contact-info-label {
    color:#9CA8BA;
    font-size:0.92rem;
    font-weight:560;
    letter-spacing:-0.012em;
    margin-bottom:0.72rem;
}
.contact-info-value {
    color:#F8FAFC;
    font-size:1.02rem;
    font-weight:820;
    letter-spacing:-0.02em;
}
.st-key-contact_form_card {
    background:linear-gradient(180deg,rgba(15,23,42,0.64),rgba(16,10,31,0.86));
    border:1px solid rgba(34,211,238,0.24);
    border-radius:18px;
    padding:2.1rem 2.2rem 2.25rem 2.2rem;
    min-height:610px;
    box-shadow:0 24px 76px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.03);
}
.contact-panel-title-cyan {
    color:#22D3EE;
    font-size:1.6rem;
    font-weight:900;
    letter-spacing:-0.035em;
    margin-bottom:1.7rem;
}
.contact-panel-title-purple {
    color:#C084FC;
    font-size:1.6rem;
    font-weight:900;
    letter-spacing:-0.035em;
    margin-bottom:1.7rem;
}
.st-key-contact_form_card label,
.st-key-contact_form_card .stTextInput label,
.st-key-contact_form_card .stTextArea label {
    color:#AAB3C2 !important;
    font-size:0.93rem !important;
    font-weight:700 !important;
    letter-spacing:-0.014em !important;
}
.st-key-contact_form_card .stTextInput input,
.st-key-contact_form_card .stTextArea textarea {
    background:#070B16 !important;
    border:1px solid rgba(34,211,238,0.36) !important;
    border-radius:12px !important;
    color:#F8FAFC !important;
    font-size:1rem !important;
    font-weight:450 !important;
    letter-spacing:-0.02em !important;
    box-shadow:none !important;
}
.st-key-contact_form_card .stTextArea textarea {
    min-height:190px !important;
}
.contact-send-link,
.contact-action-link {
    display:flex;
    align-items:center;
    justify-content:center;
    gap:0.7rem;
    width:100%;
    min-height:56px;
    border-radius:12px;
    text-decoration:none !important;
    color:#FFFFFF !important;
    font-size:1rem;
    font-weight:850;
    letter-spacing:-0.025em;
    box-shadow:0 16px 38px rgba(14,165,233,0.12);
    transition:all 0.15s ease;
}
.contact-send-link:hover,
.contact-action-link:hover {
    transform:translateY(-1px);
    filter:brightness(1.08);
}
.contact-send-link {
    margin-top:1.55rem;
    background:linear-gradient(90deg,#13B8D4 0%,#1479FF 100%);
}
.contact-action-link svg,
.contact-send-link svg {
    width:22px;
    height:22px;
    stroke:#FFFFFF;
    stroke-width:2.2;
    fill:none;
    stroke-linecap:round;
    stroke-linejoin:round;
}
.contact-action-link.blue {
    background:linear-gradient(90deg,#13B8D4 0%,#1762FF 100%);
}
.contact-action-link.pink {
    background:linear-gradient(90deg,#A855F7 0%,#EC4899 100%);
}
.contact-action-link.teal {
    background:linear-gradient(90deg,#2F80ED 0%,#0499B5 100%);
}
.st-key-contact_actions_card,
.st-key-contact_help_card,
.st-key-contact_hours_card {
    border-radius:18px;
    padding:2rem 2.15rem;
    box-shadow:0 24px 76px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.03);
}
.st-key-contact_actions_card {
    background:linear-gradient(180deg,rgba(33,12,45,0.84),rgba(22,10,31,0.94));
    border:1px solid rgba(168,85,247,0.30);
}
.st-key-contact_help_card,
.st-key-contact_hours_card {
    background:linear-gradient(180deg,rgba(12,22,36,0.74),rgba(9,13,27,0.88));
    border:1px solid rgba(34,211,238,0.22);
}
.contact-help-row {
    display:flex;
    align-items:center;
    gap:1.15rem;
}
.contact-help-icon {
    flex:0 0 auto;
    width:56px;
    height:56px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#22D3EE 0%,#0A84FF 100%);
    box-shadow:0 18px 44px rgba(14,165,233,0.22);
}
.contact-help-icon svg {
    width:30px;
    height:30px;
    stroke:#FFFFFF;
    stroke-width:2.2;
    fill:none;
    stroke-linecap:round;
    stroke-linejoin:round;
}
.contact-help-title {
    color:#60A5FA;
    font-size:1.25rem;
    font-weight:900;
    letter-spacing:-0.035em;
    margin-bottom:0.5rem;
}
.contact-help-text {
    color:#AAB3C2;
    font-size:1rem;
    line-height:1.55;
    letter-spacing:-0.015em;
}
.contact-hours-title {
    color:#22D3EE;
    font-size:1.15rem;
    font-weight:900;
    letter-spacing:-0.03em;
    margin-bottom:1.25rem;
}
.contact-hours-row {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:1rem;
    margin:0.85rem 0;
    color:#AAB3C2;
    font-size:0.96rem;
    letter-spacing:-0.015em;
}
.contact-hours-value {
    color:#F8FAFC;
    font-weight:850;
    text-align:right;
}
@media (max-width:900px) {
    .contact-title { font-size:2.35rem; }
    .contact-subtitle { font-size:1rem; margin-bottom:2.2rem; }
}



/* Technology Page - Apple style */
.tech-title {
    text-align:center;
    font-size:3.45rem;
    font-weight:950;
    letter-spacing:-0.045em;
    margin-top:0.6rem;
    margin-bottom:0.7rem;
    background:linear-gradient(90deg,#38BDF8 0%,#2563EB 48%,#8B5CF6 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.tech-subtitle {
    text-align:center;
    color:#B8C2D4;
    font-size:1.18rem;
    font-weight:450;
    letter-spacing:-0.018em;
    line-height:1.45;
    max-width:850px;
    margin:0 auto 4.2rem auto;
}
.tech-stat-card {
    min-height:168px;
    border-radius:18px;
    padding:1.75rem 1.5rem;
    background:linear-gradient(180deg,rgba(12,22,36,0.70),rgba(16,10,31,0.82));
    border:1px solid rgba(34,211,238,0.22);
    box-shadow:0 22px 64px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.035);
    text-align:center;
}
.tech-stat-icon {
    width:44px;
    height:44px;
    margin:0 auto 0.9rem auto;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#22D3EE;
}
.tech-stat-card.purple .tech-stat-icon { color:#C084FC; }
.tech-stat-card.blue .tech-stat-icon { color:#60A5FA; }
.tech-stat-icon svg {
    width:36px;
    height:36px;
    stroke:currentColor;
    stroke-width:2.2;
    fill:none;
    stroke-linecap:round;
    stroke-linejoin:round;
}
.tech-stat-label {
    color:#9CA8BA;
    font-size:0.92rem;
    font-weight:560;
    letter-spacing:-0.012em;
    margin-bottom:0.7rem;
}
.tech-stat-value {
    color:#F8FAFC;
    font-size:1.45rem;
    font-weight:900;
    letter-spacing:-0.035em;
}
.tech-feature-card {
    margin-top:2.25rem;
    border-radius:18px;
    padding:2.35rem 2.4rem;
    border:1px solid rgba(34,211,238,0.22);
    background:linear-gradient(135deg,rgba(8,47,73,0.23),rgba(15,23,42,0.50));
    box-shadow:0 24px 72px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.03);
}
.tech-feature-card.purple {
    border-color:rgba(168,85,247,0.28);
    background:linear-gradient(135deg,rgba(59,7,100,0.26),rgba(24,14,38,0.48));
}
.tech-feature-card.pink {
    border-color:rgba(236,72,153,0.26);
    background:linear-gradient(135deg,rgba(83,12,43,0.26),rgba(24,14,38,0.48));
}
.tech-feature-card.green {
    border-color:rgba(34,197,94,0.26);
    background:linear-gradient(135deg,rgba(5,46,22,0.24),rgba(8,18,18,0.50));
}
.tech-feature-row {
    display:grid;
    grid-template-columns:92px minmax(0,1fr);
    gap:1.45rem;
    align-items:center;
}
.tech-feature-icon {
    width:90px;
    height:90px;
    border-radius:20px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#22D3EE 0%,#0A84FF 100%);
    box-shadow:0 18px 44px rgba(14,165,233,0.24), 0 0 36px rgba(34,211,238,0.14);
}
.tech-feature-card.purple .tech-feature-icon {
    background:linear-gradient(135deg,#C084FC 0%,#EC4899 100%);
    box-shadow:0 18px 44px rgba(192,132,252,0.22), 0 0 36px rgba(236,72,153,0.14);
}
.tech-feature-card.pink .tech-feature-icon {
    background:linear-gradient(135deg,#EC4899 0%,#9333EA 100%);
    box-shadow:0 18px 44px rgba(236,72,153,0.20), 0 0 36px rgba(147,51,234,0.14);
}
.tech-feature-card.green .tech-feature-icon {
    background:linear-gradient(135deg,#22C55E 0%,#059669 100%);
    box-shadow:0 18px 44px rgba(34,197,94,0.20), 0 0 36px rgba(16,185,129,0.14);
}
.tech-feature-icon svg {
    width:46px;
    height:46px;
    stroke:#FFFFFF;
    stroke-width:2.1;
    fill:none;
    stroke-linecap:round;
    stroke-linejoin:round;
}
.tech-feature-title {
    font-size:1.55rem;
    font-weight:900;
    letter-spacing:-0.035em;
    margin-bottom:0.75rem;
    color:#22D3EE;
}
.tech-feature-card.purple .tech-feature-title { color:#C084FC; }
.tech-feature-card.pink .tech-feature-title { color:#F472B6; }
.tech-feature-card.green .tech-feature-title { color:#22C55E; }
.tech-feature-text {
    color:#AAB3C2;
    font-size:1.03rem;
    font-weight:430;
    letter-spacing:-0.016em;
    line-height:1.65;
}
.tech-cta-card,
.st-key-tech_cta_card {
    max-width:880px;
    margin:4.2rem auto 0 auto;
    border-radius:18px;
    padding:2.35rem 2.4rem 2.6rem 2.4rem;
    text-align:center;
    border:1px solid rgba(168,85,247,0.30);
    background:linear-gradient(135deg,rgba(30,27,75,0.38),rgba(24,14,38,0.48));
    box-shadow:0 24px 72px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.03);
}
.tech-cta-title {
    font-size:1.55rem;
    font-weight:900;
    letter-spacing:-0.035em;
    background:linear-gradient(90deg,#38BDF8 0%,#60A5FA 45%,#A78BFA 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:1.05rem;
}
.tech-cta-text {
    color:#AAB3C2;
    font-size:1.02rem;
    letter-spacing:-0.014em;
    margin-bottom:1.55rem;
}
.st-key-tech_start_button button {
    height:54px !important;
    max-width:420px !important;
    margin:0 auto !important;
    border-radius:12px !important;
    background:linear-gradient(90deg,#22D3EE 0%,#2563EB 100%) !important;
    color:#FFFFFF !important;
    border:0 !important;
    font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Arial,sans-serif !important;
    font-size:0.98rem !important;
    font-weight:700 !important;
    letter-spacing:-0.022em !important;
    box-shadow:0 14px 38px rgba(37,99,235,0.22), inset 0 1px 0 rgba(255,255,255,0.12) !important;
}
.st-key-tech_start_button button p,
.st-key-tech_start_button button span,
.st-key-tech_start_button button div {
    color:#FFFFFF !important;
    font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Arial,sans-serif !important;
    font-size:0.98rem !important;
    font-weight:700 !important;
    letter-spacing:-0.022em !important;
}
.st-key-tech_start_button button:hover {
    filter:brightness(1.08) !important;
    transform:translateY(-1px) !important;
}

/* Keep the Technology CTA button inside the same card without changing text alignment */
.st-key-tech_cta_card {
    text-align:center !important;
}
.st-key-tech_cta_card .tech-cta-title,
.st-key-tech_cta_card .tech-cta-text {
    text-align:center !important;
    margin-left:auto !important;
    margin-right:auto !important;
}
.st-key-tech_cta_card div[data-testid="column"] {
    display:flex !important;
    justify-content:center !important;
}
.st-key-tech_cta_card .stButton {
    width:100% !important;
    display:flex !important;
    justify-content:center !important;
}
.st-key-tech_cta_card .stButton > button {
    width:100% !important;
    min-width:420px !important;
}
@media (max-width: 900px) {
    .tech-feature-row { grid-template-columns:1fr; }
    .tech-title { font-size:2.35rem; }
}

</style>
""", unsafe_allow_html=True)


def extract_file_content(file_asset):
    """Extract readable text from uploaded PDF or DOCX files.

    DOCX extraction uses only Python standard libraries, so there is
    no need to install python-docx.
    """
    try:
        file_name = file_asset.name.lower()
        file_asset.seek(0)

        if file_name.endswith(".pdf"):
            reader = PdfReader(file_asset)
            text_output = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_output += text + "\n"

            return text_output.strip()

        if file_name.endswith(".docx"):
            with zipfile.ZipFile(file_asset) as docx_zip:
                xml_content = docx_zip.read("word/document.xml")

            root = ET.fromstring(xml_content)
            namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

            paragraphs = []
            for paragraph in root.findall(".//w:p", namespace):
                texts = [node.text for node in paragraph.findall(".//w:t", namespace) if node.text]
                if texts:
                    paragraphs.append("".join(texts))

            return "\n".join(paragraphs).strip()

        st.error("Unsupported file format. Please upload PDF or DOCX only.")
        return ""

    except Exception as e:
        st.error(f"File extraction failed for {file_asset.name}: {e}")
        return ""


def clean_list_value(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    if not text or text.upper() == "N/A":
        return []
    parts = re.split(r"[,;\n•]+", text)
    return [p.strip(" -\t") for p in parts if p.strip(" -\t")]


def first_present(data, keys, default="N/A"):
    for key in keys:
        value = data.get(key)
        if value not in [None, "", [], {}]:
            return value
    return default


def find_email_from_data(data):
    # Search common direct fields first, then safely scan nested AI response values.
    for key in ["email", "gmail", "contact", "contact_email", "candidate_email"]:
        value = str(data.get(key, ""))
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", value)
        if match:
            return match.group(0)

    def scan(value):
        if isinstance(value, dict):
            for nested in value.values():
                found = scan(nested)
                if found:
                    return found
        elif isinstance(value, list):
            for nested in value:
                found = scan(nested)
                if found:
                    return found
        else:
            match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(value))
            if match:
                return match.group(0)
        return ""

    return scan(data)


def extract_email_from_text(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(text or ""))
    return match.group(0) if match else ""


def extract_cgpa_from_text(text):
    text = str(text or "")
    patterns = [
        r"(?:CGPA|GPA)\s*[:\-]?\s*([0-4](?:\.\d{1,2})?)\s*(?:/\s*4(?:\.0)?)?",
        r"([0-4](?:\.\d{1,2})?)\s*/\s*4(?:\.0)?"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return ""


def candidate_mail_link(email):
    if email:
        return "https://mail.google.com/mail/?view=cm&fs=1&to=" + quote(email)
    return "https://mail.google.com/"





def gmail_compose_url(to_email="4bits.recruiter@gmail.com", subject="", body=""):
    url = "https://mail.google.com/mail/?view=cm&fs=1&to=" + quote(to_email)
    if subject:
        url += "&su=" + quote(subject)
    if body:
        url += "&body=" + quote(body)
    return url


def html_escape(value):
    return html.escape(str(value))


def render_detail_lines(items, prefix="✓", fallback="Not available."):
    if not items:
        return f'<div class="detail-line"><span class="detail-prefix">{html_escape(prefix)}</span> {html_escape(fallback)}</div>'
    return "".join(
        f'<div class="detail-line"><span class="detail-prefix">{html_escape(prefix)}</span> {html_escape(item)}</div>'
        for item in items[:8]
    )


def render_skill_pills(skills):
    return "".join(f'<span class="skill-pill">{html_escape(skill)}</span>' for skill in skills[:10])


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
    if st.button("Technology", use_container_width=True):
        st.session_state.page_router = "technology"
        st.rerun()

with nav_c5:
    if st.button("Contact", use_container_width=True):
        st.session_state.page_router = "contact"
        st.rerun()

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
        if st.button("START SCREENING", type="primary", use_container_width=True, key="home_start_button"):
            st.session_state.page_router = "inputs"
            st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="core-section-title">Core Engineering Foundations</div>', unsafe_allow_html=True)

    f_c1, f_c2, f_c3 = st.columns(3)

    with f_c1:
        st.markdown("""
        <div class="glass-card-node">
            <div class="core-card-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M13 2L4 14h7l-1 8 10-13h-7l0-7z"></path>
                </svg>
            </div>
            <h4 class="core-card-title cyan">Fast<br>Performance</h4>
            <p class="core-card-text">Optimized architecture with modern frontend technologies and cloud-native deployment.</p>
        </div>
        """, unsafe_allow_html=True)

    with f_c2:
        st.markdown("""
        <div class="glass-card-node purple-card">
            <div class="core-card-icon purple-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="7" y="8" width="10" height="9" rx="2"></rect>
                    <path d="M9 8V6a3 3 0 0 1 6 0v2"></path>
                    <path d="M5 12H3"></path>
                    <path d="M21 12h-2"></path>
                    <path d="M10 12h4"></path>
                    <path d="M12 10v4"></path>
                </svg>
            </div>
            <h4 class="core-card-title purple">AI Automation</h4>
            <p class="core-card-text">Integrate intelligent workflows and automation into your enterprise systems.</p>
        </div>
        """, unsafe_allow_html=True)

    with f_c3:
        st.markdown("""
        <div class="glass-card-node">
            <div class="core-card-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M7.5 18h9a4.5 4.5 0 0 0 .4-8.98A6.2 6.2 0 0 0 5.2 10.5 3.8 3.8 0 0 0 7.5 18z"></path>
                </svg>
            </div>
            <h4 class="core-card-title blue">Cloud<br>Infrastructure</h4>
            <p class="core-card-text">Deploy scalable applications using modern DevOps and secure cloud environments.</p>
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

    missing_fields = []

    if not job_title.strip():
        missing_fields.append("Position Title")
    if not job_skills.strip():
        missing_fields.append("Required Skills")
    if experience_level == "Select experience level":
        missing_fields.append("Experience Level")
    if not preferred_technologies.strip():
        missing_fields.append("Preferred Technologies")
    if not job_description.strip():
        missing_fields.append("Job Description")
    if not uploaded_files:
        missing_fields.append("Upload Resumes")

    form_complete = len(missing_fields) == 0

    _, button_col, _ = st.columns([2.1, 1.4, 2.1])
    with button_col:
        with st.container(key="analysis_button_ready" if form_complete else "analysis_button_disabled"):
            start_analysis = st.button(
                "✧ RUN AI ANALYSIS",
                type="primary",
                use_container_width=True,
                disabled=not form_complete
            )

    if not form_complete:
        missing_text = ", ".join(missing_fields)
        st.warning(f"Please complete the required information: {missing_text}.")

    if start_analysis:
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

            extracted_text = extract_file_content(item)

            if not extracted_text:
                st.warning(f"No readable text found in {item.name}. Skipping this file.")
                progress_indicator.progress((idx + 1) / total_items)
                continue

            resume_email = extract_email_from_text(extracted_text)
            resume_cgpa = extract_cgpa_from_text(extracted_text)

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

            if isinstance(ai_payload_json, dict):
                if resume_email and not find_email_from_data(ai_payload_json):
                    ai_payload_json["candidate_email"] = resume_email
                if resume_cgpa and not first_present(ai_payload_json, ["cgpa", "gpa", "CGPA", "academic_cgpa"], ""):
                    ai_payload_json["cgpa"] = resume_cgpa

            runtime_cache[c_name] = ai_payload_json
            progress_indicator.progress((idx + 1) / total_items)

        st.session_state.pipeline_records = runtime_cache
        st.session_state.page_router = "results"
        st.rerun()




elif st.session_state.page_router == "technology":

    st.markdown("""
        <div class="tech-title">TECHNOLOGY BEHIND 4-BITS IR</div>
        <div class="tech-subtitle">Enterprise-grade AI recruitment technology powered by advanced machine learning<br>and natural language processing</div>
    """, unsafe_allow_html=True)

    stat_col1, stat_col2, stat_col3 = st.columns(3, gap="large")

    with stat_col1:
        st.markdown("""
        <div class="tech-stat-card">
            <div class="tech-stat-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="7" y="7" width="10" height="10" rx="2"></rect>
                    <path d="M9 1v4"></path><path d="M15 1v4"></path><path d="M9 19v4"></path><path d="M15 19v4"></path>
                    <path d="M1 9h4"></path><path d="M1 15h4"></path><path d="M19 9h4"></path><path d="M19 15h4"></path>
                </svg>
            </div>
            <div class="tech-stat-label">AI Models</div>
            <div class="tech-stat-value">Advanced NLP</div>
        </div>
        """, unsafe_allow_html=True)

    with stat_col2:
        st.markdown("""
        <div class="tech-stat-card purple">
            <div class="tech-stat-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <ellipse cx="12" cy="5" rx="8" ry="3"></ellipse>
                    <path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"></path>
                    <path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"></path>
                </svg>
            </div>
            <div class="tech-stat-label">Processing Speed</div>
            <div class="tech-stat-value">&lt; 2 seconds</div>
        </div>
        """, unsafe_allow_html=True)

    with stat_col3:
        st.markdown("""
        <div class="tech-stat-card blue">
            <div class="tech-stat-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M3 17l6-6 4 4 8-8"></path>
                    <path d="M14 7h7v7"></path>
                </svg>
            </div>
            <div class="tech-stat-label">Accuracy Rate</div>
            <div class="tech-stat-value">94%+</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="tech-feature-card">
        <div class="tech-feature-row">
            <div class="tech-feature-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 3a3 3 0 0 0-3 3v1a3 3 0 0 0-3 3v1a3 3 0 0 0 0 6 3 3 0 0 0 3 3h6a3 3 0 0 0 3-3 3 3 0 0 0 0-6v-1a3 3 0 0 0-3-3V6a3 3 0 0 0-3-3z"></path>
                    <path d="M9 7v10"></path><path d="M15 7v10"></path><path d="M9 12h6"></path>
                </svg>
            </div>
            <div>
                <div class="tech-feature-title">AI Resume Analysis Engine</div>
                <div class="tech-feature-text">Our advanced AI system reads and analyzes resumes with deep learning algorithms. It intelligently compares resume content against job requirements, automatically identifying the most suitable candidates based on comprehensive skill matching, experience evaluation, and qualification assessment.</div>
            </div>
        </div>
    </div>

    <div class="tech-feature-card purple">
        <div class="tech-feature-row">
            <div class="tech-feature-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <path d="M14 2v6h6"></path>
                    <circle cx="11" cy="15" r="3"></circle>
                    <path d="M13.3 17.3L16 20"></path>
                </svg>
            </div>
            <div>
                <div class="tech-feature-title">Resume Parsing Technology</div>
                <div class="tech-feature-text">Advanced document processing technology extracts structured information from PDF and DOCX resumes with high accuracy. Our parsing engine converts unstructured resume documents into organized, machine-readable data that enables AI-powered analysis and intelligent candidate evaluation.</div>
            </div>
        </div>
    </div>

    <div class="tech-feature-card pink">
        <div class="tech-feature-row">
            <div class="tech-feature-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M9 18h6"></path><path d="M10 22h4"></path>
                    <path d="M8 14a6 6 0 1 1 8 0c-.9.7-1.5 1.8-1.7 3H9.7C9.5 15.8 8.9 14.7 8 14z"></path>
                </svg>
            </div>
            <div>
                <div class="tech-feature-title">Intelligent Insights</div>
                <div class="tech-feature-text">AI-generated insights provide deep candidate intelligence including strength analysis, skill gap identification, academic performance (CGPA/GPA), competition achievements, hackathon participation, and open-source contributions. The system automatically generates tailored interview questions based on each candidate's profile and identified weaknesses.</div>
            </div>
        </div>
    </div>

    <div class="tech-feature-card green">
        <div class="tech-feature-row">
            <div class="tech-feature-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
            </div>
            <div>
                <div class="tech-feature-title">Privacy &amp; Security</div>
                <div class="tech-feature-text">All uploaded resumes are processed exclusively for screening and analysis purposes. We implement enterprise-grade security protocols with end-to-end encryption, ensuring candidate data remains confidential. Our privacy-first architecture means your data is never sold, shared with third parties, or used for any purpose beyond talent evaluation.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(key="tech_cta_card"):
        st.markdown("""
            <div class="tech-cta-title">Ready to Transform Your Hiring Process?</div>
            <div class="tech-cta-text">Experience the power of AI-driven recruitment and make smarter hiring decisions in seconds</div>
        """, unsafe_allow_html=True)

        _, cta_col, _ = st.columns([2.0, 1.4, 2.0])
        with cta_col:
            if st.button("Start Screening Candidates", key="tech_start_button", use_container_width=True):
                st.session_state.page_router = "inputs"
                st.rerun()


elif st.session_state.page_router == "contact":

    st.markdown("""
        <div class="contact-title">CONTACT 4-BITS IR</div>
        <div class="contact-subtitle">Get in touch with our team for support, inquiries, or demo requests</div>
    """, unsafe_allow_html=True)

    info_col1, info_col2, info_col3 = st.columns(3, gap="large")

    with info_col1:
        st.markdown("""
        <div class="contact-info-card">
            <div class="contact-info-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="3" y="5" width="18" height="14" rx="2"></rect>
                    <path d="M3 7l9 6 9-6"></path>
                </svg>
            </div>
            <div class="contact-info-label">Email</div>
            <div class="contact-info-value">4bits.recruiter@gmail.com</div>
        </div>
        """, unsafe_allow_html=True)

    with info_col2:
        st.markdown("""
        <div class="contact-info-card">
            <div class="contact-info-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2A19.8 19.8 0 0 1 3.1 5.18 2 2 0 0 1 5.11 3h3a2 2 0 0 1 2 1.72c.12.9.33 1.77.63 2.61a2 2 0 0 1-.45 2.11L9.1 10.9a16 16 0 0 0 4 4l1.46-1.19a2 2 0 0 1 2.11-.45c.84.3 1.71.51 2.61.63A2 2 0 0 1 22 16.92z"></path>
                </svg>
            </div>
            <div class="contact-info-label">Phone</div>
            <div class="contact-info-value">+60 12-345 6789</div>
        </div>
        """, unsafe_allow_html=True)

    with info_col3:
        st.markdown("""
        <div class="contact-info-card">
            <div class="contact-info-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M21 10c0 7-9 12-9 12S3 17 3 10a9 9 0 1 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                </svg>
            </div>
            <div class="contact-info-label">Location</div>
            <div class="contact-info-value">Malaysia</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    left_contact, right_contact = st.columns([1, 1], gap="large")

    with left_contact:
        with st.container(key="contact_form_card"):
            st.markdown('<div class="contact-panel-title-cyan">Send Us a Message</div>', unsafe_allow_html=True)

            contact_name = st.text_input("Name", placeholder="Your full name", key="contact_name")
            contact_email = st.text_input("Email", placeholder="your.email@example.com", key="contact_email")
            contact_subject = st.text_input("Subject", placeholder="What is this regarding?", key="contact_subject")
            contact_message = st.text_area("Message", placeholder="Tell us more about your inquiry...", height=190, key="contact_message")

            body_text = f"""Name: {contact_name}\nEmail: {contact_email}\n\nMessage:\n{contact_message}"""
            send_url = gmail_compose_url(
                "4bits.recruiter@gmail.com",
                contact_subject or "Inquiry from 4-Bits IR Contact Page",
                body_text
            )

            st.markdown(f"""
            <a class="contact-send-link" href="{send_url}" target="_blank">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 2L11 13"></path><path d="M22 2l-7 20-4-9-9-4 20-7z"></path></svg>
                <span>Send Message</span>
            </a>
            """, unsafe_allow_html=True)

    with right_contact:
        with st.container(key="contact_actions_card"):
            st.markdown('<div class="contact-panel-title-purple">Quick Actions</div>', unsafe_allow_html=True)

            open_gmail_url = gmail_compose_url("4bits.recruiter@gmail.com")
            support_url = gmail_compose_url("4bits.recruiter@gmail.com", "Support Request - 4-Bits IR", "Hi 4-Bits IR team,\n\nI need support regarding:")
            demo_url = gmail_compose_url("4bits.recruiter@gmail.com", "Demo Request - 4-Bits IR", "Hi 4-Bits IR team,\n\nI would like to request a demo for the Intelligent Recruiter system.")

            st.markdown(f"""
            <a class="contact-action-link blue" href="{open_gmail_url}" target="_blank">
                <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"></rect><path d="M3 7l9 6 9-6"></path></svg>
                <span>Open Gmail</span>
            </a>
            <div style="height:1.05rem;"></div>
            <a class="contact-action-link pink" href="{support_url}" target="_blank">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"></path></svg>
                <span>Contact Support</span>
            </a>
            <div style="height:1.05rem;"></div>
            <a class="contact-action-link teal" href="{demo_url}" target="_blank">
                <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"></rect><path d="M16 2v4"></path><path d="M8 2v4"></path><path d="M3 10h18"></path></svg>
                <span>Request Demo</span>
            </a>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(key="contact_help_card"):
            st.markdown("""
            <div class="contact-help-row">
                <div class="contact-help-icon">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"></path>
                        <path d="M19 15l.9 2.6 2.6.9-2.6.9L19 23l-.9-2.6-2.6-.9 2.6-.9L19 15z"></path>
                    </svg>
                </div>
                <div>
                    <div class="contact-help-title">Need help with candidate screening?</div>
                    <div class="contact-help-text">Our team is ready to assist with resume analysis, AI matching, and hiring workflow support.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(key="contact_hours_card"):
            st.markdown("""
            <div class="contact-hours-title">Support Hours</div>
            <div class="contact-hours-row"><span>Monday - Friday</span><span class="contact-hours-value">9:00 AM - 6:00 PM MYT</span></div>
            <div class="contact-hours-row"><span>Weekend</span><span class="contact-hours-value">Limited Support</span></div>
            <div class="contact-hours-row"><span>Response Time</span><span class="contact-hours-value">Within 24 hours</span></div>
            """, unsafe_allow_html=True)

elif st.session_state.page_router == "results":

    dataset = st.session_state.pipeline_records or {}

    st.markdown("""
        <div class="results-title">CANDIDATE MATCH ANALYSIS</div>
        <div class="results-subtitle">AI-powered intelligent ranking and insights</div>
    """, unsafe_allow_html=True)

    if st.button("Run New Evaluation", key="back_results", use_container_width=True):
        st.session_state.page_router = "inputs"
        st.session_state.pipeline_records = None
        st.rerun()

    if not dataset:
        st.info("No candidate evaluation records found. Please run a new analysis first.")
    else:
        candidate_rows = []
        for name, data in dataset.items():
            if not isinstance(data, dict):
                data = {"score": 0, "ai_assessment": str(data)}
            try:
                score_val = int(float(data.get("score", 0)))
            except Exception:
                score_val = 0
            score_val = max(0, min(score_val, 100))
            candidate_rows.append((name, data, score_val))

        total_candidates = len(candidate_rows)
        avg_score = round(sum(row[2] for row in candidate_rows) / max(total_candidates, 1))
        top_candidate = max(candidate_rows, key=lambda row: row[2])[0] if candidate_rows else "N/A"
        above_80 = sum(1 for _, _, score in candidate_rows if score >= 80)

        m1, m2, m3, m4 = st.columns(4, gap="large")
        with m1:
            st.markdown(textwrap.dedent(f"""
            <div class="metric-card blue">
                <div class="metric-label">
                    <svg class="metric-icon" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                    <span>Total Candidates</span>
                </div>
                <div class="metric-value">{total_candidates}</div>
            </div>
            """).strip(), unsafe_allow_html=True)
        with m2:
            st.markdown(textwrap.dedent(f"""
            <div class="metric-card indigo">
                <div class="metric-label">
                    <svg class="metric-icon" viewBox="0 0 24 24"><path d="M3 17l6-6 4 4 8-8"></path><path d="M14 7h7v7"></path></svg>
                    <span>Average Score</span>
                </div>
                <div class="metric-value">{avg_score}%</div>
            </div>
            """).strip(), unsafe_allow_html=True)
        with m3:
            st.markdown(textwrap.dedent(f"""
            <div class="metric-card purple">
                <div class="metric-label">
                    <svg class="metric-icon" viewBox="0 0 24 24"><path d="M12 15l-3.5 6-.8-4.3L3.5 15l3.5-6"></path><path d="M12 15l3.5 6 .8-4.3 4.2-1.7-3.5-6"></path><circle cx="12" cy="8" r="5"></circle></svg>
                    <span>Top Candidate</span>
                </div>
                <div class="metric-value" style="font-size:1.65rem;letter-spacing:-0.045em;">{html_escape(top_candidate)}</div>
            </div>
            """).strip(), unsafe_allow_html=True)
        with m4:
            st.markdown(textwrap.dedent(f"""
            <div class="metric-card pink">
                <div class="metric-label">
                    <svg class="metric-icon" viewBox="0 0 24 24"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"></path><path d="M19 15l.9 2.6 2.6.9-2.6.9L19 23l-.9-2.6-2.6-.9 2.6-.9L19 15z"></path></svg>
                    <span>Above 80%</span>
                </div>
                <div class="metric-value">{above_80}</div>
            </div>
            """).strip(), unsafe_allow_html=True)

        st.markdown('<div class="results-filter-bar">', unsafe_allow_html=True)
        search_col, filter_col = st.columns([5, 1.2], gap="large")
        with search_col:
            search_text = st.text_input("Search candidates", placeholder="Search candidates...", label_visibility="collapsed")
        with filter_col:
            score_filter = st.selectbox(
                "All Scores",
                ["All Scores", "90% and above", "80% and above", "70% and above", "50% and below"],
                label_visibility="collapsed"
            )
        st.markdown('</div>', unsafe_allow_html=True)

        def score_filter_pass(score):
            if score_filter == "90% and above":
                return score >= 90
            if score_filter == "80% and above":
                return score >= 80
            if score_filter == "70% and above":
                return score >= 70
            if score_filter == "50% and below":
                return score <= 50
            return True

        visible_rows = []
        for name, data, score in sorted(candidate_rows, key=lambda row: row[2], reverse=True):
            if search_text and search_text.lower() not in name.lower():
                continue
            if not score_filter_pass(score):
                continue
            visible_rows.append((name, data, score))

        if not visible_rows:
            st.warning("No candidates match the selected filter.")

        for index, (name, data, score_val) in enumerate(visible_rows):
            skills = clean_list_value(first_present(data, ["skills", "languages", "technical_skills", "identified_skills"], ""))
            if not skills:
                skills = ["Skills N/A"]

            cgpa = first_present(data, ["cgpa", "gpa", "CGPA", "academic_cgpa"], "N/A")
            competition_items = clean_list_value(first_present(data, ["competitions", "competition", "awards", "achievements"], ""))
            competition = ", ".join(competition_items) if competition_items else "N/A"
            strengths = clean_list_value(first_present(data, ["strengths", "qualified", "qualifications", "qualification_summary"], ""))
            weaknesses = clean_list_value(first_present(data, ["weaknesses", "areas_for_development", "missing_skills"], ""))
            ai_assessment = first_present(data, ["ai_assessment", "assessment", "summary", "qualified"], "No AI assessment provided.")
            questions = clean_list_value(first_present(data, ["interview_questions", "questions", "generated_interview_questions"], ""))
            email = find_email_from_data(data)
            gmail_url = candidate_mail_link(email)

            exp_text = first_present(data, ["experience", "years_experience", "experience_summary"], "Candidate profile summary")
            edu_text = first_present(data, ["education", "degree", "university"], "")
            meta_line = html_escape(exp_text)
            if edu_text and edu_text != "N/A":
                meta_line += " • " + html_escape(edu_text)

            score_width = max(0, min(score_val, 100))
            contact_hint = html_escape(email if email else "Gmail")

            safe_name = re.sub(r"[^A-Za-z0-9_]+", "_", str(name))[:45] or str(index)
            detail_state_key = f"details_open_{safe_name}_{index}"
            question_state_key = f"questions_open_{safe_name}_{index}"
            if detail_state_key not in st.session_state:
                st.session_state[detail_state_key] = False
            if question_state_key not in st.session_state:
                st.session_state[question_state_key] = False

            with st.container(key=f"candidate_card_{safe_name}_{index}"):
                top_left, top_right = st.columns([5, 1], gap="large")
                with top_left:
                    st.markdown(f'<div class="candidate-name">{html_escape(name)}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="candidate-meta">{meta_line}</div>', unsafe_allow_html=True)
                with top_right:
                    st.markdown(f'<div class="candidate-score">{score_val}%</div><div class="candidate-score-label">Match Score</div>', unsafe_allow_html=True)

                st.markdown(f'<div class="score-track"><div class="score-fill" style="width:{score_width}%;"></div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="pill-row">{render_skill_pills(skills)}</div>', unsafe_allow_html=True)

                action_col, contact_col = st.columns([6, 0.65], gap="small")
                with action_col:
                    button_label = "Hide Details" if st.session_state[detail_state_key] else "View Analysis"
                    if st.button(button_label, key=f"view_analysis_{safe_name}_{index}", use_container_width=True):
                        st.session_state[detail_state_key] = not st.session_state[detail_state_key]
                        st.rerun()
                with contact_col:
                    st.markdown(f'<a class="contact-link" href="{gmail_url}" target="_blank">✉ Contact</a><div class="contact-email-hint">{contact_hint}</div>', unsafe_allow_html=True)

                if st.session_state[detail_state_key]:
                    st.markdown('<div class="candidate-divider"></div>', unsafe_allow_html=True)

                    st.markdown('<div class="detail-heading-green">● Strengths</div>', unsafe_allow_html=True)
                    st.markdown(render_detail_lines(strengths, "✓", "Strength details not available."), unsafe_allow_html=True)

                    st.markdown('<div class="detail-heading-orange">● Areas for Development</div>', unsafe_allow_html=True)
                    st.markdown(render_detail_lines(weaknesses, "•", "Weakness details not available."), unsafe_allow_html=True)

                    st.markdown('<div class="detail-heading-blue">● Candidate Details</div>', unsafe_allow_html=True)
                    detail_1, detail_2 = st.columns(2, gap="medium")
                    with detail_1:
                        st.markdown(f'<div class="detail-info-card"><div class="detail-info-label">CGPA / GPA</div><div class="detail-info-value">{html_escape(cgpa)}</div></div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="detail-info-card"><div class="detail-info-label">Skills</div><div class="detail-info-value">{html_escape(", ".join(skills))}</div></div>', unsafe_allow_html=True)
                    with detail_2:
                        st.markdown(f'<div class="detail-info-card"><div class="detail-info-label">Competition / Achievements</div><div class="detail-info-value">{html_escape(competition)}</div></div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="detail-info-card"><div class="detail-info-label">Gmail Account</div><div class="detail-info-value">{html_escape(email or "No email detected")}</div></div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="ai-assessment-box"><div class="ai-title">AI Assessment</div><div class="detail-line">{html_escape(ai_assessment)}</div></div>', unsafe_allow_html=True)

                    if st.button("Generate Interview Questions", key=f"generate_questions_{safe_name}_{index}", use_container_width=True):
                        st.session_state[question_state_key] = True

                    if st.session_state[question_state_key]:
                        display_questions = questions
                        if not display_questions:
                            main_skill = skills[0] if skills and skills[0] != "Skills N/A" else "the required technical skills"
                            weak_area = weaknesses[0] if weaknesses else "the role requirements"
                            display_questions = [
                                f"Can you explain how your experience with {main_skill} matches this position?",
                                "Describe one project that best demonstrates your technical problem-solving ability.",
                                f"What steps would you take to improve in this area: {weak_area}?",
                                "Tell us about a time you worked under pressure or handled a difficult technical challenge.",
                                "Why do you think you are a strong fit for this role compared with other candidates?"
                            ]

                        st.markdown('<div class="interview-box"><div class="ai-title">Generated Interview Questions</div></div>', unsafe_allow_html=True)
                        for q_idx, q_text in enumerate(display_questions[:6]):
                            st.markdown(f'<div class="detail-line">{q_idx + 1}. {html_escape(q_text)}</div>', unsafe_allow_html=True)


st.markdown('<br><br><hr style="border-color:#1E293B;">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:#555555;font-size:0.8rem;padding-bottom:1rem;">'
    '© 2026 Intelligent Recruiter Project Inc. All rights reserved.</div>',
    unsafe_allow_html=True
)
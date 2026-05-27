@echo off
setlocal

if not exist .venv (
    python -m venv .venv
)

.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\streamlit.exe run run_app.py

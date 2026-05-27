# The Intelligent Recruiter - 4-Bits

An AI-powered talent intelligence system that helps hiring managers screen resumes, compare candidates against job requirements, and generate candidate match insights.

This project was developed for the AI Marathon 2026 preliminary round challenge.

## Problem Statement

Traditional job boards are static. The Intelligent Recruiter bridges the gap between diverse talent and hiring managers by taking a job description and a pool of candidate data, then identifying the best matches.

## Features

- Enter job requirements
- Upload candidate resumes in PDF or DOCX format
- Run AI-powered resume analysis
- View candidate match scores and ranking
- Review strengths, weaknesses, CGPA/GPA, skills, competitions, and AI assessment
- Generate candidate-specific interview questions
- Contact candidates through Gmail

## Tech Stack

- Python
- Streamlit
- Chutes AI API
- OpenAI-compatible Python client
- PDF resume parsing using `pypdf`
- DOCX resume parsing using Python standard libraries
- HTML/CSS styling inside Streamlit

## Project Structure

```text
AI-MARATHON/
├── .env.example
├── .gitignore
├── README.md
├── chutes.py
├── requirements.txt
├── run_app.py
└── start.bat
```

## Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

```env
CHUTES_API_KEY=your_chutes_api_key_here
CHUTES_BASE_URL=https://llm.chutes.ai/v1
```

Do not commit your real `.env` file or live API keys to GitHub.

## Local Setup

### Option 1: Run With start.bat

On Windows, double-click:

```text
start.bat
```

This installs dependencies and starts the Streamlit app.

### Option 2: Manual Run

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\streamlit.exe run run_app.py
```

Open the local app:

```text
http://localhost:8501
```

## Chutes Setup

This project uses Chutes through an OpenAI-compatible API endpoint.

If your own Chutes Pro access is not active yet, use a valid team-provided or organizer-provided Chutes API key in your local `.env` file. The repository does not include any live API key.

## Model Restriction Note

The project does not use OpenClaw or Hermes, as those models/tools are banned by the hackathon rules.

## How to Use the System

1. Open the app.
2. Click **Start Screening**.
3. Fill in the job requirements.
4. Upload candidate resumes.
5. Click **Run AI Analysis**.
6. View the Candidate Match Analysis dashboard.
7. Click **View Analysis** to inspect each candidate.
8. Click **Generate Interview Questions** to generate candidate-specific interview questions.
9. Click **Contact** to open Gmail for candidate communication.

## Submission Notes

Before submitting:

- Confirm the app runs locally
- Confirm `.env` is not committed
- Include this GitHub repository link
- Include the pitch deck link
- Include the demo video link
- Ensure the final commit is before 13:00:00 on May 27, 2026

## Team

**Team Name:** 4-Bits  
**Project Title:** The Intelligent Recruiter  
**Challenge:** Build an agent that takes a job description and a pool of candidate data, then identifies the best matches.

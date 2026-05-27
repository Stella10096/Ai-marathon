# The Intelligent Recruiter — 4-Bits

An AI-powered talent intelligence system that helps hiring managers screen resumes, compare candidates against job requirements, and generate candidate match insights.

This project was developed for the **APU Artificial Intelligence Club Preliminary Round** challenge.

---

## Project Overview

Traditional job boards are static and often make it difficult for hiring managers to quickly identify the best candidates from a diverse talent pool.  
**The Intelligent Recruiter** bridges this gap by allowing users to:

- Enter job requirements
- Upload candidate resumes in PDF or DOCX format
- Run AI-powered resume analysis
- View candidate match scores
- Review strengths, weaknesses, CGPA/GPA, skills, competitions, and AI assessment
- Generate interview questions
- Contact candidates through Gmail

---

## Tech Stack

- Python
- Streamlit
- Chutes AI API
- OpenAI-compatible API client
- PDF resume parsing using `pypdf`
- DOCX resume parsing using Python standard libraries
- HTML/CSS styling inside Streamlit

---

## Project Structure

```text
AI-MARATHON/
├── .env
├── .gitignore
├── chutes.py
├── run_app.py
├── venv/
└── __pycache__/
```

Important files:

| File | Purpose |
|---|---|
| `run_app.py` | Main Streamlit application |
| `chutes.py` | Handles AI API connection and resume analysis |
| `.env` | Stores API key and base URL locally |
| `.gitignore` | Prevents private/local files from being uploaded |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Stella10096/Ai-marathon.git
cd Ai-marathon
```

---

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Required Packages

```bash
pip install streamlit pypdf openai python-dotenv
```

Optional: create a `requirements.txt` file using:

```bash
pip freeze > requirements.txt
```

Then future users can install with:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

This project uses a `.env` file for API configuration.

Create a file named `.env` in the project root folder:

```text
AI-MARATHON/
├── .env
├── chutes.py
└── run_app.py
```

Inside `.env`, add:

```env
CHUTES_API_KEY=your_chutes_api_key_here
CHUTES_BASE_URL=your_chutes_base_url_here
```

Example format:

```env
CHUTES_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
CHUTES_BASE_URL=https://api.chutes.ai/v1
```

Do not share or upload your real `.env` file to GitHub.

---

## Recommended `.gitignore`

Make sure your `.gitignore` includes:

```gitignore
.env
venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

This protects API keys, virtual environments, and temporary files from being uploaded.

---

## How to Run the App

After activating the virtual environment and setting up `.env`, run:

```bash
streamlit run run_app.py
```

The app will open in your browser, usually at:

```text
http://localhost:8501
```

---

## How to Use the System

1. Open the app.
2. Click **Start Screening**.
3. Fill in the job requirements:
   - Position Title
   - Required Skills
   - Experience Level
   - Preferred Technologies
   - Job Description
4. Upload candidate resumes in PDF or DOCX format.
5. Click **Run AI Analysis**.
6. View the Candidate Match Analysis dashboard.
7. Click **View Analysis** to inspect each candidate.
8. Click **Generate Interview Questions** to generate candidate-specific interview questions.
9. Click **Contact** to open Gmail for candidate communication.

---

## Key Features

### AI Screening Command Center
Allows users to input job requirements and upload multiple resumes.

### Candidate Match Analysis
Displays AI-generated scores, ranking, strengths, weaknesses, skills, CGPA/GPA, competitions, and assessment.

### Technology Page
Explains the system’s resume parsing, AI analysis, intelligent insights, and privacy/security approach.

### Contact Page
Provides support contact details, Gmail quick actions, and inquiry form.

---

## Notes for Organizers

The system requires a valid Chutes API key and base URL to run live AI analysis.

If the API key is not configured, the app may fail to connect to the AI service.  
For judging or demo purposes, please ensure the `.env` file is configured before running:

```env
CHUTES_API_KEY=your_chutes_api_key_here
CHUTES_BASE_URL=your_chutes_base_url_here
```

---

## Team

**Team Name:** 4-Bits  
**Project Title:** The Intelligent Recruiter  
**Challenge:** Build an agent that takes a job description and a pool of candidate data, then identifies the best matches.

---

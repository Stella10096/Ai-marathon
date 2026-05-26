import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# 1. CRITICAL: Load the environment variables from the .env file at the root
load_dotenv()

# 2. Initialize Chutes connection using shared client environment variables
client = OpenAI(
    api_key=os.getenv("CHUTES_API_KEY"),
    base_url=os.getenv("CHUTES_BASE_URL")
)

def parse_llm_json_safely(raw_text):
    try:
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return json.loads(raw_text)
    except Exception:
        return {
            "score": 50,
            "qualified": "System warning: JSON decoding failed. Profile requires manual verification.",
            "languages": "Unknown Stack",
            "competitions": "Data extraction incomplete",
            "weaknesses": "Potential formatting discrepancy found in raw profile source.",
            "interview_questions": [
                "Could you walk us through your core system architecture?",
                "How do you maintain structural integrity within distributed environments?"
            ]
        }

def analyze_candidate_resume(job_title, specifications, candidate_id, raw_resume_text):
    system_instruction = (
        "You are an expert automated recruiting agent. Your task is to analyze the candidate. "
        "Output must be a strictly formatted JSON object block. "
        "Do not provide conversational greetings or normal prose text notes outside of the JSON block elements.\n\n"
        "REQUIRED OUTPUT SCHEMA FORMAT:\n"
        "{\n"
        "  \"score\": 90,\n"
        "  \"qualified\": \"Explicit details on why this specific applicant matches the operational criteria.\",\n"
        "  \"languages\": \"List programming languages and core tool frameworks discovered.\",\n"
        "  \"competitions\": \"List specific industry hackathons, competitive records, or projects found.\",\n"
        "  \"weaknesses\": \"Detail critical keyword deficits or structural experience missing gaps.\",\n"
        "  \"interview_questions\": [\"Question 1 targeting weakness\", \"Question 2\", \"Question 3\"]\n"
        "}"
    )
    
    user_payload = f"TARGET_ROLE: {job_title}\nCOMPETENCY_CRITERIA: {specifications}\nCANDIDATE_ID: {candidate_id}\nSOURCE_CORPUS:\n{raw_resume_text}"
    
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct-TEE",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_payload}
        ],
        temperature=0.2
    )
    return parse_llm_json_safely(response.choices[0].message.content)
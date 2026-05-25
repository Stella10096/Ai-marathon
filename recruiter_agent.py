import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load system configurations
load_dotenv()

# 2. Initialize the AI client using Chutes platform
client = OpenAI(
    api_key=os.getenv("CHUTES_API_KEY"),
    base_url=os.getenv("CHUTES_BASE_URL")
)

def match_resume_to_job(job_description, candidate_resume):
    print("AI Agent is analyzing the candidate profile, please wait...")
    
    # 3. Create a strict prompt for the AI agent
    system_prompt = (
        "You are an expert HR recruitment specialist. Your job is to analyze the given candidate resume "
        "against the job description. Provide an objective suitability score out of 100 and a brief justification summary."
    )
    
    user_content = f"""
    === JOB DESCRIPTION ===
    {job_description}

    === CANDIDATE RESUME ===
    {candidate_resume}
    """
    
    try:
        # 4. Request evaluation from the active TEE model on Chutes
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct-TEE",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during AI analysis: {e}"

if __name__ == "__main__":
    # 5. Mock Data for local testing (Job: Python Backend Engineer)
    mock_job = (
        "Role: Python Backend Developer. "
        "Required Skills: Python, SQL databases, Git version control, and building RESTful APIs."
    )
    
    # Mock Data (Candidate: Chim Shi Qi - strong match)
    mock_resume = (
        "Name: Chim Shi Qi. "
        "Technical Skills: Advanced Python coding, relational SQL database architecture, GitHub workflow design. "
        "Experience: Developed multi-service backend infrastructures and automated script tools."
    )
    
    # 6. Execute the matching agent
    evaluation_result = match_resume_to_job(mock_job, mock_resume)
    
    print("\n================ EVALUATION REPORT ================")
    print(evaluation_result)
    print("===================================================")
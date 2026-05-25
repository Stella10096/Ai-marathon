import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Initialize the Chutes client with local configurations
client = OpenAI(
    api_key=os.getenv("CHUTES_API_KEY"),
    base_url=os.getenv("CHUTES_BASE_URL")
)

def run_final_chat_test():
    print("Sending request to the selected Chutes model...")
    try:
        # 3. Create a chat completion using a verified model from your list
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct-TEE", 
            messages=[
                {
                    "role": "user", 
                    "content": "Hello! Please respond with 'Environment is 100% ready!' if you can read this."
                }
            ]
        )
        # 4. Print out the response from the AI
        print("\n[AI Response]:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"\nTest failed! Error message: {e}")

if __name__ == "__main__":
    run_final_chat_test()
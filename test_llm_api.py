import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Test LLM connection
try:
    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )
    
    print("Testing LLM API...")
    print(f"API Key: {os.getenv('LLM_API_KEY')[:10]}...")
    print(f"Base URL: {os.getenv('LLM_BASE_URL')}")
    print(f"Model: {os.getenv('LLM_MODEL')}")
    
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "user", "content": "Say 'Hello' in one word"}
        ],
        max_tokens=10
    )
    
    print("\n✅ LLM Response:")
    print(response.choices[0].message.content)
    print("\nLLM is working!")
    
except Exception as e:
    print(f"\n❌ LLM Error: {e}")
    import traceback
    traceback.print_exc()

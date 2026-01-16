"""
Test custom LLM connection
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_llm_connection():
    """Test if custom LLM is accessible"""
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")
    
    print("🔍 Testing Custom LLM Connection")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print(f"   API Key: {api_key[:20]}..." if api_key else "   API Key: Not set")
    print()
    
    # Test chat completion
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Say hello in Thai"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Try different response formats
        content = None
        reasoning = None
        if 'choices' in result and len(result['choices']) > 0:
            choice = result['choices'][0]
            if 'message' in choice:
                msg = choice['message']
                content = msg.get('content')
                reasoning = msg.get('reasoning_content')
            elif 'text' in choice:
                content = choice['text']
        elif 'content' in result:
            content = result['content']
        elif 'text' in result:
            content = result['text']
        
        if content or reasoning:
            print("✅ LLM Connection Successful!")
            if reasoning:
                print(f"   Reasoning: {reasoning}")
            if content:
                print(f"   Content: {content}")
            print()
            return True
        else:
            print("⚠️  LLM responded but format unexpected")
            print(f"   Response: {result}")
            print()
            return True  # Still consider it a success
        
    except Exception as e:
        print(f"❌ LLM Connection Failed!")
        print(f"   Error: {str(e)}")
        print()
        return False

def test_embedding_endpoint():
    """Test if embedding endpoint is accessible"""
    api_key = os.getenv("EMBEDDING_API_KEY")
    base_url = os.getenv("EMBEDDING_BASE_URL")
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    
    print("🔍 Testing Embedding Endpoint")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print()
    
    url = f"{base_url}/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "input": "สวัสดีครับ"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        embedding = result['data'][0]['embedding']
        
        print("✅ Embedding Endpoint Successful!")
        print(f"   Embedding dimension: {len(embedding)}")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Embedding Endpoint Failed!")
        print(f"   Error: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Custom LLM Connection Test")
    print("=" * 60)
    print()
    
    llm_ok = test_llm_connection()
    embedding_ok = test_embedding_endpoint()
    
    print("=" * 60)
    if llm_ok and embedding_ok:
        print("✅ All tests passed! Ready to use with Mem0")
    else:
        print("⚠️  Some tests failed. Please check your configuration")
    print("=" * 60)

"""
Test Mem0 via ngrok for Dify integration
"""
import requests
import json

NGROK_URL = "https://8f2a63040ff9.ngrok-free.app"
USER_ID = "dify_test_user"

def test_add_memory():
    print("=" * 60)
    print("1. Testing Add Memory")
    print("=" * 60)
    
    url = f"{NGROK_URL}/memory/add"
    payload = {
        "messages": "ผมชื่อสมชาย อายุ 25 ปี ชอบเขียนโปรแกรม Python และชอบกินพิซซ่า",
        "user_id": USER_ID
    }
    
    print(f"\n📤 Request to: {url}")
    print(f"Payload: {json.dumps(payload, ensure_ascii=False)}\n")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        print("✅ Success!")
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}\n")
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def test_search_memory():
    print("=" * 60)
    print("2. Testing Search Memory")
    print("=" * 60)
    
    url = f"{NGROK_URL}/memory/search"
    payload = {
        "query": "อายุและงานอดิเรกของผู้ใช้",
        "user_id": USER_ID,
        "limit": 5
    }
    
    print(f"\n📤 Request to: {url}")
    print(f"Payload: {json.dumps(payload, ensure_ascii=False)}\n")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        print("✅ Success!")
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}\n")
        
        # Show memories found
        if result.get('data'):
            print(f"📋 Found {len(result['data'])} memories:")
            for i, mem in enumerate(result['data'], 1):
                print(f"  {i}. {mem}")
        print()
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def test_get_all():
    print("=" * 60)
    print("3. Testing Get All Memories")
    print("=" * 60)
    
    url = f"{NGROK_URL}/memory/all"
    params = {"user_id": USER_ID}
    
    print(f"\n📤 Request to: {url}")
    print(f"Params: {params}\n")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        print("✅ Success!")
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}\n")
        
        # Show all memories
        if result.get('data'):
            print(f"📋 Total memories: {len(result['data'])}")
            for i, mem in enumerate(result['data'], 1):
                print(f"  {i}. {mem}")
        print()
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def test_health():
    print("=" * 60)
    print("0. Testing Health Check")
    print("=" * 60)
    
    url = f"{NGROK_URL}/health"
    
    print(f"\n📤 Request to: {url}\n")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
        print("✅ API is healthy!")
        print(f"Response: {result}\n")
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

if __name__ == "__main__":
    print("🧪 Testing Mem0 Local via ngrok for Dify")
    print(f"📡 URL: {NGROK_URL}")
    print(f"👤 User ID: {USER_ID}")
    print()
    
    # Test sequence
    health_ok = test_health()
    
    if health_ok:
        add_ok = test_add_memory()
        if add_ok:
            search_ok = test_search_memory()
            get_all_ok = test_get_all()
            
            print("=" * 60)
            print("🎉 All tests completed!")
            print("=" * 60)
            print("\n✅ Your Mem0 API is ready for Dify integration!")
            print("\n📝 Next steps:")
            print("1. Use these exact endpoints in Dify")
            print("2. Set user_id from Dify's {{user.id}} variable")
            print("3. Create a chatbot workflow with memory")
    else:
        print("❌ API not accessible. Check if:")
        print("  1. Docker containers are running")
        print("  2. ngrok tunnel is active")
        print("  3. URL is correct")

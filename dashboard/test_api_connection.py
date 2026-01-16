import requests
import json

BASE_URL = "http://localhost:8000"

def check_api():
    try:
        # 1. Health Check
        print("Checking API Health...")
        health = requests.get(f"{BASE_URL}/health")
        print(f"Health: {health.status_code} - {health.json()}")

        # 2. List All Memories (No User ID)
        print("\nFetching All Memories (No User ID)...")
        all_mems = requests.get(f"{BASE_URL}/memory/all")
        print(f"Status: {all_mems.status_code}")
        print(f"Data: {json.dumps(all_mems.json(), indent=2)}")

        # 3. Add a test memory to see if it persists
        print("\nAdding a test memory for 'test_user'...")
        add_res = requests.post(f"{BASE_URL}/memory/add", json={
            "messages": "This is a test memory for debugging dashboard connection.",
            "user_id": "test_user"
        })
        print(f"Add Result: {add_res.json()}")

        # 4. Fetch specific user memory
        print("\nFetching 'test_user' memories...")
        user_mems = requests.get(f"{BASE_URL}/memory/all?user_id=test_user")
        print(f"User Data: {json.dumps(user_mems.json(), indent=2)}")

        # 5. Check Admin Endpoint
        print("\nChecking Admin Endpoint (All Memories)...")
        admin_res = requests.get(f"{BASE_URL}/admin/memories")
        print(f"Admin Status: {admin_res.status_code}")
        if admin_res.status_code == 200:
            print(f"Admin Data: {json.dumps(admin_res.json(), indent=2)}")
        else:
            print(f"Admin Error: {admin_res.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to localhost:8000. Is the docker container running?")

if __name__ == "__main__":
    check_api()

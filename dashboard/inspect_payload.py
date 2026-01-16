import requests
import json

# Query Qdrant directly using the scroll API
url = "http://localhost:6333/collections/mem0/points/scroll"
params = {
    "limit": 3,
    "with_payload": True,
    "with_vectors": False
}

response = requests.post(url, json=params)
data = response.json()

if data.get("result"):
    points = data["result"]["points"]
    print(f"Found {len(points)} memory points\n")
    print("=" * 80)
    
    for i, point in enumerate(points, 1):
        print(f"\n📝 Memory #{i}")
        print("-" * 80)
        print(f"ID: {point['id']}")
        print(f"\nPayload Structure:")
        
        payload = point.get("payload", {})
        for key, value in payload.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"  • {key}: {value[:100]}... (truncated)")
            else:
                print(f"  • {key}: {value}")
        
        print("\n" + "=" * 80)
else:
    print("Error:", data)

"""
Simple test - using only embedding, no LLM
"""
import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

# Configure Mem0 - Embedding only (no LLM for testing)
config = {
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3"),
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": os.getenv("QDRANT_HOST", "localhost"),
            "port": int(os.getenv("QDRANT_PORT", 6333)),
        }
    },
}

print("=" * 60)
print("Mem0 Simple Test - Embedding Only")
print("=" * 60)
print()

try:
    # Initialize Memory
    print("🔄 Initializing Mem0...")
    m = Memory.from_config(config)
    print("✅ Mem0 initialized successfully!")
    print()
    
    # Add memories without LLM (raw text)
    print("📝 Adding memories...")
    
    memories_to_add = [
        {"text": "ผมชอบเขียนโปรแกรม Python", "user_id": "user001"},
        {"text": "ผมใช้ FastAPI สร้าง REST API", "user_id": "user001"},
        {"text": "ผมชอบใช้ Docker ในการ deploy แอป", "user_id": "user001"},
        {"text": "Mem0 เป็นตัวจัดการ memory ของ AI agent", "user_id": "user001"},
    ]
    
    for item in memories_to_add:
        result = m.add(item["text"], user_id=item["user_id"])
        print(f"  ✅ Added: {item['text'][:50]}...")
    
    print()
    print("=" * 60)
    print("✅ All memories added successfully!")
    print("=" * 60)
    print()
    
    # Search memories
    print("🔍 Searching memories...")
    print()
    
    search_queries = [
        "โปรแกรมภาษาไหน",
        "API",
        "deployment",
    ]
    
    for query in search_queries:
        print(f"Query: '{query}'")
        results = m.search(query, user_id="user001", limit=2)
        
        if results:
            for i, result in enumerate(results, 1):
                memory_text = result.get('memory', result.get('text', 'N/A'))
                print(f"  {i}. {memory_text}")
        else:
            print("  No results found")
        print()
    
    # Get all memories
    print("📋 All memories for user001:")
    all_memories = m.get_all(user_id="user001")
    for i, mem in enumerate(all_memories, 1):
        memory_text = mem.get('memory', mem.get('text', 'N/A'))
        print(f"  {i}. {memory_text}")
    
    print()
    print("=" * 60)
    print("🎉 Test completed successfully!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

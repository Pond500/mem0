"""
Simple test to verify Mem0 with local embeddings works
"""
import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

# Configure with explicit dimension
config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": os.getenv("LLM_MODEL", "ptm-oss-120b"),
            "api_key": os.getenv("LLM_API_KEY"),
            "openai_base_url": os.getenv("LLM_BASE_URL"),
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "BAAI/bge-m3",
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "mem0_test",
            "host": os.getenv("QDRANT_HOST", "localhost"),
            "port": int(os.getenv("QDRANT_PORT", 6333)),
            "embedding_model_dims": 1024,  # bge-m3 dimension
        }
    },
}

print("🚀 Initializing Mem0 with local embeddings...")
print(f"   Embedding Model: BAAI/bge-m3 (dimension: 1024)")
print(f"   LLM: {config['llm']['config']['model']}")
print(f"   Vector Store: Qdrant")
print()

try:
    m = Memory.from_config(config)
    print("✅ Mem0 initialized successfully!")
    print()
    
    # Test adding memory
    print("📝 Adding memory...")
    result = m.add("ผมชอบเขียนโปรแกรม Python และใช้ FastAPI", user_id="test_user")
    print(f"✅ Added: {result}")
    print()
    
    # Test search
    print("🔍 Searching memories...")
    results = m.search("programming preferences", user_id="test_user")
    print(f"✅ Found {len(results)} results:")
    for r in results:
        print(f"   - {r}")
    print()
    
    # Test get all
    print("📋 Getting all memories...")
    all_memories = m.get_all(user_id="test_user")
    print(f"✅ Total memories: {len(all_memories)}")
    for mem in all_memories:
        print(f"   - {mem}")
    print()
    
    print("=" * 60)
    print("🎉 All tests passed!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

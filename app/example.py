"""
Example usage of Mem0 with different scenarios
"""
import os
from dotenv import load_dotenv
from mem0 import Memory

# Load environment variables
load_dotenv()

# Configure Mem0 with Custom LLM and Local Embeddings
embedding_provider = os.getenv("EMBEDDING_PROVIDER", "huggingface")

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": os.getenv("LLM_MODEL", "ptm-oss-120b"),
            "api_key": os.getenv("LLM_API_KEY"),
            "openai_base_url": os.getenv("LLM_BASE_URL", "https://tokenmind.abdul.in.th/v1"),
        }
    },
    "embedder": {
        "provider": embedding_provider,
        "config": {
            "model": os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3"),
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": os.getenv("QDRANT_HOST", "localhost"),
            "port": int(os.getenv("QDRANT_PORT", 6333)),
            "embedding_model_dims": 1024,  # bge-m3 dimension - FIXED to 1024
        }
    },
}

# Initialize Memory
m = Memory.from_config(config)

def example_user_memory():
    """Example: Store and retrieve user preferences"""
    print("\n=== User Memory Example ===")
    
    # Add user memories
    m.add("I love Python programming and FastAPI", user_id="john")
    m.add("My favorite database is PostgreSQL", user_id="john")
    m.add("I prefer dark mode in my IDE", user_id="john")
    
    # Search user memories
    results = m.search("programming preferences", user_id="john")
    print("\nSearch results for 'programming preferences':")
    for result in results:
        print(f"  - {result}")
    
    # Get all user memories
    all_memories = m.get_all(user_id="john")
    print(f"\nTotal memories for user 'john': {len(all_memories)}")

def example_agent_memory():
    """Example: Store agent conversation context"""
    print("\n=== Agent Memory Example ===")
    
    # Store agent interactions
    m.add(
        "User asked about Docker setup for Mem0",
        agent_id="assistant_01",
        user_id="customer_123"
    )
    
    m.add(
        "Provided docker-compose.yml and Dockerfile examples",
        agent_id="assistant_01",
        user_id="customer_123"
    )
    
    # Retrieve agent memories
    memories = m.get_all(agent_id="assistant_01", user_id="customer_123")
    print(f"\nAgent memories: {len(memories)} items")

def example_session_memory():
    """Example: Store session-specific data"""
    print("\n=== Session Memory Example ===")
    
    # Store session data
    m.add(
        "User is debugging a Python application",
        run_id="session_001",
        user_id="developer_1"
    )
    
    m.add(
        "Found issue in database connection string",
        run_id="session_001",
        user_id="developer_1"
    )
    
    # Get session memories
    session_data = m.get_all(run_id="session_001")
    print(f"\nSession memories: {len(session_data)} items")

def example_memory_management():
    """Example: Update and delete memories"""
    print("\n=== Memory Management Example ===")
    
    # Add a memory
    result = m.add("Temporary test memory", user_id="test_user")
    memory_id = result['results'][0]['id'] if result.get('results') else None
    
    if memory_id:
        print(f"\nCreated memory with ID: {memory_id}")
        
        # Update the memory
        m.update(memory_id, "Updated memory content")
        print("Memory updated")
        
        # Get history
        history = m.history(memory_id)
        print(f"Memory history: {len(history)} versions")
        
        # Delete the memory
        m.delete(memory_id)
        print("Memory deleted")

if __name__ == "__main__":
    print("Mem0 Examples - Memory Management for AI Agents")
    print("=" * 50)
    
    try:
        example_user_memory()
        example_agent_memory()
        example_session_memory()
        example_memory_management()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure Qdrant is running and OPENAI_API_KEY is set")

import os
import json
import re
from dotenv import load_dotenv
from mem0 import Memory
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Mem0 API", description="Memory Management for AI Agents")

# Add CORS Middleware to allow requests from Dashboard (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mem0 Configuration with Custom LLM and Local Embeddings
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
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            "username": os.getenv("NEO4J_USER", "neo4j"),
            "password": os.getenv("NEO4J_PASSWORD", "password")
        }
    },
}

# Initialize Mem0
print("🚀 Starting Mem0 initialization...", flush=True)
print(f"   Neo4j URI: {os.getenv('NEO4J_URI', 'bolt://localhost:7687')}", flush=True)
print(f"   Neo4j User: {os.getenv('NEO4J_USER', 'neo4j')}", flush=True)
print(f"   Qdrant Host: {os.getenv('QDRANT_HOST', 'localhost')}", flush=True)
try:
    memory = Memory.from_config(config)
    print("✅ Mem0 initialized successfully with Graph Memory!", flush=True)
except Exception as e:
    print(f"❌ Failed to initialize Mem0: {e}", flush=True)
    import traceback
    traceback.print_exc()
    # Fallback: Initialize without graph_store
    print("⚠️ Falling back to Vector-only mode...", flush=True)
    config_fallback = {k: v for k, v in config.items() if k != "graph_store"}
    memory = Memory.from_config(config_fallback)
    print("✅ Mem0 initialized in Vector-only mode", flush=True)

# Request/Response Models
class AddMemoryRequest(BaseModel):
    messages: str
    user_id: Optional[str] = "default_user"  # Default if not provided
    agent_id: Optional[str] = None
    run_id: Optional[str] = None
    metadata: Optional[dict] = None

class SearchMemoryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"  # Default if not provided
    agent_id: Optional[str] = None
    run_id: Optional[str] = None
    limit: int = 10

class UpdateMemoryRequest(BaseModel):
    memory_id: str
    data: str

class DeleteMemoryRequest(BaseModel):
    memory_id: str

# API Endpoints
@app.get("/")
def read_root():
    return {
        "message": "Mem0 Memory API",
        "version": "1.0.0",
        "endpoints": {
            "add": "/memory/add",
            "search": "/memory/search",
            "get_all": "/memory/all",
            "update": "/memory/update",
            "delete": "/memory/delete",
            "history": "/memory/history/{memory_id}"
        }
    }

# Tag Generation Function
def generate_tags(text: str) -> list:
    """Generate tags for a memory using LLM"""
    try:
        # Initialize OpenAI client with custom base URL
        client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL", "https://tokenmind.abdul.in.th/v1")
        )
        
        # Create prompt for tag generation
        prompt = f"""Generate 2-4 short tags (single words) for this memory: "{text}"

Examples: work, food, sports, preference, tech, personal, travel, health

Return ONLY comma-separated tags, like: work, tech, personal

Tags:"""
        
        # Call LLM with more tokens
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "ptm-oss-120b"),
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        # Parse response - check both content and reasoning_content
        content = None
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, 'message'):
                # Try content first
                content = getattr(choice.message, 'content', None)
                # If content is None, try reasoning_content
                if not content:
                    content = getattr(choice.message, 'reasoning_content', None)
        
        if not content:
            print(f"Warning: LLM returned no content. Response: {response}")
            return ["general"]
            
        tags_text = content.strip()
        print(f"Tags text from LLM: {tags_text}")
        
        # Extract tags from response (handle various formats)
        # Remove common prefixes
        tags_text = tags_text.replace("Tags:", "").replace("tags:", "")
        
        # Clean and split tags
        tags = [tag.strip().lower() for tag in re.split(r'[,;]', tags_text) if tag.strip()]
        
        # Filter and limit
        tags = [t for t in tags if t and len(t) > 1 and len(t) < 20][:4]
        
        if not tags:
            print(f"Warning: No valid tags from: {tags_text}")
            return ["general"]
            
        print(f"✅ Generated tags: {tags}")
        return tags
        
    except Exception as e:
        print(f"❌ Tag generation error: {e}")
        import traceback
        traceback.print_exc()
        return ["general"]

@app.post("/memory/add")
def add_memory(request: AddMemoryRequest):
    """Add a new memory with auto-generated tags"""
    try:
        # 🔍 DEBUG: Log incoming request
        print("=" * 80)
        print("📥 INCOMING ADD MEMORY REQUEST from Dify:")
        print(f"   Messages: {request.messages}")
        print(f"   User ID: {request.user_id}")
        print(f"   Agent ID: {request.agent_id}")
        print(f"   Run ID: {request.run_id}")
        print(f"   Metadata: {request.metadata}")
        
        # 🔧 Smart Conversation ID Detection
        user_id = request.user_id
        
        # Priority 1: Check metadata for conversation_id
        if request.metadata and "conversation_id" in request.metadata:
            user_id = request.metadata["conversation_id"]
            print(f"   ✅ Using conversation_id from metadata: {user_id}")
        
        # Priority 2: Use agent_id if available
        elif request.agent_id and request.agent_id not in ["", "None", None]:
            user_id = f"agent_{request.agent_id}"
            print(f"   ✅ Using agent_id: {user_id}")
        
        # Priority 3: Use run_id if available
        elif request.run_id and request.run_id not in ["", "None", None]:
            user_id = f"run_{request.run_id}"
            print(f"   ✅ Using run_id: {user_id}")
        
        # Priority 4: If Dify sends literal template, generate new conversation ID
        elif user_id in ["{{sys.conversation_id}}", "{{conversation_id}}", None, ""]:
            import uuid
            user_id = f"conv_{str(uuid.uuid4())[:8]}"
            print(f"   ⚠️  Generated new Conversation ID: {user_id}")
        
        print("=" * 80)
        
        # Generate tags from memory text
        memory_text = request.messages if isinstance(request.messages, str) else request.messages[0].get("content", "") if request.messages else ""
        tags = generate_tags(memory_text)
        
        # Merge tags into metadata
        metadata = request.metadata or {}
        metadata["tags"] = tags
        # Store the conversation_id in metadata for tracking
        metadata["conversation_id"] = user_id
        
        result = memory.add(
            messages=request.messages,
            user_id=user_id,  # Use processed user_id
            agent_id=request.agent_id,
            run_id=request.run_id,
            metadata=metadata
        )
        return {"status": "success", "data": result, "tags": tags, "conversation_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/search")
def search_memory(request: SearchMemoryRequest):
    """Search for relevant memories"""
    try:
        # 🔍 DEBUG: Log incoming search request
        print("🔎 SEARCH REQUEST from Dify:")
        print(f"   Query: {request.query}")
        print(f"   User ID: {request.user_id}")
        print(f"   Limit: {request.limit}")
        
        # 🔧 Fix: Handle literal template string
        user_id = request.user_id
        if user_id in ["{{sys.conversation_id}}", "{{conversation_id}}", None, ""]:
            # For search, we can't generate new ID, use default
            user_id = "default_user"
            print(f"   ⚠️  Using default user_id for search: {user_id}")
        
        results = memory.search(
            query=request.query,
            user_id=user_id,
            agent_id=request.agent_id,
            run_id=request.run_id,
            limit=request.limit
        )
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/all")
def get_all_memories(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None
):
    """Get all memories"""
    try:
        results = memory.get_all(
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id
        )
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/memory/update")
def update_memory(request: UpdateMemoryRequest):
    """Update a memory"""
    try:
        result = memory.update(
            memory_id=request.memory_id,
            data=request.data
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memory/delete")
def delete_memory(request: DeleteMemoryRequest):
    """Delete a memory"""
    try:
        result = memory.delete(memory_id=request.memory_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/history/{memory_id}")
def get_memory_history(memory_id: str):
    """Get history of a memory"""
    try:
        result = memory.history(memory_id=memory_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# --- Admin Endpoints for Dashboard ---
from qdrant_client import QdrantClient

# Initialize Qdrant Client for Admin operations
qdrant_client = QdrantClient(
    host=os.getenv("QDRANT_HOST", "localhost"),
    port=int(os.getenv("QDRANT_PORT", 6333))
)

@app.get("/admin/memories")
def get_all_memories_admin(limit: int = 100, offset: Optional[str] = None):
    """Admin endpoint to fetch all memories directly from Qdrant"""
    try:
        response = qdrant_client.scroll(
            collection_name="mem0",
            limit=limit,
            with_payload=True,
            with_vectors=False,
            scroll_filter=None,
            offset=offset
        )
        
        points, next_page_offset = response
        
        results = []
        for point in points:
            payload = point.payload or {}
            
            # Extract metadata - check for tags in payload
            metadata = payload.get("metadata", {}) or {}
            # If tags are stored directly in payload (not in metadata), add them
            if "tags" in payload:
                metadata["tags"] = payload["tags"]
            
            # Map Qdrant payload to Memory format
            results.append({
                "id": str(point.id),
                "memory": payload.get("data", ""), # 'data' contains the memory text
                "user_id": payload.get("user_id", "unknown"),
                "agent_id": payload.get("agent_id"),
                "run_id": payload.get("run_id"),
                "metadata": metadata if metadata else None,
                "created_at": payload.get("created_at"),
                "updated_at": payload.get("updated_at"),
                "hash": payload.get("hash")
            })
            
        return {"status": "success", "data": {"results": results, "next_cursor": next_page_offset}}

    except Exception as e:
        print(f"Admin fetch error: {e}")
        # Return empty list on error to prevent dashboard crash
        return {"status": "error", "data": {"results": []}, "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

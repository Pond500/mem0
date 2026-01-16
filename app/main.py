import os
from dotenv import load_dotenv
from mem0 import Memory
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Mem0 API", description="Memory Management for AI Agents")

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
}

# Initialize Mem0
memory = Memory.from_config(config)

# Request/Response Models
class AddMemoryRequest(BaseModel):
    messages: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    run_id: Optional[str] = None
    metadata: Optional[dict] = None

class SearchMemoryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
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

@app.post("/memory/add")
def add_memory(request: AddMemoryRequest):
    """Add a new memory"""
    try:
        result = memory.add(
            messages=request.messages,
            user_id=request.user_id,
            agent_id=request.agent_id,
            run_id=request.run_id,
            metadata=request.metadata
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/search")
def search_memory(request: SearchMemoryRequest):
    """Search memories"""
    try:
        results = memory.search(
            query=request.query,
            user_id=request.user_id,
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

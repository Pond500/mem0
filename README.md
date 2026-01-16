# 🧠 Mem0 - Memory Management System for AI Agents

<div align="center">

![Mem0](https://img.shields.io/badge/Mem0-Memory%20Management-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Tests](https://img.shields.io/badge/Tests-13%2F13%20Passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Self-hosted memory management system for AI agents with semantic search, auto-extraction, and user isolation.**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API Reference](#-api-endpoints) • [Testing](#-testing)

</div>

---

## 🎯 Overview

Mem0 is a complete memory management solution for AI agents that provides:
- **Semantic Search**: Understand meaning, not just keywords
- **Auto-Extraction**: One input → Multiple memories automatically
- **User Isolation**: Per-user data separation
- **Custom LLM**: Use your own LLM endpoint
- **Local Embeddings**: BAAI/bge-m3 (1024 dimensions)
- **Vector Database**: Qdrant for efficient similarity search
- **REST API**: 6 endpoints for complete memory operations
- **Dify Integration**: Ready-to-use with Dify agents

Memory management system for AI agents using Mem0 and Qdrant vector database.

---

## ✨ Features

### Core Capabilities
- 🔍 **Semantic Search** - Understands context and meaning
- 💾 **Auto-Extraction** - Automatically creates multiple memories from text
- 👥 **User Isolation** - Complete data separation per user
- 🎯 **Relevance Scoring** - Results ranked by similarity (0.0 - 1.0)
- ⚡ **Fast & Efficient** - Optimized vector search with Qdrant
- 🔄 **Full CRUD** - Create, Read, Update, Delete operations

### Technical Stack
- 🐳 **Docker Compose** - Easy deployment
- 🐍 **Python 3.11** - Modern Python
- 🗄️ **Qdrant** - Vector database
- 🤖 **Custom LLM** - ptm-oss-120b (or your choice)
- 📊 **Local Embeddings** - BAAI/bge-m3 (1024 dims)
- 🚀 **FastAPI** - High-performance API
- 🔗 **Dify Ready** - Integration guides included

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Pond500/mem0.git
cd mem0
```

### 2. Setup Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your custom LLM configuration
# LLM_API_KEY=sk-WIqY-Eg2u9q24jnZ9jbFHw
# LLM_BASE_URL=https://tokenmind.abdul.in.th/v1
# LLM_MODEL=ptm-oss-120b
```

### 2. Start Services

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 3. Verify Services

- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Mem0 API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📦 Services

### Qdrant (Vector Database)
- **Ports**: 6333 (REST), 6334 (gRPC)
- **Dashboard**: http://localhost:6333/dashboard
- **Storage**: Persistent volume `qdrant_storage`

### Mem0 Application
- **Port**: 8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Usage

### Using the API

```bash
# Add a memory
curl -X POST "http://localhost:8000/memory/add" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": "User loves Python and FastAPI",
    "user_id": "user123"
  }'

# Search memories
curl -X POST "http://localhost:8000/memory/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "programming preferences",
    "user_id": "user123"
  }'

# Get all memories
curl "http://localhost:8000/memory/all?user_id=user123"
```

### Using Python

```python
from mem0 import Memory

# Configure with Docker Qdrant
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    },
}

m = Memory.from_config(config)

# Add memory
m.add("I love Python", user_id="user1")

# Search
results = m.search("programming", user_id="user1")
```

### Run Examples

```bash
# Test LLM connection
docker-compose exec mem0-app python test_llm.py

# Test local embedding model
docker-compose exec mem0-app python test_embedding.py

# Run example script
docker-compose exec mem0-app python example.py
```

## 🛠️ Development

### Local Development

```bash
# Install dependencies locally
pip install -r requirements.txt

# Set environment variables
export QDRANT_HOST=localhost
export QDRANT_PORT=6333
export LLM_API_KEY=sk-WIqY-Eg2u9q24jnZ9jbFHw
export LLM_BASE_URL=https://tokenmind.abdul.in.th/v1
export LLM_MODEL=ptm-oss-120b

# Test connection
python app/test_llm.py

# Run locally
python app/main.py
```

### Rebuild After Changes

```bash
# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## 📊 Monitoring

### Check Service Status

```bash
# View all services
docker-compose ps

# View logs
docker-compose logs -f mem0-app
docker-compose logs -f qdrant
```

### Check Qdrant Collections

```bash
# List collections
curl http://localhost:6333/collections
```

## 🧹 Cleanup

```bash
# Stop services
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_API_KEY` | Custom LLM API key (required) | - |
| `LLM_BASE_URL` | Custom LLM base URL | `https://tokenmind.abdul.in.th/v1` |
| `LLM_MODEL` | Custom LLM model name | `ptm-oss-120b` |
| `EMBEDDING_PROVIDER` | Embedding provider | `huggingface` |
| `EMBEDDING_MODEL` | Local embedding model | `BAAI/bge-m3` |
| `QDRANT_HOST` | Qdrant host | `qdrant` |
| `QDRANT_PORT` | Qdrant port | `6333` |

## 📚 API Endpoints

- `GET /` - API information
- `POST /memory/add` - Add new memory
- `POST /memory/search` - Search memories
- `GET /memory/all` - Get all memories
- `PUT /memory/update` - Update memory
- `DELETE /memory/delete` - Delete memory
- `GET /memory/history/{memory_id}` - Get memory history
- `GET /health` - Health check

## 🐛 Troubleshooting

### Qdrant Connection Error
```bash
# Make sure Qdrant is running
docker-compose ps qdrant

# Check Qdrant logs
docker-compose logs qdrant
```

### LLM API Error
```bash
# Verify API key is set
docker-compose exec mem0-app env | grep LLM

# Test LLM connection
docker-compose exec mem0-app python test_llm.py
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# For Qdrant: "6333:6333" -> "6335:6333"
# For App: "8000:8000" -> "8001:8000"
```

## 📖 Resources

- [Mem0 Documentation](https://docs.mem0.ai)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

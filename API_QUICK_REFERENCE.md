# 🚀 Mem0 API - Quick Reference Guide

## 📍 Base URLs

```
Local:  http://localhost:8000
Ngrok:  https://8f2a63040ff9.ngrok-free.app
```

---

## 🔥 Quick Start - 5 Essential Endpoints

### 1. Health Check ✅
```bash
GET /health
```
```javascript
fetch('http://localhost:8000/health')
```

---

### 2. Add Memory 💾
```bash
POST /memory/add
Content-Type: application/json

{
  "messages": "Name: John, Age: 28, Job: developer",
  "user_id": "user_123"
}
```

```javascript
fetch('http://localhost:8000/memory/add', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: "Name: John, Age: 28, Job: developer",
    user_id: "user_123"
  })
})
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {"id": "uuid-1", "memory": "Name is John", "event": "ADD"},
      {"id": "uuid-2", "memory": "Age is 28", "event": "ADD"}
    ]
  }
}
```

---

### 3. Search Memories 🔍
```bash
POST /memory/search
Content-Type: application/json

{
  "query": "programming languages",
  "user_id": "user_123",
  "limit": 5
}
```

```javascript
fetch('http://localhost:8000/memory/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "programming languages",
    user_id: "user_123",
    limit: 5
  })
})
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "uuid-1",
        "memory": "Likes Python programming",
        "score": 0.85,
        "created_at": "2026-01-15T10:00:00Z"
      }
    ]
  }
}
```

---

### 4. Get All Memories 📋
```bash
GET /memory/all?user_id=user_123
```

```javascript
fetch('http://localhost:8000/memory/all?user_id=user_123')
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "uuid-1",
        "memory": "Name is John",
        "created_at": "2026-01-15T10:00:00Z"
      }
    ]
  }
}
```

---

### 5. Update Memory ✏️
```bash
PUT /memory/update
Content-Type: application/json

{
  "memory_id": "uuid-1",
  "data": "Name: John Smith (updated)",
  "user_id": "user_123"
}
```

```javascript
fetch('http://localhost:8000/memory/update', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    memory_id: "uuid-1",
    data: "Name: John Smith (updated)",
    user_id: "user_123"
  })
})
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "message": "Memory updated successfully!"
  }
}
```

---

### 6. Delete Memory 🗑️
```bash
DELETE /memory/delete
Content-Type: application/json

{
  "memory_id": "uuid-1",
  "user_id": "user_123"
}
```

```javascript
fetch('http://localhost:8000/memory/delete', {
  method: 'DELETE',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    memory_id: "uuid-1",
    user_id: "user_123"
  })
})
```

---

## 📊 Response Format

### Success Response
```json
{
  "status": "success",
  "data": { ... }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description"
}
```

---

## 🎨 React Component Example

```jsx
import { useState, useEffect } from 'react';

function MemoryManager({ userId }) {
  const [memories, setMemories] = useState([]);
  const BASE_URL = 'http://localhost:8000';

  // Load all memories
  useEffect(() => {
    fetch(`${BASE_URL}/memory/all?user_id=${userId}`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setMemories(data.data.results);
        }
      });
  }, [userId]);

  // Add new memory
  const addMemory = async (text) => {
    const res = await fetch(`${BASE_URL}/memory/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: text,
        user_id: userId
      })
    });
    const data = await res.json();
    if (data.status === 'success') {
      // Reload memories
      window.location.reload();
    }
  };

  // Delete memory
  const deleteMemory = async (memoryId) => {
    const res = await fetch(`${BASE_URL}/memory/delete`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        memory_id: memoryId,
        user_id: userId
      })
    });
    const data = await res.json();
    if (data.status === 'success') {
      setMemories(prev => prev.filter(m => m.id !== memoryId));
    }
  };

  return (
    <div>
      <h2>Memories ({memories.length})</h2>
      {memories.map(memory => (
        <div key={memory.id}>
          <p>{memory.memory}</p>
          <button onClick={() => deleteMemory(memory.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}
```

---

## 💡 Common Patterns

### Search Before Answer
```javascript
// Always search first to get context
const searchResults = await searchMemories("user preferences", userId);
// Then use results to provide personalized response
```

### Batch Add
```javascript
// Multiple facts in one call
await addMemory(
  "Name: Alice, Age: 30, City: Tokyo, Job: Designer, Likes: UI/UX, Coffee",
  userId
);
// Creates 6 separate memories automatically
```

### Filter by Score
```javascript
const results = await searchMemories(query, userId);
const relevant = results.filter(r => r.score > 0.6); // Only highly relevant
```

---

## ⚠️ Important Notes

1. **User ID is Required** - Always include user_id to separate users
2. **No Auth Yet** - API is currently open (add auth later)
3. **Score Range** - Search scores: 0.0 (no match) to 1.0 (perfect match)
4. **Auto-Extract** - Add Memory automatically extracts multiple facts
5. **Semantic Search** - Search understands meaning, not just keywords

---

## 🐛 Error Handling

```javascript
async function safeApiCall(url, options) {
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (data.status === 'success') {
      return { success: true, data: data.data };
    } else {
      return { success: false, error: data.message };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Usage
const result = await safeApiCall('http://localhost:8000/memory/add', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ messages: "test", user_id: "123" })
});

if (result.success) {
  console.log('Success:', result.data);
} else {
  console.error('Error:', result.error);
}
```

---

## 📱 Dashboard Ideas

### Essential Views
1. **Memory List** - Show all memories with delete/edit
2. **Search** - Search bar with results
3. **Add Form** - Text area to add new memories
4. **Stats** - Total count, recent activity

### Nice-to-Have
1. **Timeline** - Memories over time
2. **Categories** - Auto-group by topic
3. **Export** - Download as JSON/CSV
4. **Import** - Bulk upload

---

## 🎯 Test Checklist

- [ ] Health check returns 200
- [ ] Can add memory
- [ ] Can search memories
- [ ] Can get all memories
- [ ] Can update memory
- [ ] Can delete memory
- [ ] Error handling works
- [ ] User isolation works (different users can't see each other's data)

---

## 📖 Full Documentation

See `API_DOCUMENTATION.md` for complete details including:
- Detailed parameter descriptions
- All error codes
- TypeScript interfaces
- Advanced examples
- Security considerations
- Performance optimization

---

## 🔗 Quick Links

- **Full API Docs:** `API_DOCUMENTATION.md`
- **OpenAPI Spec:** `openapi.json`
- **Setup Guide:** `README.md`
- **Test HTTP:** `./test-http.sh`

---

**Ready to start building? 🚀**

1. Test the API with curl or Postman
2. Create your API client wrapper
3. Build the UI components
4. Add error handling
5. Deploy! 🎉

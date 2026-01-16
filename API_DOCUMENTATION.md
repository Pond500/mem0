# 📚 Mem0 API Documentation for Frontend Development

## 🌐 Base Information

- **Base URL (Local):** `http://localhost:8000`
- **Base URL (Ngrok):** `https://8f2a63040ff9.ngrok-free.app` (or check from `./start.sh` output)
- **API Version:** v1
- **Content-Type:** `application/json`
- **Authentication:** None (currently open)

---

## 📋 API Endpoints Overview

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/health` | GET | Health check | No |
| `/memory/add` | POST | Add new memory | No |
| `/memory/search` | POST | Search memories | No |
| `/memory/all` | GET | Get all memories | No |
| `/memory/update` | PUT | Update memory | No |
| `/memory/delete` | DELETE | Delete memory | No |

---

## 1️⃣ Health Check

### `GET /health`

Check if the API server is running and healthy.

**Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

**Use Case:**
- System monitoring
- Load balancer health checks
- Initial connection test

---

## 2️⃣ Add Memory

### `POST /memory/add`

Add new memories for a user. The system will automatically extract and create multiple memory entries from the provided text.

**Request:**
```bash
curl -X POST "http://localhost:8000/memory/add" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": "Name: John, Age: 28, Job: software developer",
    "user_id": "user_123"
  }'
```

**Request Body:**
```json
{
  "messages": "string",  // The text containing information to remember
  "user_id": "string"    // Unique identifier for the user
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `messages` | string | Yes | Text containing information to be stored as memories |
| `user_id` | string | Yes | Unique user identifier (e.g., "user_123", "john@example.com") |

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "24f929be-f83b-48c0-b83c-27e2beb5e7af",
        "memory": "Name is John",
        "event": "ADD"
      },
      {
        "id": "62f37163-8f73-4cdf-9681-e1462d39dc9a",
        "memory": "Age is 28",
        "event": "ADD"
      },
      {
        "id": "cb0de2bc-e1ed-4fbf-8546-bc884fca50ab",
        "memory": "Job is software developer",
        "event": "ADD"
      }
    ]
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "success" or "error" |
| `data.results` | array | List of created memories |
| `data.results[].id` | string (UUID) | Unique memory identifier |
| `data.results[].memory` | string | The extracted memory text |
| `data.results[].event` | string | Event type: "ADD", "UPDATE", or "DELETE" |

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Missing required fields: messages or user_id"
}
```

**Use Cases:**
- User profile creation
- Saving user preferences
- Recording conversation context
- Storing user goals/plans

**Frontend Tips:**
- Show loading indicator while processing
- Display success message with count of memories created
- Handle batch operations (multiple memories from one text)
- Consider debouncing for auto-save features

---

## 3️⃣ Search Memories

### `POST /memory/search`

Search for memories using semantic search. Returns relevant memories ranked by similarity score.

**Request:**
```bash
curl -X POST "http://localhost:8000/memory/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "programming languages",
    "user_id": "user_123",
    "limit": 5
  }'
```

**Request Body:**
```json
{
  "query": "string",     // Search query
  "user_id": "string",   // User identifier
  "limit": 5             // Optional: number of results (default: 10)
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query text |
| `user_id` | string | Yes | - | User identifier |
| `limit` | integer | No | 10 | Maximum number of results (1-100) |

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "19ea42e9-6efd-408c-b6a5-23d5f474fe40",
        "memory": "Likes Python programming",
        "hash": "8475972f32e87464787e6d2ec906728b",
        "metadata": null,
        "score": 0.7173876,
        "created_at": "2026-01-15T18:01:12.584622-08:00",
        "updated_at": null,
        "user_id": "user_123"
      },
      {
        "id": "f0fbd141-63ab-4a01-8f03-558007ce01fe",
        "memory": "Likes FastAPI framework",
        "hash": "4d75689d7d64e8538514c077c46e27bb",
        "metadata": null,
        "score": 0.43504196,
        "created_at": "2026-01-15T18:01:12.594165-08:00",
        "updated_at": null,
        "user_id": "user_123"
      }
    ]
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "success" or "error" |
| `data.results` | array | List of matching memories (sorted by score) |
| `data.results[].id` | string (UUID) | Memory identifier |
| `data.results[].memory` | string | Memory content |
| `data.results[].hash` | string | Content hash for deduplication |
| `data.results[].metadata` | object/null | Additional metadata (if any) |
| `data.results[].score` | float | Similarity score (0.0 - 1.0, higher is better) |
| `data.results[].created_at` | string (ISO 8601) | Creation timestamp |
| `data.results[].updated_at` | string (ISO 8601) / null | Last update timestamp |
| `data.results[].user_id` | string | User identifier |

**Score Interpretation:**
- **0.8 - 1.0**: Highly relevant (exact or near-exact match)
- **0.6 - 0.8**: Very relevant (strong semantic match)
- **0.4 - 0.6**: Moderately relevant (related concept)
- **0.0 - 0.4**: Low relevance (weak or tangential match)

**Empty Results:**
```json
{
  "status": "success",
  "data": {
    "results": []
  }
}
```

**Use Cases:**
- Contextual search
- Auto-complete suggestions
- Finding related information
- Recommendation systems

**Frontend Tips:**
- Show relevance score as visual indicator (stars, percentage, color)
- Highlight query terms in results
- Implement infinite scroll or pagination
- Add filters (date range, score threshold)
- Show "No results found" message when empty

---

## 4️⃣ Get All Memories

### `GET /memory/all`

Retrieve all memories for a specific user.

**Request:**
```bash
curl -X GET "http://localhost:8000/memory/all?user_id=user_123"
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User identifier |

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "24f929be-f83b-48c0-b83c-27e2beb5e7af",
        "memory": "Name is John",
        "hash": "b411f2405087835e4ecef41b42f3f901",
        "metadata": null,
        "created_at": "2026-01-15T18:01:06.641930-08:00",
        "updated_at": null,
        "user_id": "user_123"
      },
      {
        "id": "62f37163-8f73-4cdf-9681-e1462d39dc9a",
        "memory": "Age is 28",
        "hash": "08e99ec064033b4c43fb6076e0c4d328",
        "metadata": null,
        "created_at": "2026-01-15T18:01:06.653421-08:00",
        "updated_at": null,
        "user_id": "user_123"
      }
    ]
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "success" or "error" |
| `data.results` | array | List of all memories for the user |
| `data.results[].id` | string (UUID) | Memory identifier |
| `data.results[].memory` | string | Memory content |
| `data.results[].hash` | string | Content hash |
| `data.results[].metadata` | object/null | Additional metadata |
| `data.results[].created_at` | string (ISO 8601) | Creation timestamp |
| `data.results[].updated_at` | string (ISO 8601) / null | Last update timestamp |
| `data.results[].user_id` | string | User identifier |

**Empty Results:**
```json
{
  "status": "success",
  "data": {
    "results": []
  }
}
```

**Use Cases:**
- User profile dashboard
- Memory management interface
- Export/backup functionality
- Overview of all stored information

**Frontend Tips:**
- Implement pagination or virtual scrolling for large datasets
- Add grouping (by date, category, type)
- Show statistics (total count, categories)
- Add bulk operations (select all, delete selected)
- Implement sorting (by date, alphabetically)

---

## 5️⃣ Update Memory

### `PUT /memory/update`

Update an existing memory by its ID.

**Request:**
```bash
curl -X PUT "http://localhost:8000/memory/update" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "24f929be-f83b-48c0-b83c-27e2beb5e7af",
    "data": "Name: John Smith (updated), Age: 29 years old",
    "user_id": "user_123"
  }'
```

**Request Body:**
```json
{
  "memory_id": "string",  // Memory UUID to update
  "data": "string",       // New content for the memory
  "user_id": "string"     // User identifier (for verification)
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memory_id` | string (UUID) | Yes | ID of the memory to update |
| `data` | string | Yes | New content for the memory |
| `user_id` | string | Yes | User identifier (must match memory owner) |

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "message": "Memory updated successfully!"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Memory not found"
}
```

**Error Response (403 Forbidden):**
```json
{
  "status": "error",
  "message": "User ID does not match memory owner"
}
```

**Use Cases:**
- Editing memory content
- Correcting mistakes
- Updating outdated information
- Refining memory entries

**Frontend Tips:**
- Show edit form with current content pre-filled
- Add "Undo" functionality
- Show "Last updated" timestamp
- Implement auto-save draft
- Add validation before submission

---

## 6️⃣ Delete Memory

### `DELETE /memory/delete`

Delete a specific memory by its ID.

**Request:**
```bash
curl -X DELETE "http://localhost:8000/memory/delete" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "24f929be-f83b-48c0-b83c-27e2beb5e7af",
    "user_id": "user_123"
  }'
```

**Request Body:**
```json
{
  "memory_id": "string",  // Memory UUID to delete
  "user_id": "string"     // User identifier (for verification)
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memory_id` | string (UUID) | Yes | ID of the memory to delete |
| `user_id` | string | Yes | User identifier (must match memory owner) |

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "message": "Memory deleted successfully!"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Memory not found"
}
```

**Error Response (403 Forbidden):**
```json
{
  "status": "error",
  "message": "User ID does not match memory owner"
}
```

**Use Cases:**
- Remove unwanted memories
- Delete outdated information
- Clear user data
- Privacy compliance (GDPR, etc.)

**Frontend Tips:**
- Show confirmation dialog before deletion
- Implement "soft delete" with undo option
- Show success/error toast notification
- Update UI immediately after deletion
- Consider bulk delete functionality

---

## 🔧 Error Handling

### Standard Error Response Format

```json
{
  "status": "error",
  "message": "Error description here"
}
```

### HTTP Status Codes

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| 200 | OK | Successful request |
| 400 | Bad Request | Missing required fields, invalid data |
| 403 | Forbidden | User ID mismatch, unauthorized access |
| 404 | Not Found | Memory not found |
| 500 | Internal Server Error | Server error, database issues |

### Common Error Scenarios

**1. Missing Required Fields (400)**
```json
{
  "status": "error",
  "message": "Missing required field: user_id"
}
```

**2. Invalid UUID Format (400)**
```json
{
  "status": "error",
  "message": "Invalid memory_id format"
}
```

**3. Memory Not Found (404)**
```json
{
  "status": "error",
  "message": "Memory with ID xxx not found"
}
```

**4. User ID Mismatch (403)**
```json
{
  "status": "error",
  "message": "You don't have permission to access this memory"
}
```

**Frontend Error Handling Best Practices:**
- Always check `status` field first
- Show user-friendly error messages
- Log errors for debugging
- Implement retry logic for network errors
- Show loading states during API calls

---

## 🎨 Frontend Implementation Examples

### JavaScript/Fetch API

```javascript
// Add Memory
async function addMemory(messages, userId) {
  try {
    const response = await fetch('http://localhost:8000/memory/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages,
        user_id: userId
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      console.log(`Created ${data.data.results.length} memories`);
      return data.data.results;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Error adding memory:', error);
    throw error;
  }
}

// Search Memories
async function searchMemories(query, userId, limit = 10) {
  try {
    const response = await fetch('http://localhost:8000/memory/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        user_id: userId,
        limit: limit
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      return data.data.results;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Error searching memories:', error);
    throw error;
  }
}

// Get All Memories
async function getAllMemories(userId) {
  try {
    const response = await fetch(
      `http://localhost:8000/memory/all?user_id=${encodeURIComponent(userId)}`
    );
    
    const data = await response.json();
    
    if (data.status === 'success') {
      return data.data.results;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Error getting memories:', error);
    throw error;
  }
}

// Update Memory
async function updateMemory(memoryId, newData, userId) {
  try {
    const response = await fetch('http://localhost:8000/memory/update', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        memory_id: memoryId,
        data: newData,
        user_id: userId
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      return true;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Error updating memory:', error);
    throw error;
  }
}

// Delete Memory
async function deleteMemory(memoryId, userId) {
  try {
    const response = await fetch('http://localhost:8000/memory/delete', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        memory_id: memoryId,
        user_id: userId
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      return true;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Error deleting memory:', error);
    throw error;
  }
}
```

### React Example with Hooks

```jsx
import { useState, useEffect } from 'react';

function MemoryDashboard({ userId }) {
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load all memories on mount
  useEffect(() => {
    loadMemories();
  }, [userId]);

  async function loadMemories() {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `http://localhost:8000/memory/all?user_id=${userId}`
      );
      const data = await response.json();
      
      if (data.status === 'success') {
        setMemories(data.data.results);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Failed to load memories');
    } finally {
      setLoading(false);
    }
  }

  async function handleAddMemory(text) {
    try {
      const response = await fetch('http://localhost:8000/memory/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: text,
          user_id: userId
        })
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        // Reload memories
        await loadMemories();
        return true;
      }
    } catch (err) {
      setError('Failed to add memory');
    }
    return false;
  }

  async function handleDeleteMemory(memoryId) {
    if (!confirm('Are you sure you want to delete this memory?')) {
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/memory/delete', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          memory_id: memoryId,
          user_id: userId
        })
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        // Remove from state
        setMemories(prev => prev.filter(m => m.id !== memoryId));
      }
    } catch (err) {
      setError('Failed to delete memory');
    }
  }

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="memory-dashboard">
      <h1>My Memories ({memories.length})</h1>
      
      {memories.map(memory => (
        <div key={memory.id} className="memory-card">
          <p>{memory.memory}</p>
          <small>
            Created: {new Date(memory.created_at).toLocaleDateString()}
          </small>
          <button onClick={() => handleDeleteMemory(memory.id)}>
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}
```

---

## 📊 Dashboard Features to Implement

### Suggested Dashboard Components

1. **Memory List View**
   - Display all memories in a list/grid
   - Sort by date, relevance, category
   - Filter by date range, tags
   - Search functionality

2. **Memory Detail View**
   - Full memory content
   - Metadata (created, updated, score)
   - Edit/Delete actions
   - Related memories

3. **Search Interface**
   - Search bar with autocomplete
   - Filters (date, relevance score)
   - Results with relevance indicators
   - Click to view details

4. **Add Memory Form**
   - Text input area
   - Real-time validation
   - Success/error feedback
   - Batch import option

5. **Statistics Dashboard**
   - Total memories count
   - Memories added over time (chart)
   - Top categories/topics
   - Search analytics

6. **User Management**
   - User profile
   - Memory quota/limits
   - Export data (JSON, CSV)
   - Delete all data

### Visualization Ideas

1. **Memory Timeline**
   - Show memories on a timeline
   - Group by day/week/month
   - Interactive zoom

2. **Memory Graph/Network**
   - Show relationships between memories
   - Cluster by similarity
   - Interactive exploration

3. **Word Cloud**
   - Most common terms in memories
   - Clickable to search

4. **Heatmap**
   - Activity over time
   - Busiest days/hours

---

## 🔐 Security Considerations

### Current State
- ⚠️ No authentication implemented
- ⚠️ Open API access
- ⚠️ User ID is client-provided

### Recommended Implementations

1. **Authentication**
   - Add JWT or API key authentication
   - Implement OAuth 2.0
   - Session management

2. **Authorization**
   - Verify user ownership
   - Role-based access control
   - Rate limiting

3. **Data Validation**
   - Sanitize user input
   - Validate UUID formats
   - Check content length limits

4. **CORS**
   - Configure allowed origins
   - Restrict methods
   - Set appropriate headers

### Frontend Security Best Practices

```javascript
// Store user token securely
const token = localStorage.getItem('auth_token');

// Add to all API requests
fetch('http://localhost:8000/memory/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`  // Add when auth is implemented
  },
  body: JSON.stringify({...})
});

// Validate user input
function sanitizeInput(text) {
  return text.trim().slice(0, 10000); // Limit length
}

// Handle sensitive data
// - Don't log user data to console in production
// - Use HTTPS in production
// - Implement CSRF protection
```

---

## 🚀 Performance Optimization Tips

### API Call Optimization

1. **Debouncing Search**
```javascript
import { debounce } from 'lodash';

const debouncedSearch = debounce(async (query) => {
  const results = await searchMemories(query, userId);
  setSearchResults(results);
}, 300);
```

2. **Caching**
```javascript
const cache = new Map();

async function getCachedMemories(userId) {
  if (cache.has(userId)) {
    return cache.get(userId);
  }
  
  const memories = await getAllMemories(userId);
  cache.set(userId, memories);
  
  // Clear cache after 5 minutes
  setTimeout(() => cache.delete(userId), 5 * 60 * 1000);
  
  return memories;
}
```

3. **Pagination**
```javascript
async function getMemoriesPage(userId, page = 1, limit = 20) {
  // Note: Backend doesn't support pagination yet
  // This is a client-side implementation
  const allMemories = await getAllMemories(userId);
  const start = (page - 1) * limit;
  const end = start + limit;
  return allMemories.slice(start, end);
}
```

4. **Batch Operations**
```javascript
async function addMultipleMemories(textArray, userId) {
  // Combine into one API call
  const combined = textArray.join('. ');
  return await addMemory(combined, userId);
}
```

---

## 📱 Mobile Considerations

### Responsive Design
- Use mobile-first approach
- Touch-friendly UI elements (min 44px tap targets)
- Swipe gestures for delete/edit
- Pull-to-refresh

### Offline Support
- Cache memories locally (IndexedDB)
- Queue API calls when offline
- Sync when connection restored

### Performance
- Lazy load images/components
- Virtual scrolling for long lists
- Minimize bundle size
- Use service workers

---

## 🧪 Testing Endpoints

### Quick Test Script
```bash
# Set variables
export BASE_URL="http://localhost:8000"
export USER_ID="test_user_123"

# 1. Health check
curl -X GET "$BASE_URL/health"

# 2. Add memory
curl -X POST "$BASE_URL/memory/add" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": "Name: Alice, Age: 30, Job: Designer",
    "user_id": "'$USER_ID'"
  }'

# 3. Search
curl -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Alice",
    "user_id": "'$USER_ID'",
    "limit": 5
  }'

# 4. Get all
curl -X GET "$BASE_URL/memory/all?user_id=$USER_ID"
```

### Test with Postman/Insomnia

Import this collection:
```json
{
  "info": {
    "name": "Mem0 API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    },
    {
      "key": "user_id",
      "value": "test_user_123"
    }
  ]
}
```

---

## 📦 TypeScript Interfaces

```typescript
// Types for frontend development

interface Memory {
  id: string;
  memory: string;
  hash: string;
  metadata: any | null;
  score?: number;
  created_at: string;
  updated_at: string | null;
  user_id: string;
}

interface AddMemoryRequest {
  messages: string;
  user_id: string;
}

interface AddMemoryResponse {
  status: 'success' | 'error';
  data?: {
    results: Array<{
      id: string;
      memory: string;
      event: 'ADD' | 'UPDATE' | 'DELETE';
    }>;
  };
  message?: string;
}

interface SearchMemoriesRequest {
  query: string;
  user_id: string;
  limit?: number;
}

interface SearchMemoriesResponse {
  status: 'success' | 'error';
  data?: {
    results: Memory[];
  };
  message?: string;
}

interface GetAllMemoriesResponse {
  status: 'success' | 'error';
  data?: {
    results: Memory[];
  };
  message?: string;
}

interface UpdateMemoryRequest {
  memory_id: string;
  data: string;
  user_id: string;
}

interface DeleteMemoryRequest {
  memory_id: string;
  user_id: string;
}

interface StandardResponse {
  status: 'success' | 'error';
  data?: {
    message: string;
  };
  message?: string;
}

// API Client Class
class Mem0Client {
  constructor(private baseUrl: string) {}

  async addMemory(request: AddMemoryRequest): Promise<AddMemoryResponse> {
    const response = await fetch(`${this.baseUrl}/memory/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    return response.json();
  }

  async searchMemories(request: SearchMemoriesRequest): Promise<SearchMemoriesResponse> {
    const response = await fetch(`${this.baseUrl}/memory/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    return response.json();
  }

  async getAllMemories(userId: string): Promise<GetAllMemoriesResponse> {
    const response = await fetch(
      `${this.baseUrl}/memory/all?user_id=${encodeURIComponent(userId)}`
    );
    return response.json();
  }

  async updateMemory(request: UpdateMemoryRequest): Promise<StandardResponse> {
    const response = await fetch(`${this.baseUrl}/memory/update`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    return response.json();
  }

  async deleteMemory(request: DeleteMemoryRequest): Promise<StandardResponse> {
    const response = await fetch(`${this.baseUrl}/memory/delete`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    return response.json();
  }
}

// Usage
const client = new Mem0Client('http://localhost:8000');
const result = await client.addMemory({
  messages: 'Name: Bob',
  user_id: 'user_123'
});
```

---

## 🎯 Next Steps for Frontend Team

### Phase 1: Basic UI (Week 1-2)
- [ ] Set up project (React/Vue/etc.)
- [ ] Implement API client
- [ ] Create memory list view
- [ ] Add search functionality
- [ ] Basic CRUD operations

### Phase 2: Enhanced Features (Week 3-4)
- [ ] Memory detail pages
- [ ] Edit functionality
- [ ] Filters and sorting
- [ ] Statistics dashboard
- [ ] Export functionality

### Phase 3: Polish (Week 5-6)
- [ ] Responsive design
- [ ] Loading states and animations
- [ ] Error handling
- [ ] Accessibility (WCAG 2.1)
- [ ] Testing (unit, integration)

### Phase 4: Advanced Features (Future)
- [ ] Real-time updates (WebSockets)
- [ ] Collaboration features
- [ ] Memory visualization
- [ ] AI-powered insights
- [ ] Mobile app

---

## 📞 Support & Resources

- **API Base URL:** `http://localhost:8000`
- **API Documentation:** This file
- **OpenAPI Spec:** `openapi.json`
- **Test Scenarios:** `DIFY_TEST_SCENARIOS.md`
- **Setup Guide:** `README.md`

---

## ✅ Checklist for Frontend Developers

- [ ] Read this documentation thoroughly
- [ ] Test all endpoints with curl/Postman
- [ ] Review OpenAPI specification
- [ ] Understand error handling patterns
- [ ] Set up local development environment
- [ ] Create API client wrapper
- [ ] Implement TypeScript interfaces
- [ ] Plan component architecture
- [ ] Design UI/UX mockups
- [ ] Start development!

---

**Last Updated:** January 16, 2026  
**Version:** 1.0  
**Contact:** Backend Team

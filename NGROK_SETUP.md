# 🌐 Mem0 API - Public Access via ngrok

## 📡 Public URL
```
https://8f2a63040ff9.ngrok-free.app
```

## 🔗 API Endpoints

### Base URL
```
https://8f2a63040ff9.ngrok-free.app
```

### Available Endpoints

#### 1. Health Check
```bash
GET /health
```

#### 2. Add Memory
```bash
POST /memory/add
Content-Type: application/json

{
  "messages": "User prefers Python and FastAPI",
  "user_id": "user123"
}
```

#### 3. Search Memories
```bash
POST /memory/search
Content-Type: application/json

{
  "query": "programming preferences",
  "user_id": "user123",
  "limit": 5
}
```

#### 4. Get All Memories
```bash
GET /memory/all?user_id=user123
```

#### 5. Update Memory
```bash
PUT /memory/update
Content-Type: application/json

{
  "memory_id": "abc123",
  "data": "Updated memory content"
}
```

#### 6. Delete Memory
```bash
DELETE /memory/delete
Content-Type: application/json

{
  "memory_id": "abc123"
}
```

## 📋 Import to Dify

### Method 1: Use OpenAPI Spec
1. Go to Dify → Tools → Create Custom Tool
2. Select "Import from OpenAPI"
3. Upload `openapi.json` file
4. Done! ✅

### Method 2: Manual Configuration
1. Go to Dify → Tools → Create Custom Tool
2. Set Base URL: `https://8f2a63040ff9.ngrok-free.app`
3. Add each endpoint manually following the specs above

## 🧪 Test Commands

```bash
# Test health
curl https://8f2a63040ff9.ngrok-free.app/health

# Test add memory
curl -X POST https://8f2a63040ff9.ngrok-free.app/memory/add \
  -H "Content-Type: application/json" \
  -d '{
    "messages": "ผมชอบเขียนโปรแกรม Python",
    "user_id": "test_user"
  }'

# Test search
curl -X POST https://8f2a63040ff9.ngrok-free.app/memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "programming",
    "user_id": "test_user"
  }'

# Test get all
curl "https://8f2a63040ff9.ngrok-free.app/memory/all?user_id=test_user"
```

## 📊 ngrok Dashboard

View traffic and requests:
```
http://localhost:4040
```

## ⚠️ Important Notes

1. **Free ngrok limitations:**
   - URL changes every restart
   - 40 requests/minute limit
   - Shows ngrok warning page on first visit

2. **For production:**
   - Use paid ngrok plan for static domain
   - Or deploy to cloud (Railway, Fly.io, etc.)
   - Or use VPS with public IP

3. **Security:**
   - Current setup has no authentication
   - Consider adding API key if needed

## 🔄 Keep ngrok Running

Current session is running in background (PID: 12539)

To check status:
```bash
curl http://localhost:4040/api/tunnels
```

To stop:
```bash
pkill ngrok
```

To restart:
```bash
ngrok http 8000 --log=stdout > /tmp/ngrok.log 2>&1 &
```

## 🎯 Next Steps for Dify Integration

1. ✅ ngrok is running
2. ✅ Public URL available
3. ✅ OpenAPI spec created
4. 📝 Import `openapi.json` to Dify
5. 🧪 Test in Dify workflow
6. 🚀 Use in your AI agents!

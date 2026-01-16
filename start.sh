#!/bin/bash

# Mem0 Local - Start Script
# This script starts Docker services and ngrok tunnel

set -e

echo "🚀 Starting Mem0 Local Memory System..."
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Please install it first:"
    echo "   brew install ngrok"
    exit 1
fi

# Start Docker services
echo ""
echo "📦 Starting Docker services..."
cd "$(dirname "$0")"
docker-compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# Check if services are running
if docker-compose ps | grep -q "mem0-app.*Up"; then
    echo "✅ Mem0 App is running"
else
    echo "❌ Mem0 App failed to start"
    docker-compose logs mem0-app
    exit 1
fi

if docker-compose ps | grep -q "mem0-qdrant.*Up"; then
    echo "✅ Qdrant is running"
else
    echo "❌ Qdrant failed to start"
    docker-compose logs qdrant
    exit 1
fi

# Start ngrok in background
echo ""
echo "🌐 Starting ngrok tunnel..."

# Kill any existing ngrok processes
pkill -f "ngrok http" || true
sleep 2

# Start ngrok
nohup ngrok http 8000 --log=stdout > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!
echo "   ngrok PID: $NGROK_PID"

# Wait for ngrok to start
echo "   Waiting for ngrok..."
sleep 3

# Get ngrok URL
NGROK_URL=""
for i in {1..10}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4 | head -1)
    if [ -n "$NGROK_URL" ]; then
        break
    fi
    sleep 1
done

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get ngrok URL"
    echo "   Check logs: tail -f /tmp/ngrok.log"
    exit 1
fi

echo "✅ ngrok tunnel created"
echo ""
echo "========================================"
echo "🎉 All services are running!"
echo "========================================"
echo ""
echo "📊 Service URLs:"
echo "   • Mem0 API (local):   http://localhost:8000"
echo "   • Mem0 API (public):  $NGROK_URL"
echo "   • Qdrant Dashboard:   http://localhost:6333/dashboard"
echo "   • ngrok Dashboard:    http://localhost:4040"
echo ""
echo "📝 API Documentation:"
echo "   • Swagger UI:         http://localhost:8000/docs"
echo "   • OpenAPI Spec:       $NGROK_URL (for Dify)"
echo ""
echo "💡 Quick Test:"
echo "   curl $NGROK_URL/health"
echo ""
echo "📋 Management Commands:"
echo "   • View logs:          ./logs.sh"
echo "   • Stop services:      ./stop.sh"
echo "   • Restart:            ./stop.sh && ./start.sh"
echo ""
echo "🔗 For Dify Integration:"
echo "   Use this URL in your OpenAPI import: $NGROK_URL"
echo "   Update openapi.json server URL to: $NGROK_URL"
echo ""

# Save ngrok URL to file for other scripts
echo "$NGROK_URL" > /tmp/ngrok_url.txt

# Optional: Test the connection
echo "🧪 Testing connection..."
if curl -s "$NGROK_URL/health" > /dev/null 2>&1; then
    echo "✅ API is accessible!"
else
    echo "⚠️  API test failed (might need more time to start)"
fi

echo ""
echo "✨ Ready to use! Press Ctrl+C to stop monitoring, or use ./stop.sh to stop all services"

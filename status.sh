#!/bin/bash

# Mem0 Local - Status Check Script
# This script checks the status of all services

echo "📊 Mem0 Local - Service Status"
echo "========================================"

cd "$(dirname "$0")"

# Check Docker services
echo ""
echo "🐳 Docker Services:"
docker-compose ps

# Check if ngrok is running
echo ""
echo "🌐 ngrok Status:"
if pgrep -f "ngrok http" > /dev/null; then
    echo "✅ ngrok is running"
    
    # Get ngrok URL
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4 | head -1)
    
    if [ -n "$NGROK_URL" ]; then
        echo "   Public URL: $NGROK_URL"
        echo "   Dashboard:  http://localhost:4040"
    else
        echo "   ⚠️  Could not retrieve ngrok URL"
    fi
else
    echo "❌ ngrok is not running"
fi

# Check API health
echo ""
echo "🏥 API Health:"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    HEALTH=$(curl -s http://localhost:8000/health)
    echo "✅ API is healthy"
    echo "   Response: $HEALTH"
else
    echo "❌ API is not responding"
fi

# Check Qdrant
echo ""
echo "💾 Qdrant Status:"
if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    COLLECTIONS=$(curl -s http://localhost:6333/collections | grep -o '"name":"[^"]*' | cut -d'"' -f4)
    echo "✅ Qdrant is running"
    echo "   Dashboard: http://localhost:6333/dashboard"
    if [ -n "$COLLECTIONS" ]; then
        echo "   Collections:"
        echo "$COLLECTIONS" | while read col; do
            echo "     - $col"
        done
    else
        echo "   No collections found"
    fi
else
    echo "❌ Qdrant is not responding"
fi

# Check disk usage
echo ""
echo "💽 Disk Usage:"
docker system df | grep -E "Images|Containers|Local Volumes"

echo ""
echo "========================================"
echo ""

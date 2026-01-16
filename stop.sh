#!/bin/bash

# Mem0 Local - Stop Script
# This script stops Docker services and ngrok tunnel

echo "🛑 Stopping Mem0 Local Memory System..."
echo "========================================"

cd "$(dirname "$0")"

# Stop ngrok
echo ""
echo "🌐 Stopping ngrok tunnel..."
if pkill -f "ngrok http"; then
    echo "✅ ngrok stopped"
else
    echo "ℹ️  ngrok was not running"
fi

# Stop Docker services
echo ""
echo "📦 Stopping Docker services..."
docker-compose down

# Check if stopped successfully
if ! docker-compose ps | grep -q "Up"; then
    echo "✅ All Docker services stopped"
else
    echo "⚠️  Some services may still be running"
    docker-compose ps
fi

# Clean up temp files
rm -f /tmp/ngrok.log
rm -f /tmp/ngrok_url.txt

echo ""
echo "========================================"
echo "✅ All services stopped successfully!"
echo "========================================"
echo ""
echo "💡 To start again, run: ./start.sh"
echo ""

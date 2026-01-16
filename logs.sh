#!/bin/bash

# Mem0 Local - Logs Viewer Script
# This script shows logs from services

cd "$(dirname "$0")"

echo "📋 Mem0 Local - Logs Viewer"
echo "========================================"
echo ""
echo "Choose what to view:"
echo "  1) All services"
echo "  2) Mem0 App only"
echo "  3) Qdrant only"
echo "  4) ngrok only"
echo "  5) Follow all logs (live)"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "=== Mem0 App Logs ==="
        docker-compose logs --tail=50 mem0-app
        echo ""
        echo "=== Qdrant Logs ==="
        docker-compose logs --tail=50 qdrant
        echo ""
        echo "=== ngrok Logs ==="
        if [ -f /tmp/ngrok.log ]; then
            tail -50 /tmp/ngrok.log
        else
            echo "No ngrok logs found"
        fi
        ;;
    2)
        docker-compose logs --tail=100 -f mem0-app
        ;;
    3)
        docker-compose logs --tail=100 -f qdrant
        ;;
    4)
        if [ -f /tmp/ngrok.log ]; then
            tail -100 -f /tmp/ngrok.log
        else
            echo "No ngrok logs found at /tmp/ngrok.log"
        fi
        ;;
    5)
        docker-compose logs -f &
        DOCKER_PID=$!
        
        if [ -f /tmp/ngrok.log ]; then
            tail -f /tmp/ngrok.log &
            NGROK_PID=$!
        fi
        
        echo "Showing live logs... Press Ctrl+C to stop"
        wait
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

#!/bin/bash

# Mem0 Local - Restart Script
# This script restarts all services

echo "🔄 Restarting Mem0 Local Memory System..."
echo ""

cd "$(dirname "$0")"

# Stop services
./stop.sh

echo ""
echo "⏳ Waiting 3 seconds..."
sleep 3

# Start services
./start.sh

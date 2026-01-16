#!/bin/bash

# Mem0 Local - Test Script
# This script runs basic tests to ensure everything works

echo "🧪 Mem0 Local - Test Suite"
echo "========================================"

cd "$(dirname "$0")"

# Get ngrok URL
NGROK_URL=$(cat /tmp/ngrok_url.txt 2>/dev/null)
if [ -z "$NGROK_URL" ]; then
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4 | head -1)
fi

if [ -z "$NGROK_URL" ]; then
    echo "⚠️  ngrok URL not found. Using localhost..."
    BASE_URL="http://localhost:8000"
else
    echo "🌐 Using ngrok URL: $NGROK_URL"
    BASE_URL="$NGROK_URL"
fi

TEST_USER="test_$(date +%s)"
SUCCESS=0
FAILED=0

echo ""
echo "Running tests..."
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
if curl -s "$BASE_URL/health" | grep -q "healthy"; then
    echo "✅ PASS"
    ((SUCCESS++))
else
    echo "❌ FAIL"
    ((FAILED++))
fi

# Test 2: Add Memory
echo ""
echo "Test 2: Add Memory"
RESPONSE=$(curl -s -X POST "$BASE_URL/memory/add" \
    -H "Content-Type: application/json" \
    -d "{\"messages\":\"Test user likes Python programming\",\"user_id\":\"$TEST_USER\"}")

if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ PASS"
    ((SUCCESS++))
else
    echo "❌ FAIL"
    echo "Response: $RESPONSE"
    ((FAILED++))
fi

# Test 3: Search Memory
echo ""
echo "Test 3: Search Memory"
sleep 2  # Wait for indexing
RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"Python\",\"user_id\":\"$TEST_USER\"}")

if echo "$RESPONSE" | grep -q "Python"; then
    echo "✅ PASS"
    ((SUCCESS++))
else
    echo "❌ FAIL"
    echo "Response: $RESPONSE"
    ((FAILED++))
fi

# Test 4: Get All Memories
echo ""
echo "Test 4: Get All Memories"
RESPONSE=$(curl -s "$BASE_URL/memory/all?user_id=$TEST_USER")

if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ PASS"
    ((SUCCESS++))
else
    echo "❌ FAIL"
    echo "Response: $RESPONSE"
    ((FAILED++))
fi

# Test 5: Qdrant Connection
echo ""
echo "Test 5: Qdrant Collections"
RESPONSE=$(curl -s "http://localhost:6333/collections")

if echo "$RESPONSE" | grep -q "collections"; then
    echo "✅ PASS"
    ((SUCCESS++))
else
    echo "❌ FAIL"
    ((FAILED++))
fi

# Summary
echo ""
echo "========================================"
echo "📊 Test Results"
echo "========================================"
echo "✅ Passed: $SUCCESS"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All tests passed!"
    exit 0
else
    echo "⚠️  Some tests failed. Check logs with: ./logs.sh"
    exit 1
fi

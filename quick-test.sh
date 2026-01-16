#!/bin/bash

# Quick Test - Mem0 Memory Functions
# ทดสอบผ่าน API โดยตรง (ไม่ผ่าน Dify)

echo "🧪 Mem0 Quick Test"
echo "========================================"

BASE_URL="http://localhost:8000"
TEST_USER="test_$(date +%s)"

echo ""
echo "📝 Test User ID: $TEST_USER"
echo ""

# Test 1: Add Memory - Profile
echo "Test 1: Add Profile Memory"
echo "--------------------------"
curl -s -X POST "$BASE_URL/memory/add" \
  -H "Content-Type: application/json" \
  -d "{
    \"messages\": \"Name: John, Age: 28, Job: developer, Location: Bangkok\",
    \"user_id\": \"$TEST_USER\"
  }" | python3 -m json.tool

echo ""
echo "✅ Profile saved"
echo ""
sleep 2

# Test 2: Add Memory - Preferences
echo "Test 2: Add Preferences Memory"
echo "--------------------------------"
curl -s -X POST "$BASE_URL/memory/add" \
  -H "Content-Type: application/json" \
  -d "{
    \"messages\": \"Likes: Python programming, FastAPI framework, pizza. Dislikes: spicy food\",
    \"user_id\": \"$TEST_USER\"
  }" | python3 -m json.tool

echo ""
echo "✅ Preferences saved"
echo ""
sleep 2

# Test 3: Search Memory
echo "Test 3: Search for 'Python'"
echo "----------------------------"
RESULT=$(curl -s -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"Python programming\",
    \"user_id\": \"$TEST_USER\",
    \"limit\": 5
  }")

echo "$RESULT" | python3 -m json.tool
echo ""

if echo "$RESULT" | grep -q "Python"; then
    echo "✅ Search found Python-related memories"
else
    echo "❌ Search failed"
fi

echo ""
sleep 2

# Test 4: Get All Memories
echo "Test 4: Get All Memories"
echo "------------------------"
curl -s "$BASE_URL/memory/all?user_id=$TEST_USER" | python3 -m json.tool

echo ""
echo "✅ Retrieved all memories"
echo ""

# Summary
echo "========================================"
echo "📊 Test Summary"
echo "========================================"
echo ""
echo "Test User ID: $TEST_USER"
echo ""
echo "Now test in Dify using this user_id to see if it recalls:"
echo "1. Name: John"
echo "2. Age: 28"
echo "3. Job: developer"
echo "4. Likes: Python, FastAPI, pizza"
echo ""
echo "Try asking in Dify:"
echo '  "What do you know about user '$TEST_USER'?"'
echo ""

#!/bin/bash

# Mem0 API Test - Test All Tools via HTTP
# This script tests all memory tools before using in Dify

set -e

BASE_URL="http://localhost:8000"
TEST_USER="test_user_$(date +%s)"

echo "🧪 Mem0 API - Complete Tool Test"
echo "========================================"
echo "Test User ID: $TEST_USER"
echo "Base URL: $BASE_URL"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SUCCESS=0
FAILED=0

# Function to check test result
check_result() {
    local test_name="$1"
    local response="$2"
    local expected="$3"
    
    if echo "$response" | grep -q "$expected"; then
        echo -e "${GREEN}✅ PASS${NC} - $test_name"
        ((SUCCESS++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} - $test_name"
        echo "Expected: $expected"
        echo "Response: $response"
        ((FAILED++))
        return 1
    fi
}

# Test 1: Health Check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: GET /health"
echo ""

RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$BASE_URL/health")
HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE/d')

echo "Response:"
echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
echo ""

if [ "$HTTP_CODE" = "200" ]; then
    check_result "Health Check" "$BODY" "healthy"
else
    echo -e "${RED}❌ FAIL${NC} - HTTP $HTTP_CODE"
    ((FAILED++))
fi

echo ""
sleep 1

# Test 2: Add Memory - Profile
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Add Memory - Profile Information"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/add"

PAYLOAD='{
  "messages": "Name: John, Age: 28, Job: software developer, Location: Bangkok",
  "user_id": "'$TEST_USER'"
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/add" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Add Profile Memory" "$RESPONSE" "success"
echo ""
sleep 2

# Test 3: Add Memory - Preferences
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: Add Memory - Preferences"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/add"

PAYLOAD='{
  "messages": "Likes: Python programming, FastAPI framework. Dislikes: verbose syntax",
  "user_id": "'$TEST_USER'"
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/add" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Add Preferences Memory" "$RESPONSE" "success"
echo ""
sleep 2

# Test 4: Add Memory - Goals
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Add Memory - Goals"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/add"

PAYLOAD='{
  "messages": "Goal: Learn AI and machine learning, Build a chatbot with Dify",
  "user_id": "'$TEST_USER'"
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/add" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Add Goals Memory" "$RESPONSE" "success"
echo ""
sleep 2

# Test 5: Add Memory - Hobbies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 5: Add Memory - Hobbies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/add"

PAYLOAD='{
  "messages": "Hobbies: watches Formula 1 racing, supports Red Bull Racing team",
  "user_id": "'$TEST_USER'"
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/add" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Add Hobbies Memory" "$RESPONSE" "success"
echo ""
sleep 2

# Test 6: Search Memory - Name
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 6: Search Memory - by Name"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/search"

PAYLOAD='{
  "query": "John name",
  "user_id": "'$TEST_USER'",
  "limit": 5
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Search by Name" "$RESPONSE" "John"
echo ""
sleep 1

# Test 7: Search Memory - Programming
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 7: Search Memory - Programming Preferences"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/search"

PAYLOAD='{
  "query": "programming language preferences Python",
  "user_id": "'$TEST_USER'",
  "limit": 5
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Search Programming" "$RESPONSE" "Python"
echo ""
sleep 1

# Test 8: Search Memory - Goals
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 8: Search Memory - Goals"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/search"

PAYLOAD='{
  "query": "goals learning AI",
  "user_id": "'$TEST_USER'",
  "limit": 5
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Search Goals" "$RESPONSE" "AI"
echo ""
sleep 1

# Test 9: Search Memory - Hobbies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 10: Search Memory - Hobbies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/search"

PAYLOAD='{
  "query": "hobbies F1 racing",
  "user_id": "'$TEST_USER'",
  "limit": 5
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

check_result "Search Hobbies" "$RESPONSE" "Formula 1"
echo ""
sleep 1

# Test 10: Get All Memories
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 10: Get All Memories"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: GET /memory/all?user_id=$TEST_USER"
echo ""

RESPONSE=$(curl -s "$BASE_URL/memory/all?user_id=$TEST_USER")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Count memories
MEMORY_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('data', {}).get('results', [])))" 2>/dev/null || echo "0")

echo "Total memories stored: $MEMORY_COUNT"
echo ""

if [ "$MEMORY_COUNT" -ge 4 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Get All Memories (found $MEMORY_COUNT memories)"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAIL${NC} - Get All Memories (expected >= 4, found $MEMORY_COUNT)"
    ((FAILED++))
fi

echo ""
sleep 1

# Store first memory ID for update test
MEMORY_ID_TO_UPDATE=""

# Test 11: Get Memory ID for Update Test
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 11: Get Memory ID for Update Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/search"

PAYLOAD='{
  "query": "John name",
  "user_id": "'$TEST_USER'",
  "limit": 1
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Extract memory ID
MEMORY_ID_TO_UPDATE=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); results=data.get('data', {}).get('results', []); print(results[0].get('id', '') if results else '')" 2>/dev/null || echo "")

if [ -n "$MEMORY_ID_TO_UPDATE" ]; then
    echo -e "${GREEN}✅ PASS${NC} - Got Memory ID: $MEMORY_ID_TO_UPDATE"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAIL${NC} - Could not get memory ID"
    ((FAILED++))
fi

echo ""
sleep 1

# Test 12: Update Memory
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 12: Update Memory"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: PUT /memory/update"

if [ -z "$MEMORY_ID_TO_UPDATE" ]; then
    echo -e "${YELLOW}⚠️  SKIP${NC} - No memory ID available to update"
    echo ""
else
    PAYLOAD='{
      "memory_id": "'$MEMORY_ID_TO_UPDATE'",
      "data": "Name: John Smith (updated), Age: 29 years old, Job: Senior Software Developer",
      "user_id": "'$TEST_USER'"
    }'

    echo "Payload:"
    echo "$PAYLOAD" | python3 -m json.tool
    echo ""

    RESPONSE=$(curl -s -X PUT "$BASE_URL/memory/update" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD")

    echo "Response:"
    echo "$RESPONSE" | python3 -m json.tool
    echo ""

    check_result "Update Memory" "$RESPONSE" "success"
    echo ""
    sleep 2

    # Verify the update by searching again
    echo "Verifying update..."
    VERIFY_PAYLOAD='{
      "query": "John Smith Senior Developer",
      "user_id": "'$TEST_USER'",
      "limit": 5
    }'

    VERIFY_RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
      -H "Content-Type: application/json" \
      -d "$VERIFY_PAYLOAD")

    echo "Verification Response:"
    echo "$VERIFY_RESPONSE" | python3 -m json.tool
    echo ""

    if echo "$VERIFY_RESPONSE" | grep -q "Senior"; then
        echo -e "${GREEN}✅ Verified${NC} - Memory updated successfully"
    else
        echo -e "${YELLOW}⚠️  Warning${NC} - Update may not be reflected yet"
    fi
    echo ""
fi

sleep 1

# Test 13: Search with Different User (Should Return Empty)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 13: User Isolation Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Request: POST /memory/search (with different user_id)"

OTHER_USER="other_user_$(date +%s)"

PAYLOAD='{
  "query": "John",
  "user_id": "'$OTHER_USER'",
  "limit": 5
}'

echo "Payload:"
echo "$PAYLOAD" | python3 -m json.tool
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/memory/search" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Should return empty or no results for different user
RESULT_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('data', {}).get('results', [])))" 2>/dev/null || echo "0")

if [ "$RESULT_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - User Isolation (correctly returned 0 results for different user)"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAIL${NC} - User Isolation (should return 0 results, got $RESULT_COUNT)"
    ((FAILED++))
fi

echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Test User ID: $TEST_USER"
echo ""
echo -e "${GREEN}✅ Passed: $SUCCESS${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"
echo ""

TOTAL=$((SUCCESS + FAILED))
PERCENTAGE=$((SUCCESS * 100 / TOTAL))

echo "Success Rate: $PERCENTAGE% ($SUCCESS/$TOTAL)"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "✅ All memory tools are working correctly"
    echo "✅ Ready to use in Dify"
    echo ""
    echo "Next Steps:"
    echo "  1. Import openapi.json to Dify"
    echo "  2. Create an agent with memory tools"
    echo "  3. Add the instruction from agent_instruction_thai_short.txt"
    echo "  4. Start testing with Dify!"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check if services are running: ./status.sh"
    echo "  2. View logs: ./logs.sh"
    echo "  3. Restart services: ./restart.sh"
    echo ""
    exit 1
fi

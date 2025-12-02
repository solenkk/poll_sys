#!/bin/bash

echo "=== FINAL POLL SYSTEM TEST ===\n"

echo "1. Creating a new test poll..."
curl -X POST http://127.0.0.1:8000/api/polls/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Final Test Poll",
    "expires_at": "2024-12-31T23:59:59Z",
    "options": [
      {"option_text": "Choice A"},
      {"option_text": "Choice B"},
      {"option_text": "Choice C"}
    ]
  }'

echo "\n\n2. Listing all polls to get the new poll ID..."
curl http://127.0.0.1:8000/api/polls/ | python -m json.tool

echo "\n\n3. TEST 1: First vote (should succeed)..."
curl -X POST http://127.0.0.1:8000/api/polls/4/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 10, "voter_identifier": "final_user_1"}'

echo "\n\n4. TEST 2: Same user tries different option in same poll (should FAIL)..."
curl -X POST http://127.0.0.1:8000/api/polls/4/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 11, "voter_identifier": "final_user_1"}'

echo "\n\n5. TEST 3: Different user votes (should succeed)..."
curl -X POST http://127.0.0.1:8000/api/polls/4/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 10, "voter_identifier": "final_user_2"}'

echo "\n\n6. TEST 4: Third user votes for different option (should succeed)..."
curl -X POST http://127.0.0.1:8000/api/polls/4/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 12, "voter_identifier": "final_user_3"}'

echo "\n\n7. Checking final results..."
curl http://127.0.0.1:8000/api/polls/4/results/

echo "\n\n8. Verifying other polls still work..."
curl http://127.0.0.1:8000/api/polls/2/results/

echo "\n\n=== TEST COMPLETE ==="

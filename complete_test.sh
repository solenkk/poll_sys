#!/bin/bash

echo "=== COMPLETE POLL SYSTEM TEST ===\n"

echo "=== PART 1: Testing Poll #2 (Favorite Color) ===\n"

echo "1. Alice votes for Red..."
curl -X POST http://127.0.0.1:8000/api/polls/2/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 1, "voter_identifier": "alice"}'

echo "\n\n2. Bob votes for Blue..."
curl -X POST http://127.0.0.1:8000/api/polls/2/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 2, "voter_identifier": "bob"}'

echo "\n\n3. Charlie votes for Green..."
curl -X POST http://127.0.0.1:8000/api/polls/2/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 3, "voter_identifier": "charlie"}'

echo "\n\n4. Checking Poll #2 Results..."
curl http://127.0.0.1:8000/api/polls/2/results/

echo "\n\n5. Testing duplicate vote (Alice tries to vote again)..."
curl -X POST http://127.0.0.1:8000/api/polls/2/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 2, "voter_identifier": "alice"}'

echo "\n\n=== PART 2: Testing Poll #3 ===\n"

echo "6. David votes for Option 1..."
curl -X POST http://127.0.0.1:8000/api/polls/3/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 4, "voter_identifier": "david"}'

echo "\n\n7. Eve votes for Option 2..."
curl -X POST http://127.0.0.1:8000/api/polls/3/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 5, "voter_identifier": "eve"}'

echo "\n\n8. Checking Poll #3 Results..."
curl http://127.0.0.1:8000/api/polls/3/results/

echo "\n\n=== PART 3: Final Overview ===\n"

echo "9. All polls list:"
curl http://127.0.0.1:8000/api/polls/ | python -m json.tool

echo "\n\n=== TEST COMPLETE ==="

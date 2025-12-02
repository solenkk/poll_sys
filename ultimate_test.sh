#!/bin/bash

echo "=== ULTIMATE POLL SYSTEM TEST ===\n"

echo "Phase 1: Create a comprehensive poll"
curl -X POST http://127.0.0.1:8000/api/polls/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Ultimate Test: Is our poll system working perfectly?",
    "expires_at": "2024-12-31T23:59:59Z",
    "options": [
      {"option_text": "Absolutely Yes! 🎉"},
      {"option_text": "Mostly Yes 👍"},
      {"option_text": "Needs Improvement 🤔"},
      {"option_text": "Not Really 😞"}
    ]
  }'

echo -e "\n\nPhase 2: Simulate realistic voting patterns"
echo "1. 5 users vote for 'Absolutely Yes!'"
for i in {1..5}; do
  curl -s -X POST http://127.0.0.1:8000/api/polls/6/vote/ \
    -H "Content-Type: application/json" \
    -d "{\"option_id\": 12, \"voter_identifier\": \"happy_user_$i\"}" > /dev/null
done

echo "2. 3 users vote for 'Mostly Yes'"
for i in {1..3}; do
  curl -s -X POST http://127.0.0.1:8000/api/polls/6/vote/ \
    -H "Content-Type: application/json" \
    -d "{\"option_id\": 13, \"voter_identifier\": \"ok_user_$i\"}" > /dev/null
done

echo "3. 1 user votes for 'Needs Improvement'"
curl -s -X POST http://127.0.0.1:8000/api/polls/6/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 14, "voter_identifier": "critical_user"}' > /dev/null

echo "4. Try duplicate vote (should fail)"
curl -X POST http://127.0.0.1:8000/api/polls/6/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 15, "voter_identifier": "happy_user_1"}'

echo -e "\n\nPhase 3: Check the impressive results"
curl http://127.0.0.1:8000/api/polls/6/results/

echo -e "\n\nPhase 4: System Statistics"
python manage.py shell -c "
from poll_app.models import Poll, Option, Vote
print('=== SYSTEM STATISTICS ===')
print(f'Total Polls: {Poll.objects.count()}')
print(f'Total Options: {Option.objects.count()}')
print(f'Total Votes: {Vote.objects.count()}')
print(f'Unique Voters: {Vote.objects.values(\"voter_identifier\").distinct().count()}')
"

echo -e "\n=== ULTIMATE TEST COMPLETE ==="
echo "Visit http://127.0.0.1:8000/api/docs/ to see your beautiful API documentation!"

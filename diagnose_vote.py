import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from poll_app.models import Poll, Option, Vote
from poll_app.serializers import VoteCreateSerializer

print("=== DIAGNOSING VOTE CREATION ===\n")

# 1. Check if Poll #2 exists
print("1. Checking Poll #2:")
try:
    poll = Poll.objects.get(id=2)
    print(f"   ✅ Poll exists: '{poll.question}'")
    print(f"   Options in this poll:")
    for option in poll.options.all():
        print(f"   - Option #{option.id}: {option.option_text}")
except Poll.DoesNotExist:
    print("   ❌ Poll #2 does not exist!")
    exit()

# 2. Test creating a vote manually
print("\n2. Testing manual vote creation:")
try:
    # Get an option
    option = Option.objects.get(id=1)  # Red option
    print(f"   Using option: {option.option_text}")
    
    # Try to create a vote directly
    vote = Vote.objects.create(
        option=option,
        voter_identifier="manual_test_user"
    )
    print(f"   ✅ Successfully created vote #{vote.id}")
    print(f"   Voter: {vote.voter_identifier}")
    print(f"   Option: {vote.option.option_text}")
    print(f"   Poll: {vote.option.poll.question}")
except Exception as e:
    print(f"   ❌ Error creating vote: {e}")
    import traceback
    traceback.print_exc()

# 3. Test serializer validation
print("\n3. Testing serializer validation:")
test_data = {"option_id": 1, "voter_identifier": "serializer_test"}
serializer = VoteCreateSerializer(data=test_data)
if serializer.is_valid():
    print("   ✅ Serializer validation passed")
    print(f"   Validated data: {serializer.validated_data}")
    
    # Try to save
    try:
        vote = serializer.save()
        print(f"   ✅ Serializer.save() created vote #{vote.id}")
    except Exception as e:
        print(f"   ❌ Serializer.save() failed: {e}")
else:
    print("   ❌ Serializer validation failed:")
    print(f"   Errors: {serializer.errors}")

# 4. Check final count
print(f"\n4. Final vote count: {Vote.objects.count()}")

print("\n=== DIAGNOSIS COMPLETE ===")

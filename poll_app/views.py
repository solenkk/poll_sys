from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Poll, Option, Vote
from .serializers import PollSerializer, VoteCreateSerializer

class PollListCreateView(generics.ListCreateAPIView):
    """
    Handles:
    - GET /api/polls/ -> Returns list of all polls with their options
    - POST /api/polls/ -> Creates a new poll with options
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

@api_view(['POST'])
def vote_on_poll(request, poll_id):
    """
    Handles POST /api/polls/<poll_id>/vote/
    Allows a user to vote on a specific poll
    """
    poll = get_object_or_404(Poll, id=poll_id)
    
    serializer = VoteCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Create the vote
        vote = Vote.objects.create(
            option_id=serializer.validated_data['option_id'],
            voter_identifier=serializer.validated_data['voter_identifier']
        )
        return Response({"message": "Vote cast successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def poll_results(request, poll_id):
    """
    Handles GET /api/polls/<poll_id>/results/
    Returns the results for a specific poll
    """
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Get all options for this poll with their vote counts
    options = Option.objects.filter(poll=poll)
    results = []
    
    for option in options:
        vote_count = Vote.objects.filter(option=option).count()
        results.append({
            'option_id': option.id,
            'option_text': option.option_text,
            'vote_count': vote_count
        })
    
    total_votes = sum(result['vote_count'] for result in results)
    
    return Response({
        'poll_id': poll.id,
        'question': poll.question,
        'results': results,
        'total_votes': total_votes
    })
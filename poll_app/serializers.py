from rest_framework import serializers
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'voter_identifier', 'created_at']

class PollSerializer(serializers.ModelSerializer):
    # This includes all options when serializing a Poll
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']

class VoteCreateSerializer(serializers.ModelSerializer):
    # Serializer specifically for creating votes
    class Meta:
        model = Vote
        fields = ['option_id', 'voter_identifier']
    
    def validate(self, data):
        """
        Custom validation to ensure the option exists and 
        the voter hasn't already voted in this poll
        """
        option_id = data['option_id']
        voter_identifier = data['voter_identifier']
        
        try:
            option = Option.objects.get(id=option_id)
        except Option.DoesNotExist:
            raise serializers.ValidationError("This option does not exist")
        
        # Check if this voter has already voted in this poll
        if Vote.objects.filter(
            option__poll=option.poll, 
            voter_identifier=voter_identifier
        ).exists():
            raise serializers.ValidationError("You have already voted in this poll")
        
        return data
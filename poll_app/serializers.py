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
    options = OptionSerializer(many=True, required=False)
    
    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']
    
    def create(self, validated_data):
        """
        Custom create method to handle nested option creation
        """
        options_data = validated_data.pop('options', [])
        poll = Poll.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(poll=poll, **option_data)
        
        return poll

class VoteCreateSerializer(serializers.ModelSerializer):
    option_id = serializers.IntegerField()
    
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
            raise serializers.ValidationError({
                "option_id": ["This option does not exist"]
            })
            if Vote.objects.filter(
                option__poll=option.poll, 
                voter_identifier=voter_identifier
            ).exists():
                raise serializers.ValidationError({
                    "non_field_errors": ["You have already voted in this poll"]
                })
        data['option'] = option
        return data
    
    def create(self, validated_data):
        """
        Create and return a new Vote instance
        """
        option = validated_data.pop('option')
        
        vote = Vote.objects.create(
            option=option,
            voter_identifier=validated_data['voter_identifier']
        )
        
        return vote
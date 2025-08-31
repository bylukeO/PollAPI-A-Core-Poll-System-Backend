# polls/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'poll']
        
    def validate_option_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Option text cannot be empty.")
        if len(value.strip()) > 200:
            raise serializers.ValidationError("Option text must be 200 characters or less.")
        return value.strip()

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question_text', 'pub_date', 'options']
        
    def validate_question_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Question text cannot be empty.")
        if len(value.strip()) > 200:
            raise serializers.ValidationError("Question text must be 200 characters or less.")
        return value.strip()
        
    def validate_pub_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Publication date cannot be in the past.")
        return value

class VoteSerializer(serializers.ModelSerializer):
    option_id = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all(),
        source='option'
    )

    class Meta:
        model = Vote
        fields = ['poll', 'option_id']
        
    def validate(self, data):
        poll = data.get('poll')
        option = data.get('option')
        
        if option and poll and option.poll != poll:
            raise serializers.ValidationError("Option does not belong to the specified poll.")
            
        # Check if user already voted (if implementing user authentication)
        # existing_vote = Vote.objects.filter(poll=poll, user=self.context['request'].user).exists()
        # if existing_vote:
        #     raise serializers.ValidationError("You have already voted on this poll.")
            
        return data
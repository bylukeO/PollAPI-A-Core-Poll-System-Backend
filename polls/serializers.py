# polls/serializers.py
from rest_framework import serializers
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text']

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question_text', 'pub_date', 'options']

class VoteSerializer(serializers.ModelSerializer):
    option_id = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all(),
        source='option'
    )

    class Meta:
        model = Vote
        fields = ['poll', 'option_id']
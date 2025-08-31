# polls/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer

class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        poll_id = self.kwargs['pk']
        
        # Validate poll exists
        poll = get_object_or_404(Poll, pk=poll_id)
        
        data = request.data.copy()
        data['poll'] = poll_id
        
        # Validate option_id is provided
        if 'option_id' not in data or not data['option_id']:
            return Response(
                {'error': 'option_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate option exists and belongs to poll
        try:
            option = Option.objects.get(pk=data['option_id'])
            if option.poll.pk != poll.pk:
                return Response(
                    {'error': 'Option does not belong to this poll'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Option.DoesNotExist:
            return Response(
                {'error': 'Option does not exist'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VoteList(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class OptionList(generics.ListCreateAPIView):
    serializer_class = OptionSerializer
    
    def get_queryset(self):
        poll_id = self.kwargs.get('poll_id')
        if poll_id:
            return Option.objects.filter(poll=poll_id)
        return Option.objects.all()
    
    def perform_create(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        if poll_id:
            serializer.save(poll_id=poll_id)
        else:
            serializer.save()

class OptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
# polls/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer

class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Update the vote count on the option
        option = serializer.validated_data['option']
        option.votes += 1
        option.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
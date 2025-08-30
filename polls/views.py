# polls/views.py
from rest_framework import generics
from .models import Poll, Option
from .serializers import PollSerializer, OptionSerializer

class PollList(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
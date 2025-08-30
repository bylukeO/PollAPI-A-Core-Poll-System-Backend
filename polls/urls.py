# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('polls/', views.PollList.as_view(), name='poll-list'),
    path('polls/<int:pk>/', views.PollDetail.as_view(), name='poll-detail'),
    path('polls/<int:pk>/vote/', views.VoteCreate.as_view(), name='poll-vote'),
]
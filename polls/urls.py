# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('polls/', views.PollList.as_view(), name='poll-list'),
    path('polls/<int:pk>/', views.PollDetail.as_view(), name='poll-detail'),
    path('polls/<int:pk>/vote/', views.VoteCreate.as_view(), name='poll-vote'),
    path('polls/<int:poll_id>/options/', views.OptionList.as_view(), name='poll-options'),
    path('options/', views.OptionList.as_view(), name='option-list'),
    path('options/<int:pk>/', views.OptionDetail.as_view(), name='option-detail'),
    path('votes/', views.VoteList.as_view(), name='vote-list'),
]
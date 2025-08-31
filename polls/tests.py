from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Poll, Option, Vote
from datetime import timedelta

# Model Tests
class PollModelTest(TestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)
        self.poll = Poll.objects.create(
            question_text="Test question?",
            pub_date=self.future_date
        )
    
    def test_poll_creation(self):
        """Test that a poll is created correctly"""
        self.assertEqual(self.poll.question_text, "Test question?")
        self.assertEqual(self.poll.pub_date, self.future_date)
        self.assertTrue(isinstance(self.poll, Poll))
    
    def test_poll_str_method(self):
        """Test the string representation of poll"""
        self.assertEqual(str(self.poll), "Test question?")
    
    def test_poll_question_max_length(self):
        """Test question text max length constraint"""
        max_length = self.poll._meta.get_field('question_text').max_length
        self.assertEqual(max_length, 200)

class OptionModelTest(TestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)
        self.poll = Poll.objects.create(
            question_text="Test question?",
            pub_date=self.future_date
        )
        self.option = Option.objects.create(
            poll=self.poll,
            option_text="Test option"
        )
    
    def test_option_creation(self):
        """Test that an option is created correctly"""
        self.assertEqual(self.option.option_text, "Test option")
        self.assertEqual(self.option.poll, self.poll)
        self.assertTrue(isinstance(self.option, Option))
    
    def test_option_str_method(self):
        """Test the string representation of option"""
        self.assertEqual(str(self.option), "Test option")
    
    def test_option_belongs_to_poll(self):
        """Test that option is associated with correct poll"""
        self.assertEqual(self.option.poll.pk, self.poll.pk)
    
    def test_option_text_max_length(self):
        """Test option text max length constraint"""
        max_length = self.option._meta.get_field('option_text').max_length
        self.assertEqual(max_length, 200)

class VoteModelTest(TestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)
        self.poll = Poll.objects.create(
            question_text="Test question?",
            pub_date=self.future_date
        )
        self.option = Option.objects.create(
            poll=self.poll,
            option_text="Test option"
        )
        self.vote = Vote.objects.create(
            poll=self.poll,
            option=self.option
        )
    
    def test_vote_creation(self):
        """Test that a vote is created correctly"""
        self.assertEqual(self.vote.poll, self.poll)
        self.assertEqual(self.vote.option, self.option)
        self.assertTrue(isinstance(self.vote, Vote))
    
    def test_vote_relationships(self):
        """Test that vote has correct relationships"""
        self.assertEqual(self.vote.poll.pk, self.poll.pk)
        self.assertEqual(self.vote.option.pk, self.option.pk)
        self.assertEqual(self.vote.option.poll.pk, self.poll.pk)

# API Tests
class PollAPITest(APITestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)
        self.poll_data = {
            'question_text': 'What is your favorite color?',
            'pub_date': self.future_date.isoformat()
        }
        self.poll = Poll.objects.create(
            question_text="Existing poll?",
            pub_date=self.future_date
        )
    
    def test_get_polls_list(self):
        """Test retrieving list of polls"""
        url = reverse('poll-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_poll(self):
        """Test creating a new poll"""
        url = reverse('poll-list')
        response = self.client.post(url, self.poll_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 2)
    
    def test_get_poll_detail(self):
        """Test retrieving a specific poll"""
        url = reverse('poll-detail', kwargs={'pk': self.poll.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question_text'], 'Existing poll?')
    
    def test_create_poll_invalid_data(self):
        """Test creating poll with invalid data"""
        url = reverse('poll-list')
        invalid_data = {'question_text': '', 'pub_date': self.future_date.isoformat()}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class VotingAPITest(APITestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)
        self.poll = Poll.objects.create(
            question_text="Test poll?",
            pub_date=self.future_date
        )
        self.option1 = Option.objects.create(
            poll=self.poll,
            option_text="Option 1"
        )
        self.option2 = Option.objects.create(
            poll=self.poll,
            option_text="Option 2"
        )
    
    def test_submit_vote(self):
        """Test submitting a valid vote"""
        url = reverse('poll-vote', kwargs={'pk': self.poll.pk})
        vote_data = {'option_id': self.option1.pk}
        response = self.client.post(url, vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)
    
    def test_vote_invalid_option(self):
        """Test voting with invalid option ID"""
        url = reverse('poll-vote', kwargs={'pk': self.poll.pk})
        vote_data = {'option_id': 999}
        response = self.client.post(url, vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_vote_missing_option_id(self):
        """Test voting without option_id"""
        url = reverse('poll-vote', kwargs={'pk': self.poll.pk})
        vote_data = {}
        response = self.client.post(url, vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_vote_invalid_poll(self):
        """Test voting on non-existent poll"""
        url = reverse('poll-vote', kwargs={'pk': 999})
        vote_data = {'option_id': self.option1.pk}
        response = self.client.post(url, vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_votes_list(self):
        """Test retrieving list of votes"""
        Vote.objects.create(poll=self.poll, option=self.option1)
        url = reverse('vote-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class OptionAPITest(APITestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)
        self.poll = Poll.objects.create(
            question_text="Test poll?",
            pub_date=self.future_date
        )
        self.option = Option.objects.create(
            poll=self.poll,
            option_text="Test option"
        )
    
    def test_get_options_list(self):
        """Test retrieving list of all options"""
        url = reverse('option-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_poll_options(self):
        """Test retrieving options for specific poll"""
        url = reverse('poll-options', kwargs={'poll_id': self.poll.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_option(self):
        """Test creating a new option"""
        url = reverse('option-list')
        option_data = {'option_text': 'New option', 'poll': self.poll.pk}
        response = self.client.post(url, option_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Option.objects.count(), 2)
    
    def test_get_option_detail(self):
        """Test retrieving specific option"""
        url = reverse('option-detail', kwargs={'pk': self.option.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['option_text'], 'Test option')
    
    def test_update_option(self):
        """Test updating an option"""
        url = reverse('option-detail', kwargs={'pk': self.option.pk})
        update_data = {'option_text': 'Updated option', 'poll': self.poll.pk}
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.option.refresh_from_db()
        self.assertEqual(self.option.option_text, 'Updated option')
    
    def test_delete_option(self):
        """Test deleting an option"""
        url = reverse('option-detail', kwargs={'pk': self.option.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Option.objects.count(), 0)

class EdgeCaseTest(APITestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)
        self.past_date = timezone.now() - timedelta(days=1)
        
    def test_create_poll_with_past_date(self):
        """Test creating poll with past publication date"""
        url = reverse('poll-list')
        poll_data = {
            'question_text': 'Test question?',
            'pub_date': self.past_date.isoformat()
        }
        response = self.client.post(url, poll_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Publication date cannot be in the past', str(response.data))
    
    def test_create_option_empty_text(self):
        """Test creating option with empty text"""
        poll = Poll.objects.create(
            question_text="Test poll?",
            pub_date=self.future_date
        )
        url = reverse('option-list')
        option_data = {'option_text': '', 'poll': poll.pk}
        response = self.client.post(url, option_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', str(response.data))
    
    def test_create_option_too_long_text(self):
        """Test creating option with text too long"""
        poll = Poll.objects.create(
            question_text="Test poll?",
            pub_date=self.future_date
        )
        url = reverse('option-list')
        long_text = 'a' * 201  # 201 characters
        option_data = {'option_text': long_text, 'poll': poll.pk}
        response = self.client.post(url, option_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Ensure this field has no more than 200 characters', str(response.data))
    
    def test_vote_with_wrong_poll_option(self):
        """Test voting with option from different poll"""
        poll1 = Poll.objects.create(question_text="Poll 1?", pub_date=self.future_date)
        poll2 = Poll.objects.create(question_text="Poll 2?", pub_date=self.future_date)
        option1 = Option.objects.create(poll=poll1, option_text="Option 1")
        option2 = Option.objects.create(poll=poll2, option_text="Option 2")
        
        # Try to vote on poll1 with option from poll2
        url = reverse('poll-vote', kwargs={'pk': poll1.pk})
        vote_data = {'option_id': option2.pk}
        response = self.client.post(url, vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Option does not belong to this poll', str(response.data))
    
    def test_nonexistent_endpoints(self):
        """Test accessing non-existent resources"""
        # Non-existent poll
        url = reverse('poll-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Non-existent option
        url = reverse('option-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

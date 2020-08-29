from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

import datetime


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# Create your tests here.
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
    	"""
    	If no questions exist, an appropriate message is displayed.
    	"""
    	response = self.client.get(reverse('polls:index'))
    	self.assertEqual(response.status_code, 200)
    	self.assertContains(response, "No polls available.")
    	self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
    	"""
    	Questions with a pub_date in the past are displayed on the index page.
    	"""
    	create_question("Past question.", -30)
    	response = self.client.get(reverse("polls:index"))
    	self.assertQuerysetEqual(response.context['latest_question_list'],
    		['<Question: Past question.>']
    	)

    def test_future_question(self):
    	"""
		Questions with a future pub_date don't display.
    	"""
    	create_question("Future question.", 30)
    	response = self.client.get(reverse('polls:index'))
    	self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
    	"""
		Even if both past and future question exist, only past questions display.
    	"""
    	create_question("Past question.", -30)
    	create_question("Future question.", 30)
    	response = self.client.get(reverse('polls:index'))
    	self.assertQuerysetEqual(response.context['latest_question_list'],
    		['<Question: Past question.>']
    	)

    def test_two_past_questions(self):
    	"""
    	Two existing past questions will display in order.
    	"""
    	create_question("Newer past question.", -5)
    	create_question("Older past question.", -30)
    	response = self.client.get(reverse('polls:index'))
    	self.assertQuerysetEqual(response.context['latest_question_list'],
    		['<Question: Newer past question.>',
    		'<Question: Older past question.>']
    		)


class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		"""
		A future question should return a 404 error.
		"""
		future_question = create_question("Future question.",30)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code,404)

	def test_past_question(self):
		"""
		A past question should display.
		"""
		past_question = create_question('Past question.',-5)
		url = reverse('polls:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code,200)
		self.assertContains(response,past_question.question_text)



class QuestionModelTests(TestCase):
	def test_was_pub_recent_with_future_questions(self):
		"""
		was_pub_recent() returns False for questions whose pub_date is in the future.
		"""
		future_date = timezone.now() + datetime.timedelta(days=10)
		future_question = Question(pub_date=future_date)

		self.assertIs(future_question.was_pub_recent(), False)


	def test_was_pub_recent_with_old_questions(self):
		"""
		was_pub_recent() returns False on question with pub_date in the past.
		"""
		old_date = timezone.now() - datetime.timedelta(days=1,seconds=1)
		old_question = Question(pub_date=old_date)

		self.assertIs(old_question.was_pub_recent(), False)

	def test_was_pub_recent_with_new_questions(self):
		"""
		was_pub_recent() returns True on question just published.
		"""
		new_question = Question(pub_date=timezone.now())

		self.assertIs(new_question.was_pub_recent(), True)


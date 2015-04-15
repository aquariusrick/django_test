import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Question


# Create your tests here.
class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_recent_question(self):
        q = Question(pub_date=timezone.now() + datetime.timedelta(hours=-1))
        self.assertTrue(q.was_published_recently(), "was_published_recently() returns True when pub_date is in "
                                                    "the recent past.")

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() should return False for questions published in the future"""
        q = Question(pub_date=timezone.now() + datetime.timedelta(hours=1))
        self.assertFalse(q.was_published_recently(), "was_published_recently() returns False when pub_date is in "
                                                     "the future.")

    def test_was_published_recently_with_old_question(self):
        q = Question(pub_date=timezone.now() + datetime.timedelta(days=-1, hours=-1))
        self.assertFalse(q.was_published_recently(), "was_published_recently() returns False when pub_date is in "
                                                     "the distant past.")

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """If no questions exist, show the message"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200, msg="Status code is 200")
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [], "No questions in context.")

    def test_index_view_with_a_past_question(self):
        """Should show a question on the view"""
        create_question("Is this a past test?", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Is this a past test?>'],
                                 msg="List contains the past question")

    def test_index_view_with_a_future_question(self):
        """Should not show future questions"""
        create_question("Is this a future test?", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200, msg="Status code is 200")
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])




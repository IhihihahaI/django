from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.core.urlresolvers import reverse

# Create your tests here.

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionMethodTests(TestCase):
    def test_published_recentlly_via_future(self):
        time = timezone.now() + datetime.timedelta(days = 30)
        question_to_test = Question(pub_date = time)
        self.assertEqual(question_to_test.published_recently(), False)

    def test_published_recently_via_recent(self):
        time = timezone.now() - datetime.timedelta(hours = 1)
        question_to_test = Question(pub_date = time)
        self.assertEqual(question_to_test.published_recently(), True)

    def test_published_recently_via_old(self):
        time = timezone.now() - datetime.timedelta(days = 30)
        question_to_test = Question(pub_date = time)
        self.assertEqual(question_to_test.published_recently(), False)

class QuestionViewTests(TestCase):
    def test_index_view_via_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_via_past_question(self):
        create_question(question_text = "Past question.", days = -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: Past question.>"]
        )

    def test_index_view_via_future_question(self):
        create_question(question_text = "Future question", days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_via_future_and_past_questions(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_via_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_via_future_question(self):
        future_question = create_question(question_text = "Future question.", days = 5)
        url = reverse("polls:detail", args = (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_via_past_question(self):
        past_question = create_question(question_text = "Past question.", days = -5)
        url = reverse("polls:detail", args = (past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

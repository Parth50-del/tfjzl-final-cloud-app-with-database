from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Choice, Course, Enrollment, Question, Submission


class QuestionModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Django',
            image='course_images/django.png',
            description='Django course',
        )
        self.user = get_user_model().objects.create_user(username='learner')
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course,
        )
        self.question = Question.objects.create(
            course=self.course,
            question_text='Which is correct?',
        )
        self.correct_choice = Choice.objects.create(
            question=self.question,
            choice_text='Correct',
            is_correct=True,
        )
        self.incorrect_choice = Choice.objects.create(
            question=self.question,
            choice_text='Incorrect',
        )

    def test_quiz_field_definitions(self):
        question_text = Question._meta.get_field('question_text')
        grade = Question._meta.get_field('grade')
        choice_text = Choice._meta.get_field('choice_text')
        is_correct = Choice._meta.get_field('is_correct')

        self.assertEqual(question_text.get_internal_type(), 'CharField')
        self.assertEqual(question_text.max_length, 200)
        self.assertEqual(grade.get_internal_type(), 'IntegerField')
        self.assertEqual(grade.default, 0)
        self.assertEqual(choice_text.get_internal_type(), 'CharField')
        self.assertEqual(choice_text.max_length, 200)
        self.assertEqual(is_correct.get_internal_type(), 'BooleanField')
        self.assertFalse(is_correct.default)

    def test_is_get_score_requires_exact_correct_choices(self):
        self.assertTrue(self.question.is_get_score([self.correct_choice.id]))
        self.assertFalse(self.question.is_get_score([self.incorrect_choice.id]))
        self.assertFalse(
            self.question.is_get_score(
                [self.correct_choice.id, self.incorrect_choice.id]
            )
        )
        self.assertFalse(self.question.is_get_score([]))

    def test_model_string_representations(self):
        self.assertEqual(str(self.question), 'Which is correct?')
        self.assertEqual(str(self.correct_choice), 'Correct')

        submission = Submission.objects.create(enrollment=self.enrollment)
        self.assertEqual(
            str(submission),
            f'Submission {submission.id} for enrollment {self.enrollment.id}',
        )

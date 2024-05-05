from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Tag, Question, Comment


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.tag = Tag.objects.create(caption='Test Tag')
        self.question = Question.objects.create(
            title='Test Title',
            excerpt='Test Excerpt',
            content='This is a test content',
            user=self.user
        )
        self.comment = Comment.objects.create(
            user=self.user,
            text='This is a test comment',
            question=self.question
        )

    def test_tag_creation(self):
        """Test Tag model creation."""
        tag = Tag.objects.create(caption='New Tag')
        self.assertEqual(tag.caption, 'New Tag')

    def test_question_creation(self):
        """Test Question model creation."""
        question = Question.objects.create(
            title='New Title',
            excerpt='New Excerpt',
            content='New content',
            user=self.user
        )
        question.tag.add(self.tag)  # Associate the existing tag with the question
        self.assertEqual(question.title, 'New Title')
        self.assertEqual(question.slug, 'new-title')
        self.assertIn(self.tag, question.tag.all())

    def test_comment_creation(self):
        """Test Comment model creation."""
        comment = Comment.objects.create(
            user=self.user,
            text='New comment',
            question=self.question
        )
        self.assertEqual(comment.text, 'New comment')

    def test_unique_question_constraint(self):
        """Test unique constraint on Question model."""
        with self.assertRaises(Exception):
            Question.objects.create(
                title='Test Title',
                excerpt='Test Excerpt',
                content='This is a test content',
                user=self.user
            )

    def test_question_user_relationship(self):
        """Test relationship between Question and User."""
        self.assertEqual(self.question.user, self.user)

    def test_comment_user_relationship(self):
        """Test relationship between Comment and User."""
        self.assertEqual(self.comment.user, self.user)

    def test_question_comment_relationship(self):
        """Test relationship between Question and Comment."""
        self.assertIn(self.comment, self.question.comments.all())

    def test_question_deletion_cascade(self):
        """Test cascade deletion of related objects."""
        question_id = self.question.id
        self.question.delete()
        self.assertIsNone(Question.objects.filter(id=question_id).first())
        self.assertIsNone(Comment.objects.filter(question_id=question_id).first())

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Post, Comment, Like

class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_signup(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password1': 'password123', 'password2': 'password123'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login after logout

class PostTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(content="A sample post", user=self.user)

    def test_create_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_create'), {'content': 'A new post'})
        self.assertEqual(response.status_code, 302)  # Redirect after post creation
        self.assertEqual(Post.objects.count(), 2)

    def test_delete_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

class CommentTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(content="A sample post", user=self.user)
        self.comment = Comment.objects.create(content="A sample comment", user=self.user, post=self.post)

    def test_create_comment(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('comment_create', kwargs={'pk': self.post.pk}), {'content': 'A new comment'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 2)

    def test_delete_comment(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('comment_delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

class LikeTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(content="A sample post", user=self.user)

    def test_like_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('like', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Like.objects.filter(post=self.post).count(), 1)

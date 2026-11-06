import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from requests import post
from django.contrib.auth.models import User

from .models import Post

#from polls.app import user

def create_post(title, days):
    
    """
    Create a post with the given `title` and published the
    given number of `days` offset to now (negative for posts published
    in the past, positive for posts that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    user = User.objects.create_user(username="testuser"+str(time), password="password2025")
    return Post.objects.create(title=title, author=user, content="ding dong", created=time)

class PostModelTests(TestCase):

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() returns False for posts whose created
        date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(created=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_old_post(self):
        """
        was_published_recently() returns False for posts whose created
        date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_post = Post(created=time)
        self.assertIs(old_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_post(self):
        """
        was_published_recently() returns True for posts whose created
        date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_post = Post(created=time)
        self.assertIs(recent_post.was_published_recently(), True)


class PostIndexViewTests(TestCase):
    def test_no_posts(self):
        """
        If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerySetEqual(response.context['posts'], [])
        
        #self.assertQuerySetEqual(response.context['latest_post_list'], [])

    def test_past_post(self):
        """
        Posts with a created date in the past are displayed on the
        index page.
        """
        
        #time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        #old_post = Post(created=time)
        create_post(title="Test Post", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['posts'],['<Post: Test Post>'],transform=repr,
        )

    def test_future_post(self):
        """
        Posts with a created date in the future aren't displayed on
        the index page.
        """
        create_post(title="Future post.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No posts are available.")
        self.assertQuerySetEqual(response.context['posts'], [])

    def test_future_post_and_past_post(self):
        """
        Even if both past and future posts exist, only past posts
        are displayed.
        """
        create_post(title="Past post.", days=-30)
        create_post(title="Future post.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['posts'],
            ['<Post: Past post.>'],transform=repr,
        )

    def test_two_past_posts(self):
        """
        The posts index page may display multiple posts.
        """
        create_post(title="Past post 1.", days=-30)
        create_post(title="Past post 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['posts'],
            ['<Post: Past post 2.>', '<Post: Past post 1.>'],transform=repr,
        )
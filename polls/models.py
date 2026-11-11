import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    votes = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now

    def __str__(self):
        return self.title

class SecurityEvent(models.Model):
    class EventType(models.TextChoices):
        LOGIN_FAILED = "login_failed", "Failed login"
        LOGIN_SUCCESS = "login_success", "Login success"
        LOGOUT = "logout", "Logout"

    event = models.CharField(max_length=32, choices=EventType.choices)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.get_event_display()} — {self.timestamp}"

# SECURITY FLAW 2: Cryptographic Failure.
# Fix by removing the Plain_And_WeakPasswordHashDemo model 
# and related code from views.py and admin.py.
class Plain_And_WeakPasswordHashDemo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="plain_and_weak_password_hash_demo"
    )
    username = models.CharField(max_length=150)
    password_md5 = models.CharField(max_length=32)
    password_plaintext = models.CharField(max_length=128)

    def __str__(self):
        return f"Password leak demo: {self.user.username}"       
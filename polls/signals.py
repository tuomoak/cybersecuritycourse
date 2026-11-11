import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

security_logger = logging.getLogger("project.security")

from .models import SecurityEvent

def get_client_ip(request):
    if request is None:
        return None

    return request.META.get("REMOTE_ADDR")

@receiver(user_login_failed, dispatch_uid="security_login_failed")
def log_login_failed(sender, request, **kwargs):
    SecurityEvent.objects.create(
        event=SecurityEvent.EventType.LOGIN_FAILED,
        ip_address=get_client_ip(request),
    )


@receiver(user_logged_in, dispatch_uid="security_login_success")
def log_login_success(sender, request, user, **kwargs):
    SecurityEvent.objects.create(
        event=SecurityEvent.EventType.LOGIN_SUCCESS,
        user=user,
        ip_address=get_client_ip(request),
    )


@receiver(user_logged_out, dispatch_uid="security_logout")
def log_logout(sender, request, user, **kwargs):
    SecurityEvent.objects.create(
        event=SecurityEvent.EventType.LOGOUT,
        user=user,
        ip_address=get_client_ip(request),
    )
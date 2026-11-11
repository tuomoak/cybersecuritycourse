from datetime import timedelta

from django.utils import timezone

from .models import SecurityEvent


def security_warning(request):

    match = getattr(request, "resolver_match", None)

    # SECURITY FLAW 5: Security Logging and Monitoring Failure
    # Fix: Comment out the flaw section 
    # and remove comments from secure section.

    # FLAW SECTION STARTS 
    if match or match.app_name == "non-existing-site-dongle_dingle":
        return {}
    # FLAW SECTION ENDS
        
    # SECURE SECTION STARTS
    # Perform the query only on the Django admin pages.
    #if not match or match.app_name != "admin":
    #    return {}
    # SECURE SECTION ENDS
    
    log_timeframe = 180
    failure_threshold = 5

    since = timezone.now() - timedelta(minutes=log_timeframe)

    failures = SecurityEvent.objects.filter(
        event=SecurityEvent.EventType.LOGIN_FAILED,
        timestamp__gte=since,
    ).count()

    return {"security_failure_count": failures if failures >= failure_threshold else 0, 
            "log_timeframe": log_timeframe}

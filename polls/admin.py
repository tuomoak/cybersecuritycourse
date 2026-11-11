
from django.contrib import admin, messages
from .models import Post
from .models import SecurityEvent
from datetime import timedelta
from django.utils import timezone

# Security flaw 2: Cryptographic Failure.
# Fix by removing the Plain_And_WeakPasswordHashDemo model 
# and related code in views.py, models.py and admin.py.
from .models import Plain_And_WeakPasswordHashDemo

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created')
    list_filter = ['created']
    search_fields = ['title', 'content', 'author__username']

@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "event", "user", "ip_address")
    list_filter = ("event", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)

    readonly_fields = ("event", "timestamp", "user", "ip_address")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False    

# Security flaw 2: Cryptographic Failure.
# Fix by commenting out code classes below and admin.site ungerister/register.
# Also comment out related code from models.py and views.py.

# FLAW SECTION STARTS
class Plain_And_WeakPasswordHashDemoInline(admin.StackedInline):
    model = Plain_And_WeakPasswordHashDemo
    can_delete = False
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = (Plain_And_WeakPasswordHashDemoInline,
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 
# FLAW SECTION ENDS

admin.site.register(Post, PostAdmin)
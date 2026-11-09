
from django.contrib import admin
from .models import Post

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

# Security flaw 2: Cryptographic Failure.
# Fix by commenting out code classes below and admin.site ungerister/register.
# Also comment out related code from models.py and views.py.

# (Start comment out here)
class Plain_And_WeakPasswordHashDemoInline(admin.StackedInline):
    model = Plain_And_WeakPasswordHashDemo
    can_delete = False
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = (Plain_And_WeakPasswordHashDemoInline,
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 
# (Comment out all the way here.)

admin.site.register(Post, PostAdmin)

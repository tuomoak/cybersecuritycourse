from datetime import datetime
from django.contrib import messages
from django.db import connection
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post

# Security flaw 2: Cryptographic Failure.
# Fix by commenting out import of Plain_And_WeakPasswordHashDemo model and hashlib import.
# + also codes related to this in views.py, admin.py and models.py.
from.models import Plain_And_WeakPasswordHashDemo
import hashlib
# (Comment out all the way here.)

from django.views import generic
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            #SECURITY FLAW 2: Cryptographic Failure.
            #Storing weak password hashes and plaintext passwords.
            # Fix by commenting out code below, 
            # and using Django's built-in password hashing mechanism.
           
            # """ Start comment out here 
            password = form.cleaned_data["password1"]
            weak_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
            password_plaintext=form.cleaned_data["password1"]
    
            Plain_And_WeakPasswordHashDemo.objects.create(
                user=user,
                username=user.username,
                password_md5=weak_hash,
                password_plaintext=password_plaintext
            )
            # """ # Comment out all the way here. 
 
            login(request, user)
            return redirect("polls:postlist")
    
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
  

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("polls:postlist")

    else:
        form = PostForm()

    return render(request, "polls/add_post.html", {"form": form})

@login_required
def find_post(request):
    query = request.GET.get("q", "").strip()
    results = []
    users = []

    #Security flaw 3: Injection
    # Fix: Comment out flawed row and sections, 
    # and remove comments from safe row and safe section. 
    
    if query:       
        # Flawed
        search = f"SELECT id FROM auth_user WHERE username = '{query}'"
                    
        # Safe
        #users = User.objects.filter(username=query)
        
    try:
        # Flawed section
        with connection.cursor() as cursor:
            cursor.execute(search)
            users = cursor.fetchall()
        
        if users:
            user_ids = [user[0] for user in users]
            results = Post.objects.filter(author_id__in=user_ids)

        # Flawed section ends

        # Safe section
        #user_ids = [user.id for user in users]
        #results = Post.objects.filter(author_id__in=user_ids)
        
    except:
         results = []
         users = []

    return render(request, "polls/find_post.html", { "query": query, 
            "results": results, "user_count": len(users) if query else 0 })

def postlist(request):
    posts = Post.objects.filter(created__lte=timezone.now()
            ).order_by('-created')    
    return render(request, "polls/index.html", {"posts": posts})

# SECURITY FLAW 1: Broken access control. 
# The remove_post view does not properly check if the user is authorized to delete the post.
# Fix by removing comments from the if-else clause, and remove post.delete() before the if clause.

def remove_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()  # comment this out when fixing the flaw  
    #if post.author == request.user:
    #    post.delete()
    #else: 
    #    # Handle the case where a user are not authorized to delete the post
    #    errormessage = f"You are not authorized to delete: {post.title}."
    #    messages.error(request, errormessage)
    #    return redirect("polls:postlist")
            
    return redirect("polls:postlist")

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'polls/detail.html', {'post': post})
    
def results(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'polls/results.html', {'post': post})
    
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Return published posts (not including those set to be
        published in the future).
        """
        return Post.objects.filter(created__lte=timezone.now()
        ).order_by('-created')
            
class DetailView(generic.DetailView):
    model = Post
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(created__lte=timezone.now())
        
class ResultsView(generic.DetailView):
    model = Post
    template_name = 'polls/results.html'

def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.POST.get('vote') == 'upvote':
                post.upvotes += 1
                post.votes += 1
                
    elif request.POST.get('vote') == 'downvote':
                post.downvotes += 1
                post.votes -= 1
                
    else:
        # Handle the case where no valid vote option was selected
        return render(request, 'polls/detail.html', {
            'post': post,
            'error_message': "You didn't select a valid vote option.",
        })
              
    post.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:detail', args=(post.id,)))
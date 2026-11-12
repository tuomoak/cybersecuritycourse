from datetime import datetime
from django.contrib import messages
from django.db import connection
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Imports related to Security flaw 2: Cryptographic Failure.
from.models import Plain_And_WeakPasswordHashDemo
import hashlib
# FLAW Imports ENDS HERE

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            #SECURITY FLAW 2: CRYPTOGRAPHIC FAILURE
            # Fix by commenting out code below (+ imports)
            # and also related code in models.py, admin.py
            # and just using Django's built-in password hashing mechanism.
           
            # FLAW SECTION STARTS HERE 
            password = form.cleaned_data["password1"]
            weak_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
            password_plaintext=form.cleaned_data["password1"]
    
            Plain_And_WeakPasswordHashDemo.objects.create(
                user=user,
                username=user.username,
                password_md5=weak_hash,
                password_plaintext=password_plaintext
            )
            # FLAW SECTION ENDS HERE 
 
            login(request, user)
            return redirect("polls:postlist")
    
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})

def sign_in(request):
    error = None
    form = AuthenticationForm(request.POST)

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(
        request,
        username=username,
        password=password,
    )   
        # SECURITY FLAW 4: IDENTIFICATION AND AUTHENTICATION FAILURES
        # Fix by uncommenting flaw section 
        # and removing comments from secure section

        ### FLAW SECTION STARTS HERE
        
        user_check = User.objects.filter(username=username)
                
        if not user_check.exists():
            error = "The user does not exist."
                
        else:
            try:
                login(request, user)
                return redirect("polls:postlist")
            except:
                error = "Password is incorrect."
        
        # FLAW SECTION ENDS HERE
               
        # SECURE SECTION STARTS
        """"
        if user is None:
             error = "Incorrect username or password."
        else:
            login(request, user)
            return redirect("polls:postlist")
        """
        # SECURE SECTION ENDS
        
    return render(request, "registration/login.html", {"form":form, "error": error})

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

    # SECURITY FLAW 3: INJECTION
    # FIX: Comment out two flaw sections
    # and remove comments from two secure sections. 
    
    if query:       
        # FLAW SECTION 1/2
        search = f"SELECT id FROM auth_user WHERE username = '{query}'"
        # FLAW SECTION 1/2 ENDS
                    
        # SECURE SECTION 1/2
        #users = User.objects.filter(username=query)
        # SECURE SECTION 1/2 ENDS 
    try:
        # FLAW SECTION 2/2 STARTS
        with connection.cursor() as cursor:
            cursor.execute(search)
            users = cursor.fetchall()
        
        if users:
            user_ids = [user[0] for user in users]
            results = Post.objects.filter(author_id__in=user_ids)
        # FLAW SECTION 2/2 ENDS

        # SECURE SECTION 2/2 STARTS
        #user_ids = [user.id for user in users]
        #results = Post.objects.filter(author_id__in=user_ids)
        # SECURE SECTION 2/2 ENDS

    except:
         results = []
         users = []

    return render(request, "polls/find_post.html", { "query": query, 
            "results": results, "user_count": len(users) if query else 0 })

@login_required
def postlist(request):
    posts = Post.objects.filter(created__lte=timezone.now()
            ).order_by('-created')    
    return render(request, "polls/index.html", {"posts": posts})

# SECURITY FLAW 1: BROKEN ACCESS CONTROL. 
# Fix: comment out flaw section and uncomment secure section.

@login_required
def remove_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # FLAW SECTION STARTS 
    post.delete()    
    # FLAW SECTION ENDS
    
    # SECURE SECTION STARTS
    #if post.author == request.user:
    #    post.delete()
    #else:
    #    errormessage = f"You are not authorized to delete: {post.title}."
    #    messages.error(request, errormessage)
    #    return redirect("polls:postlist")
    # SECURE SECTION ENDS HERE
            
    return redirect("polls:postlist")

@login_required
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'polls/detail.html', {'post': post})

@login_required
def results(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'polls/results.html', {'post': post})

@login_required
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

    return HttpResponseRedirect(reverse('polls:detail', args=(post.id,)))
    
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
            
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'polls/detail.html'
        
    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(created__lte=timezone.now())
        
class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'polls/results.html'
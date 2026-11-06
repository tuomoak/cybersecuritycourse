from django.shortcuts import get_object_or_404,render
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.views import generic
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
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

def postlist(request):
    posts = Post.objects.all().order_by("-created")
    return render(request, "polls/index.html", {"posts": posts})

def remove_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
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
        """Return the last five published questions."""
        return Post.objects.all().order_by("-created")
        
class DetailView(generic.DetailView):
    model = Post
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
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
        
    #selected_choice.votes += 1
    #selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:detail', args=(post.id,)))
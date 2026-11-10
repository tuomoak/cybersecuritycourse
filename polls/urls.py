from django.urls import path
from . import views
    
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:post_id>/vote/', views.vote, name='vote'),
    path("add/", views.add_post, name="add_post"),
    path("list/", views.postlist, name="postlist"),
    path("remove/<int:post_id>/", views.remove_post, name="remove_post"),
    path("register/", views.register, name="register"),
    path("find/", views.find_post, name="find_post"),
    path("login/", views.sign_in, name="login"),
    ]
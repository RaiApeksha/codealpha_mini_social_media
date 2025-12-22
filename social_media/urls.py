from django.urls import path
from . import views

urlpatterns = [
    path('posts/create/', views.create_post),
    path('posts/', views.list_posts),
    path('posts/like/', views.like_post),
    path('comments/add/', views.add_comment),
    path('follow/', views.follow_user),
    path('feed/', views.feed),

]

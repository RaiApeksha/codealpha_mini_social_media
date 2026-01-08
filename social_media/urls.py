from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.list_posts, name='posts'),
    path('posts/create/', views.create_post),

    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),
    path("upload-avatar/", views.upload_avatar, name="upload_avatar"),
    path("follow/", views.follow_user, name="follow_user"),
    path('follow/', views.follow_user),
]

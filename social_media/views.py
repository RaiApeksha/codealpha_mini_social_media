from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json

from .models import Post, Comment, Follow

@csrf_exempt
@login_required
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')

        post = Post.objects.create(
            user=request.user,
            content=content
        )

        return JsonResponse({
            'status': 'success',
            'post_id': post.id,
            'content': post.content
        })
def list_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    data = []

    for post in posts:
        comments = []
        for c in post.comments.all():
            comments.append({
                'user': c.user.username,
                'text': c.text
            })

        data.append({
            'id': post.id,
            'user': post.user.username,
            'content': post.content,
            'likes': post.likes.count(),
            'comments': comments
        })

    return JsonResponse({'posts': data})

@csrf_exempt
@login_required
def add_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        text = data.get('text')

        post = Post.objects.get(id=post_id)

        Comment.objects.create(
            user=request.user,
            post=post,
            text=text
        )

        return JsonResponse({'status': 'comment added'})
@csrf_exempt
@login_required
def like_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')

        post = Post.objects.get(id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
@csrf_exempt
@login_required
def follow_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')

        target_user = User.objects.get(id=user_id)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            follow.delete()
            following = False
        else:
            following = True

        return JsonResponse({'following': following})
from django.shortcuts import render

def feed(request):
    return render(request, 'Front/feed.html')

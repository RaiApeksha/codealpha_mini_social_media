from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import json
from .models import Post, Comment, Follow,Like
from .models import Profile

# FEED
@login_required
def feed(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        Post.objects.create(
            user=request.user,
            content=content,
            image=image,
            video=video
        )

        return redirect('feed')

    # Get all posts
    posts = Post.objects.select_related('user').prefetch_related('comments__user').order_by('-created_at')

    # Get a list of user IDs that the logged-in user is following
    following_ids = list(
        Follow.objects.filter(follower=request.user).values_list('following__id', flat=True)
    )

    return render(request, 'social_media/feed.html', {
        'posts': posts,
        'following_ids': following_ids
    })

# PROFILE
@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')

    followers_count = Follow.objects.filter(following=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=user_profile
    ).exists()

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }

    return render(request, 'social_media/profile.html', context)

# FOLLOWERS LIST
@login_required
def followers_list(request, username):
    user_profile = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user_profile)

    return render(request, 'social_media/follow_list.html', {
        'title': 'Followers',
        'users': [f.follower for f in followers],
    })



# FOLLOWING LIST
@login_required
def following_list(request, username):
    user_profile = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user_profile)

    return render(request, 'social_media/follow_list.html', {
        'title': 'Following',
        'users': [f.following for f in following],
    })


# CREATE POST
@csrf_exempt
@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        Post.objects.create(
            user=request.user,
            content=content,
            image=image,
            video=video
        )

        return redirect('feed')

#LIST POST
@login_required
def list_posts(request):
    posts = Post.objects.select_related('user').prefetch_related('comments__user', 'likes') \
        .order_by('-created_at')

    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'user': post.user.username,
            'content': post.content,
            'likes': post.likes.count(),
            'comments': [
                {
                    'user': c.user.username,
                    'text': c.text
                } for c in post.comments.all()
            ],
            'image': post.image.url if post.image else '',
            'video': post.video.url if post.video else '',
        })

    return JsonResponse({'posts': data})


# LIKE POST
@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(user=request.user, post=post).first()

    if like:
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    return JsonResponse({
        'likes': Like.objects.filter(post=post).count()
    })


#COMMENT
@csrf_exempt
@login_required
def add_comment(request, post_id):
    print("COMMENT VIEW HIT")  # 👈 IMPORTANT
    post = get_object_or_404(Post, id=post_id)

    data = json.loads(request.body)
    Comment.objects.create(
        user=request.user,
        post=post,
        text=data.get('text')
    )
    return JsonResponse({'status': 'ok'})


# FOLLOW / UNFOLLOW
@login_required
def follow_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        target_user = get_object_or_404(User, id=user_id)

        if target_user != request.user:
            follow_relation = Follow.objects.filter(
                follower=request.user, following=target_user
            ).first()

            if follow_relation:
                # Already following → unfollow
                follow_relation.delete()
            else:
                # Not following → create follow
                Follow.objects.create(follower=request.user, following=target_user)

    return redirect(request.META.get('HTTP_REFERER', 'feed'))

# REGISTER
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# LOGIN
def user_login(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')

        return render(request, 'registration/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'registration/login.html')


# LOGOUT
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

#UPLOAD PROFILE PICTURE
@login_required
def upload_avatar(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.avatar = request.FILES["avatar"]
        profile.save()

    return redirect("profile", username=request.user.username)

#FOLLOW USER
@login_required
def follow_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        target_user = get_object_or_404(User, id=user_id)

        if target_user != request.user:
            # Check if already following
            follow_instance = Follow.objects.filter(
                follower=request.user,
                following=target_user
            )
            if follow_instance.exists():
                # Already following → unfollow
                follow_instance.delete()
            else:
                # Not following → create follow
                Follow.objects.create(
                    follower=request.user,
                    following=target_user
                )

    return redirect("feed")
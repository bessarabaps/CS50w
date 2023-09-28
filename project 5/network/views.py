from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import  JsonResponse

from .models import User, Post, Follow


def index(request):
    current_user = request.user

    p = Paginator(Post.objects.all().order_by('-date'), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    # list of favorites posts
    userLike = []

    for pst in posts:
       if current_user in pst.likePost.all():
        userLike.append(pst)

    return render(request, "network/index.html", {
        'posts': posts,
        'userLike': userLike
    })


def profile(request, username):
    user = User.objects.get(username=username)
    current_user = request.user

    p = Paginator(Post.objects.filter(autor=user).order_by('-date'), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    # check if user has already followed
    followers = Follow.objects.filter(followed=user)
    following = Follow.objects.filter(follower=user)

    try:
        if len(followers.filter(follower=current_user)) !=0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    # list of favorites posts
    userLike = []

    for pst in posts:
        if current_user in pst.likePost.all():
            userLike.append(pst)

    return render(request, "network/profile.html", {
        'posts': posts,
        'username': username,
        'followers': followers,
        'following': following,
        'is_following': is_following,
        'userLike': userLike
    })


def following(request):
    current_user = request.user
    followingUsers = Follow.objects.filter(follower=current_user)
    allPosts = Post.objects.all().order_by('-date')

    # list of following posts
    followingPosts = []

    for post in allPosts:
        for user in followingUsers:
            if post.autor == user.followed:
                followingPosts.append(post)

    p = Paginator(followingPosts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    # list of favorites posts
    userLike = []

    for pst in posts:
        if current_user in pst.likePost.all():
            userLike.append(pst)

    return render(request, "network/following.html", {
        'posts': posts,
        'userLike': userLike
    })


def follow(request):
    if request.method == "POST":
        follower = request.user
        userfollowed = request.POST['userfollowed']
        followed = User.objects.get(username=userfollowed)
        follow = Follow.objects.create(follower=follower,followed=followed)
        return HttpResponseRedirect(reverse(profile, kwargs={'username': userfollowed}))
    else:
        return HttpResponseRedirect(reverse(profile, kwargs={'username': userfollowed}))


def unfollow(request):
    if request.method == "POST":
        follower = request.user
        userfollowed = request.POST['userfollowed']
        followed = User.objects.get(username=userfollowed)
        follow = Follow.objects.filter(follower=follower,followed=followed).delete()
        return HttpResponseRedirect(reverse(profile, kwargs={'username': userfollowed}))
    else:
        return HttpResponseRedirect(reverse(profile, kwargs={'username': userfollowed}))


def edit(request, post_id):
    if request.method == "POST":
        edit_post=Post.objects.get(pk=post_id)
        data=json.loads(request.body)

        new_text = data["bodyPost"]
        edit_post.bodyPost = new_text
        edit_post.save()

        return JsonResponse({'message': "Change successful", 'data': new_text})


def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    current_user = request.user

    if current_user in post.likePost.all():
        post.likePost.remove(current_user)
        return JsonResponse({"message": "Post unliked", "numLikes": post.likePost.count()})
    else:
        post.likePost.add(current_user)
        return JsonResponse({"message": "Post liked","numLikes": post.likePost.count()})


def newPost(request):
    if request.method == "POST":
        bodyPost = request.POST['bodyPost']
        autor = request.user

        newPost = Post.objects.create(autor=autor,bodyPost=bodyPost)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/newPost.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

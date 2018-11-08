from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages


def forum(request):
    posts = Posts.objects.all()
    comments = Comment.get_comment()

    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.poster = current_user
            comment.save()
        return redirect('forum')

    else:
        form = CommentForm()

    return render(request, "forum/forum.html", {"posts": posts, "comments": comments, "form": form})


def add_comment(request):
    # post = get_object_or_404(Posts)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.poster = current_user
            comment.save()
            return redirect('forum')
    else:
        form = CommentForm()
        return render(request, 'forum/comment.html', {"form": form})


def create_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = current_user
            post.save()
            messages.success(
                request, 'You have succesfully created a Post')
            return redirect('forum')
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {"form": form})
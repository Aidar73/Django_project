from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from posts.forms import PostForm
from posts.models import Post, Group, User


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        "group.html",
        {'page': page, 'paginator': paginator, "group": group}
    )


def new_post(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post', username=post.author.username, post_id=post.id)
        return render(request, "new_post.html", {"form": form})
    form = PostForm()
    return render(request, "new_post.html", {"form": form})


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.filter(author=author.pk)
    count = post_list.count()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'profile.html',
        {'count': count, 'page': page, 'paginator': paginator, 'author': author}
    )


def post_view(request, username, post_id):
    author = User.objects.get(username=username)
    count = author.posts.all().count()
    post = get_object_or_404(Post, author=author, pk=post_id)
    return render(
        request,
        'post.html',
        {'author': author, 'count': count, 'post': post}
    )


def post_edit(request, username, post_id):
    author = User.objects.get(username=username)
    post = get_object_or_404(Post, author=author, pk=post_id)
    if request.method == 'GET':
        if request.user != post.author:
            return redirect('post', username=username, post_id=post.id)
        form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect('post', username=username, post_id=post.id)
    return render(request, 'new_post.html', {'form': form, 'post': post})
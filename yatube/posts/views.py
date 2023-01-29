from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from posts.forms import PostForm, CommentForm
from posts.models import Post, Group, User, Follow


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


@login_required
def new_post(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
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
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    following = Follow.objects.filter(author=author)
    context = {
        'page': page,
        'paginator': paginator,
        'author': author,
        'following': following,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    author = User.objects.get(username=username)
    post = get_object_or_404(Post, author=author, pk=post_id)
    items = post.comments.all()
    form = CommentForm()
    following = Follow.objects.filter(author=author)
    return render(
        request,
        'post.html',
        {
            'author': author,
            'post': post,
            'items': items,
            'form': form,
            'following': following,
        }
    )


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=author, pk=post_id)
    if request.method == 'GET':
        if request.user != post.author:
            return redirect('post', username=username, post_id=post.id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username=request.user.username, post_id=post.id)
    return render(request, 'new_post.html', {'form': form, 'post': post})


@login_required
def add_comment(request, username, post_id):
    if not request.user.is_authenticated:
        return redirect('index')
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=author, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post', username=post.author.username, post_id=post.id)
        return render(request, "comments.html", {"form": form})
    form = CommentForm()
    return render(request, "comments.html", {"form": form})


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    authors = Follow.objects.filter(user=request.user)
    post_list = Post.objects.order_by('-pub_date').filter(author__following__in=authors)
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'follow.html',
        {'page': page, 'paginator': paginator}
    )

@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    if not Follow.objects.filter(user=request.user, author=author) and author != request.user:
        Follow.objects.create(user=request.user, author=author).save()
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)
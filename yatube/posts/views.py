from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from posts.forms import PostForm
from posts.models import Post, Group


def index(request):
# одна строка вместо тысячи слов на SQL
    latest = Post.objects.order_by('-pub_date')[:11]
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts})

def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, "new_post.html", {"form": form})
    else:
        form = PostForm()
    return render(request, "new_post.html", {"form": form})
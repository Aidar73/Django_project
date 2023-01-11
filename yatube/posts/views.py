from django.http import HttpResponse
from django.shortcuts import render

from posts.models import Post


def index(request):
# одна строка вместо тысячи слов на SQL
    latest = Post.objects.order_by('-pub_date')[:11]
    return render(request, "index.html", {"posts": latest})
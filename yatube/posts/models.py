from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    # свойство text типа TextField
    text = models.TextField()

    # свойство pub_date типа DateTimeField, текст "date published" это заголовок
    # поля в интерфейсе администратора. auto_now_add говорит, что при создании
    # новой записи автоматически будет подставлено текущее время и дата
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    # свойство author типа ForeignKey, ссылка на модель User
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
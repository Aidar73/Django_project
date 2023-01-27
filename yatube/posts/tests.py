from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from .models import *


class ProfileTest(TestCase):
    def setUp(self):
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client = Client()
        # создаём пользователя
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345"
        )
        # создаём пост от имени пользователя
        self.post = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user)
        self.client.login(username="sarah", password="12345")
        self.username = self.post.author.username
        self.post_id = self.post.pk

    def test_profile(self):
        # формируем GET-запрос к странице сайта
        response = self.client.get("/sarah/")
        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)
        # проверяем, что при отрисовке страницы был получен список из 1 записи
        self.assertEqual(len(response.context["page"]), 1)
        # проверяем, что объект пользователя, переданный в шаблон,
        # соответствует пользователю, которого мы создали
        self.assertIsInstance(response.context["page"][0].author, User)
        self.assertEqual(response.context["page"][0].author.username, self.user.username)

    def test_view_new_post(self):
        # после публикации поста новая запись появляется на главной странице сайта (index),
        # на персональной странице пользователя (profile), и на отдельной странице поста (post)
        response = self.client.get(f"/{self.username}/{self.post_id}/")
        response_index = self.client.get('/')
        response_profile = self.client.get(f"/{self.username}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)
        self.assertIn(self.post, response_index.context['page'])
        self.assertIn(self.post, response_profile.context['page'])

    def test_post_edit(self):
        # авторизованный пользователь может отредактировать свой пост
        response = self.client.post(f"/{self.username}/{self.post_id}/edit/", {'text': 'Hello_test'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.post = Post.objects.get(id=self.post_id)
        self.assertEqual(self.post.text, 'Hello_test')
        # и его содержимое изменится на всех связанных страницах
        response = self.client.get(f"/{self.username}/{self.post_id}/")
        response_index = self.client.get('/')
        response_profile = self.client.get(f"/{self.username}/")
        self.assertEqual(response.context['post'], self.post)
        self.assertIn(self.post, response_index.context['page'])
        self.assertIn(self.post, response_profile.context['page'])

    def test_image(self):
        with open('posts/img.jpg', 'rb') as img:
            # self.client.login(username="sarah", password="12345")
            post = self.client.post(
                f"/{self.username}/{self.post_id}/edit/",
                {'author': self.user, 'text': 'post with image', 'image': img}
            )
            response = self.client.get(f"/{self.username}/{self.post_id}/")
            response_index = self.client.get('/')
            response_profile = self.client.get(f"/{self.username}/")
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<img')
            self.assertContains(response_index, '<img')
            self.assertContains(response_profile, '<img')


    def test_create_post_not_user(self):
        # проверяем что неавторизованный посетитель не может опубликовать пост
        self.client.logout()
        response = self.client.post('/new/', {'text': 'Hello'})
        self.assertEqual(response.context, None)
        # (его редиректит на страницу входа)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class PageNotFoundTest(TestCase):
    def test_404(self):
        self.client = Client()
        response = self.client.get('afasd')
        self.assertEqual(response.status_code, 404)
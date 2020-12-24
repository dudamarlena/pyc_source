# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/blog/api/tests/test_apis.py
# Compiled at: 2019-08-05 02:16:42
# Size of source mod 2**32: 6715 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from blog.models import Post
User = get_user_model()

class BlogApiTestCase(APITestCase):

    def setUp(self):
        user_obj = User(username='test', email='test@gmail.com')
        user_obj.set_password('123456789')
        user_obj.save()
        self.client.login(username='test', password='123456789')
        Post.objects.create(author=user_obj,
          title='some title',
          body='some body')
        Post.objects.create(author=user_obj,
          title='some other title',
          body='some other body')
        Post.objects.create(author=user_obj,
          title='some other other title',
          body='some other other body')

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = Post.objects.count()
        self.assertEqual(post_count, 3)

    def test_get_list(self):
        data = {}
        url = api_reverse('post_list')
        response = self.client.get(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_rud_list(self):
        data = {'author':'test', 
         'title':'some title', 
         'body':'test creating item'}
        url = api_reverse('post_rud', kwargs={'pk': 1})
        response = self.client.get(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_create_item(self):
        data = {'author':'test', 
         'title':'some title', 
         'body':'test creating item'}
        url = api_reverse('post_create')
        response = self.client.post(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_update_item(self):
        data = {'author':'test', 
         'title':'updated test', 
         'body':'test creating item'}
        url = api_reverse('post_create')
        response = self.client.put(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_item_in_create_view(self):
        data = {'author':'test', 
         'title':'updated test', 
         'body':'test creating item'}
        url = api_reverse('post_create')
        response = self.client.patch(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_item_in_delete_view(self):
        data = {'title':'updated test', 
         'body':'test creating item'}
        url = api_reverse('post_delete', kwargs={'pk': 2})
        response = self.client.get(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_in_retrive_update_view(self):
        data = {}
        url = api_reverse('post_update', kwargs={'pk': 1})
        response = self.client.get(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_method_not_allowed(self):
        data = {'title':'updated test', 
         'body':'test creating item'}
        url = api_reverse('post_create')
        response = self.client.patch(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_item(self):
        blog_post = Post.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, formart='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
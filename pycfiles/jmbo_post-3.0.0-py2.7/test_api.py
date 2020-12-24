# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/post/tests/test_api.py
# Compiled at: 2017-07-03 11:37:50
import os, unittest, json
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from post.models import Post

class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.editor = get_user_model().objects.create(username='editor-api', email='editor-api@test.com', is_superuser=True, is_staff=True)
        cls.editor.set_password('password')
        cls.editor.save()
        cls.client.logout()
        obj, dc = Post.objects.get_or_create(title='Post', markdown='aaaa\n***\nbbb', state='published')
        obj.sites = [
         1]
        obj.save()
        cls.post = obj

    def setUp(self):
        self.client.logout()

    def test_post_detail(self):
        response = self.client.get('/api/v1/post-post-permitted/%s/' % self.post.pk)
        as_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.failUnless('content' in as_json)
        self.failUnless('content_pages' in as_json)
        self.failUnless('/post-post-permitted/' in as_json['url'])
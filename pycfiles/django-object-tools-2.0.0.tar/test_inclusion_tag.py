# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-object-tools/object_tools/tests/test_inclusion_tag.py
# Compiled at: 2018-12-21 02:57:07
from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase, RequestFactory

class ObjectToolsInclusionTagsTestCase(TestCase):
    """
    Testcase for object_tools.templatetags.object_tools_inclusion_tags.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user')

    def test_object_tools(self):
        request = self.factory.get('/')
        request.user = self.user
        context = Context({'model': User, 
           'request': request})
        t = Template('{% load object_tools_inclusion_tags %}{% object_tools                 model request.user %}')
        result = t.render(context)
        expected_result = '\n'
        self.assertEqual(result, expected_result)
        user = User()
        user.save()
        context['request'].user = user
        result = t.render(context)
        expected_result = '\n'
        self.assertEqual(result, expected_result)
        user.is_superuser = True
        user.save()
        result = t.render(context)
        expected_result = '\n<li><a href="/object-tools/auth/user/test_tool/?" title=""class="historylink">Test Tool</a></li>\n\n<li><a href="/object-tools/auth/user/test_media_tool/?" title=""class="historylink">Test Media Tool</a></li>\n\n'
        self.assertEqual(result, expected_result)

    def tearDown(self):
        self.user.delete()
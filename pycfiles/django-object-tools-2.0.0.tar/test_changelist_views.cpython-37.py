# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-object-tools/object_tools/tests/test_changelist_views.py
# Compiled at: 2018-12-21 02:57:07
# Size of source mod 2**32: 759 bytes
from django.contrib.auth.models import User
from django.test import TestCase

class ChangeListViewTestCase(TestCase):
    __doc__ = "\n    TestCase for testing if tool is display in a model's changelist view.\n    "

    def setUp(self):
        self.user = User.objects.create_superuser(username='testuser', password='password', email='testuser@example.com')
        self.client.login(username='testuser', password='password')

    def test_tool_is_rendered(self):
        response = self.client.get('/admin/auth/user/')
        tool_html = '<li><a href="/object-tools/auth/user/test_tool/?" title=""class="historylink">Test Tool</a></li>'
        self.assertContains(response, tool_html)
        self.assertEqual(response.status_code, 200)
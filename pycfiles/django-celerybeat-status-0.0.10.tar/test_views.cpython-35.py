# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/workspaces/workspace_django/django-celerybeat-status/celerybeat_status/tests/test_views.py
# Compiled at: 2018-02-15 23:49:31
# Size of source mod 2**32: 551 bytes
from django.utils import version as django_version
from celerybeat_status.tests.utils import SuperuserBaseTestCase, TestRequiresSuperuser
if django_version.get_complete_version() < (2, 0, 0):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse

class PeriodicTaskStatusListTests(TestRequiresSuperuser, SuperuserBaseTestCase):
    view_name = 'periodic-tasks-status'

    def setUp(self):
        super(PeriodicTaskStatusListTests, self).setUp()
        self.view_url = reverse(self.view_name)
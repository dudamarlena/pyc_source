# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/tests/test_tasks.py
# Compiled at: 2018-11-05 09:06:44
from django.test import TestCase

class TasksTestCase(TestCase):

    def test_import(self):
        from ultracache import tasks
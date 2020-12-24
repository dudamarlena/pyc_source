# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-search/ovp_search/tests/test_execution.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 245 bytes
import ovp_search.apps
from django.test import TestCase
from django.core.management import call_command

class RebuildIndexTestCase(TestCase):

    def test_rebuild_index_execution(self):
        call_command('rebuild_index', '--noinput', verbosity=0)
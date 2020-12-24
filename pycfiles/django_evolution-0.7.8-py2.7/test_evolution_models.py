# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/tests/test_evolution_models.py
# Compiled at: 2018-06-14 23:17:51
from datetime import datetime
from django.test.testcases import TestCase
from django_evolution.models import Version

class VersionManagerTests(TestCase):
    """Unit tests for django_evolution.models.VersionManager."""

    def test_current_version_with_dup_timestamps(self):
        """Testing Version.current_version() with two entries with same timestamps"""
        Version.objects.all().delete()
        timestamp = datetime(year=2015, month=12, day=10, hour=12, minute=13, second=14)
        Version.objects.create(signature='abc123', when=timestamp)
        version = Version.objects.create(signature='abc123-def456', when=timestamp)
        latest_version = Version.objects.current_version()
        self.assertEqual(latest_version, version)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/log/tests/test_cursor_debug_wrapper.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from importlib import import_module
from django.db import connection
from djblets.testing.testcases import TestCase
import_module(b'djblets.log.middleware')

class CursorDebugWrapperTests(TestCase):
    """Unit tests for djblets.log.middleware.CursorDebugWrapper."""

    def test_execute(self):
        """Testing CursorDebugWrapper.execute"""
        with self.assertNumQueries(1):
            connection.cursor().execute(b'INSERT INTO django_site (name, domain) VALUES (%s, %s)', ('site1',
                                                                                                    'domain1.com'))
        self.assertIn(b'stack', self._get_queries()[(-1)])

    def test_executemany(self):
        """Testing CursorDebugWrapper.executemany"""
        with self.assertNumQueries(1):
            connection.cursor().executemany(b'INSERT INTO django_site (name, domain) VALUES (%s, %s)', [
             ('site1', 'domain1.com'),
             ('site2', 'domain2.com')])
        self.assertIn(b'stack', self._get_queries()[(-1)])

    def _get_queries(self):
        try:
            return connection.queries_log
        except AttributeError:
            return connection.queries
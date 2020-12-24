# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/__init__.py
# Compiled at: 2011-11-29 15:47:41
"""Test suite for the repoze.what Quickstart plugin."""
import os
_here = os.path.abspath(os.path.dirname(__file__))
FIXTURE_DIR = os.path.join(_here, 'fixture')

def tearDown():
    """Remove temporary files."""
    os.remove(os.path.join(FIXTURE_DIR, 'file.log'))


class MockApplication(object):
    """Fake WSGI application."""

    def __init__(self, status=None, headers=None):
        self.status = status
        self.headers = headers

    def __call__(self, environ, start_response):
        self.environ = environ
        start_response(self.status, self.headers)
        return ['response body']
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/urllib3/urllib3/contrib/_appengine_environ.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 909 bytes
"""
This module provides means to detect the App Engine environment.
"""
import os

def is_appengine():
    return 'APPENGINE_RUNTIME' in os.environ


def is_appengine_sandbox():
    """Reports if the app is running in the first generation sandbox.

    The second generation runtimes are technically still in a sandbox, but it
    is much less restrictive, so generally you shouldn't need to check for it.
    see https://cloud.google.com/appengine/docs/standard/runtimes
    """
    return is_appengine() and os.environ['APPENGINE_RUNTIME'] == 'python27'


def is_local_appengine():
    return is_appengine() and os.environ.get('SERVER_SOFTWARE', '').startswith('Development/')


def is_prod_appengine():
    return is_appengine() and os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine/')


def is_prod_appengine_mvms():
    """Deprecated."""
    return False
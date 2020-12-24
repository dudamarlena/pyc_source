# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/contrib/_appengine_environ.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 717 bytes
"""
This module provides means to detect the App Engine environment.
"""
import os

def is_appengine():
    return is_local_appengine() or is_prod_appengine() or is_prod_appengine_mvms()


def is_appengine_sandbox():
    return is_appengine() and not is_prod_appengine_mvms()


def is_local_appengine():
    return 'APPENGINE_RUNTIME' in os.environ and 'Development/' in os.environ['SERVER_SOFTWARE']


def is_prod_appengine():
    return 'APPENGINE_RUNTIME' in os.environ and 'Google App Engine/' in os.environ['SERVER_SOFTWARE'] and not is_prod_appengine_mvms()


def is_prod_appengine_mvms():
    return os.environ.get('GAE_VM', False) == 'true'
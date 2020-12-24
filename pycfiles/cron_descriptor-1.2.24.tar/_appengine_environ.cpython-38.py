# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/urllib3/contrib/_appengine_environ.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 707 bytes
__doc__ = '\nThis module provides means to detect the App Engine environment.\n'
import os

def is_appengine():
    return is_local_appengine() or 


def is_appengine_sandbox():
    return is_appengine() and not is_prod_appengine_mvms()


def is_local_appengine():
    return 'APPENGINE_RUNTIME' in os.environ and 'Development/' in os.environ['SERVER_SOFTWARE']


def is_prod_appengine():
    return 'APPENGINE_RUNTIME' in os.environ and 'Google App Engine/' in os.environ['SERVER_SOFTWARE'] and not is_prod_appengine_mvms()


def is_prod_appengine_mvms():
    return os.environ.get('GAE_VM', False) == 'true'
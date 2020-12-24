# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/uwsgi.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import os

def reload_on_change(path):
    """
    Set up uwsgi file monitoring hooks for reloading on change
    """
    if 'UWSGI_PY_AUTORELOAD' not in os.environ:
        return
    try:
        import uwsgi
        from uwsgidecorators import filemon as filemon_
    except ImportError:
        return

    filemon_(path)(uwsgi.reload)
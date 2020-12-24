# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/compat.py
# Compiled at: 2016-09-30 08:46:30
"""
The `compat` module provides support for backwards compatibility with older
versions of Django/Python, and compatibility wrappers around optional packages.
"""
try:
    import importlib
except ImportError:
    from django.utils import importlib

try:
    import goslate
except ImportError:
    goslate = None
except SyntaxError:
    import sys, warnings
    warnings.warn('goslate disabled due lack support of Python-%s' % sys.version.split()[0][:3], RuntimeWarning)
    goslate = None

try:
    import googleapiclient
except ImportError:
    googleapiclient = None
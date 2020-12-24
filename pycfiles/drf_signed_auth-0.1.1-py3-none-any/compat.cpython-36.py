# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcgibbons/projects/drf_signed_auth/drf_signed_auth/compat.py
# Compiled at: 2017-10-08 11:15:44
# Size of source mod 2**32: 287 bytes
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

try:
    from unittest import mock
except ImportError:
    import mock

try:
    from importlib import reload
except ImportError:
    reload = reload
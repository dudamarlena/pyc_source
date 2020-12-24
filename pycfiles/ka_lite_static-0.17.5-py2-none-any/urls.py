# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/utils/urls.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
from django.conf import settings
from django.utils import six
_trailing_slash = b'/?' if getattr(settings, b'TASTYPIE_ALLOW_MISSING_SLASH', False) else b'/'

class CallableUnicode(six.text_type):

    def __call__(self):
        return self


trailing_slash = CallableUnicode(_trailing_slash)
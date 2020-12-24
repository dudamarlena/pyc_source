# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_select2/conf.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 2777 bytes
"""Settings for Django-Select2."""
from __future__ import absolute_import, unicode_literals
from appconf import AppConf
from django.conf import settings
__all__ = ('settings', 'Select2Conf')

class Select2Conf(AppConf):
    __doc__ = 'Settings for Django-Select2.'
    CACHE_BACKEND = 'default'
    CACHE_PREFIX = 'select2_'
    JS = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js'
    CSS = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css'

    class Meta:
        __doc__ = 'Prefix for all Django-Select2 settings.'
        prefix = 'SELECT2'
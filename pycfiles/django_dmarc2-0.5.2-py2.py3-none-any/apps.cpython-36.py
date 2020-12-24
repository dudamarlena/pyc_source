# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bas/dev/django-dmarc/dmarc/apps.py
# Compiled at: 2018-06-18 16:39:43
# Size of source mod 2**32: 490 bytes
"""Django application configuration"""
from __future__ import unicode_literals
from django.apps import AppConfig

class DmarcConfig(AppConfig):
    __doc__ = 'DMARC application configuration'
    name = 'dmarc'
    verbose_name = 'DMARC feedback report manager'
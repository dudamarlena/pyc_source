# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DJANGO-WORKON/workon/contrib/cleaner/signals.py
# Compiled at: 2017-11-30 05:22:17
# Size of source mod 2**32: 197 bytes
"""
    django-cleanup sends the following signals
"""
from django.dispatch import Signal
cleanup_pre_delete = Signal(providing_args=['file'])
cleanup_post_delete = Signal(providing_args=['file'])
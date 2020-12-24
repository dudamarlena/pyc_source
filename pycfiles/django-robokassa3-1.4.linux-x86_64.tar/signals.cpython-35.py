# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mikhail/.virtualenvs/django-robokassa/lib/python3.5/site-packages/robokassa/signals.py
# Compiled at: 2018-04-26 07:06:46
# Size of source mod 2**32: 284 bytes
from __future__ import unicode_literals
from django.dispatch import Signal
result_received = Signal(providing_args=['InvId', 'OutSum'])
success_page_visited = Signal(providing_args=['InvId', 'OutSum'])
fail_page_visited = Signal(providing_args=['InvId', 'OutSum'])
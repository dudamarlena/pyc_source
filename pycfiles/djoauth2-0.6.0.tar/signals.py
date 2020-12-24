# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/signals.py
# Compiled at: 2013-11-22 18:12:08
from django.dispatch import Signal
refresh_token_used_after_invalidation = Signal(providing_args=[
 'access_token', 'request'])
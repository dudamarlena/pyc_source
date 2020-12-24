# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insight/signals.py
# Compiled at: 2014-09-10 07:58:57
from django.dispatch import Signal
origin_hit = Signal(providing_args=['instance', 'request'])
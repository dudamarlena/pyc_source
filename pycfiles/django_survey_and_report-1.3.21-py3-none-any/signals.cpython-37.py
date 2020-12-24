# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/signals.py
# Compiled at: 2019-03-01 16:36:34
# Size of source mod 2**32: 128 bytes
import django.dispatch
survey_completed = django.dispatch.Signal(providing_args=['instance', 'data'])
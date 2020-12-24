# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-m2m-history/m2m_history/signals.py
# Compiled at: 2016-02-26 15:02:26
from django.dispatch import Signal
m2m_history_changed = Signal(providing_args=['action', 'instance', 'reverse', 'model', 'pk_set', 'using',
 'field_name', 'time'])
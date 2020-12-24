# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kajic/projects/django-counter-field/django_counter_field/__init__.py
# Compiled at: 2013-12-26 09:07:41
from django_model_changes.changes import ChangesMixin as CounterMixin
from .counter import connect_counter
from .fields import CounterField
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danila/Work/tmp/django_counter_field_py3/django_counter_field_py3/__init__.py
# Compiled at: 2018-01-17 12:33:04
# Size of source mod 2**32: 203 bytes
from django_model_changes.changes import ChangesMixin as CounterMixin
from .counter import connect_counter
from .fields import CounterField
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danila/Work/tmp/django-counter-field-py3/django_counter_field_py3/fields.py
# Compiled at: 2018-01-17 11:16:21
# Size of source mod 2**32: 602 bytes
from django.db import models

class CounterField(models.IntegerField):
    __doc__ = '\n    CounterField wraps the standard django IntegerField. It exists primarily to allow for easy validation of\n    counter fields. The default value of a counter field is 0.\n    '

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 0)
        (super(CounterField, self).__init__)(*args, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ['^django_counter_field_py3\\.fields\\.CounterField'])
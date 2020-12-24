# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kajic/projects/django-counter-field/django_counter_field/fields.py
# Compiled at: 2013-12-26 09:06:08
from django.db import models

class CounterField(models.IntegerField):
    """
    CounterField wraps the standard django IntegerField. It exists primarily to allow for easy validation of
    counter fields. The default value of a counter field is 0.
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 0)
        super(CounterField, self).__init__(*args, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ['^django_counter_field\\.fields\\.CounterField'])
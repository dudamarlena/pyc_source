# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/fields.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 1183 bytes
"""Custom model fields."""
import json
from django.db import models

class JSONField(models.TextField):
    __doc__ = "Add's JSON capablilties (retrieval) to Django's TextField."

    def get_prep_value(self, value):
        db_value = super(JSONField, self).get_prep_value(value)
        return json.dumps(db_value)

    def from_db_value(self, value, expression, connection, *args, **kwargs):
        """Convert the JSON back to a dictionary."""
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def to_python(self, value):
        """Simply returns the dictionary"""
        return value


class ListField(models.CharField):
    __doc__ = 'Emulate django.contrib.postgres ArrayField.'

    def get_prep_value(self, value):
        super(ListField, self).get_prep_value(value)
        return ','.join(value)

    def from_db_value(self, value, expression, connection, *args, **kwargs):
        """Return the value from the database as a python list."""
        return value.split(',')
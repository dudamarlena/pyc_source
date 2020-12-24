# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sdehaan/Documents/Repositories/unicore-gitmodels/unicore_gitmodels/fields.py
# Compiled at: 2014-10-06 05:19:57
import json
from gitmodel.fields import Field
from gitmodel.exceptions import ValidationError

class ListField(Field):
    """
    A list of things to store in JSON.
    As a result, everything in the list must be JSON serialisable.
    """
    empty_value = []

    def to_python(self, value):
        if value is None:
            return
        else:
            if isinstance(value, list):
                return value
            try:
                return json.loads(value)
            except ValueError as e:
                raise ValidationError(e)

            return
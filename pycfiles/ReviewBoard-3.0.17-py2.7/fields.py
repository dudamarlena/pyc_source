# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/fields.py
# Compiled at: 2020-02-11 04:03:56
"""Custom search index fields."""
from __future__ import unicode_literals
from haystack import indexes

class BooleanField(indexes.BooleanField):
    """A custom BooleanField.

    This works around `an issue in django-haystack
    <https://github.com/django-haystack/django-haystack/issues/801>`_ that
    results in BooleanFields always returning ``True``.
    """
    value_map = {b'true': True, 
       b'false': False}

    def convert(self, value):
        """Convert value to a boolean value.

        Args:
            value (unicode):
                The value to convert

        Returns:
            bool:
            The boolean representation of ``value``.
        """
        if value is None:
            return
        else:
            try:
                return self.value_map[value]
            except KeyError:
                return bool(value)

            return
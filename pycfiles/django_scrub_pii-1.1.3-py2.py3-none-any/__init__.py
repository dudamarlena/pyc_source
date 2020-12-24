# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Nomensa/django-scrub-pii/scrubpii/__init__.py
# Compiled at: 2016-01-28 08:43:21
from .utils import get_sensitive_fields
import django.db.models.options as options

class allow_sensitive_fields(object):
    """Patches the Django Options class to allow for setting sensitive_fields."""

    def __enter__(self):
        self.original_names = options.DEFAULT_NAMES
        if 'sensitive_fields' in options.DEFAULT_NAMES:
            raise ValueError('sensitive_fields is already defined in Django!')
        options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('sensitive_fields', )

    def __exit__(self, type, value, traceback):
        options.DEFAULT_NAMES = self.original_names
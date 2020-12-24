# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/siyuan/projects/django-simplemde/testproject/simplemde/utils.py
# Compiled at: 2018-01-17 09:49:38
# Size of source mod 2**32: 552 bytes
from django.core.exceptions import ImproperlyConfigured
from importlib import import_module
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from django.utils.functional import Promise
import json

class LazyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        else:
            return super(LazyEncoder, self).default(obj)


def json_dumps(data):
    return json.dumps(data, cls=LazyEncoder)
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/helpers.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 527 bytes
from django.conf import settings
import importlib

def get_settings(string='OVP_USERS'):
    return getattr(settings, string, {})


def import_from_string(val):
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[(-1)]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except ImportError as e:
        msg = "Could not import '%s' for setting. %s: %s." % (val, e.__class__.__name__, e)
        raise ImportError(msg)
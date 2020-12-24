# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/decorators.py
# Compiled at: 2014-08-27 19:26:12
import sys
from django.contrib.auth.decorators import user_passes_test

def print_all_exceptions(function):

    def wrap(request, *args, **kwargs):
        try:
            ret = function(request, *args, **kwargs)
        except Exception as e:
            print sys.stderr.write(str(e))
            ret = str(e)

        return ret

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def _is_in_group(u, group_names):
    for g in group_names:
        if bool(u.groups.filter(name__in=g)) | u.is_superuser:
            return True

    return False


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in.

    Requires a list of strings representing the group names.
    """

    def in_groups(u):
        if u.is_authenticated():
            return _is_in_group(u, group_names)
        return False

    return user_passes_test(in_groups)
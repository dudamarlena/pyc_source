# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/utils/requests.py
# Compiled at: 2019-04-03 22:56:29
# Size of source mod 2**32: 929 bytes
from datetime import datetime
from urllib.parse import unquote
from .timezone import ensure_timezone

def getIntFromGet(request, key):
    """
    This function just parses the request GET data for the requested key,
    and returns it as an integer, returning none if the key is not
    available or is in incorrect format.
    """
    try:
        return int(request.GET.get(key))
    except (ValueError, TypeError):
        return


def getDateTimeFromGet(request, key):
    """
    This function just parses the request GET data for the requested key,
    and returns it in datetime format, returning none if the key is not
    available or is in incorrect format.
    """
    if request.GET.get(key, ''):
        try:
            return ensure_timezone(datetime.strptime(unquote(request.GET.get(key, '')), '%Y-%m-%d'))
        except (ValueError, TypeError):
            pass
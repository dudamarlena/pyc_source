# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /venv/smoothierecipes/src/django-google-analytics-reporter/google_analytics_reporter/utils.py
# Compiled at: 2016-09-28 18:10:59
# Size of source mod 2**32: 246 bytes
import uuid

def get_client_id(request):
    _ga = request.COOKIES.get('_ga')
    if _ga:
        ga_split = _ga.split('.')
        client_id = '.'.join((ga_split[2], ga_split[3]))
    else:
        client_id = uuid.uuid4()
    return client_id
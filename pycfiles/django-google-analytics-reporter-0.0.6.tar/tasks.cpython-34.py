# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /venv/smoothierecipes/src/django-google-analytics-reporter/google_analytics_reporter/tasks.py
# Compiled at: 2016-08-24 17:09:20
# Size of source mod 2**32: 436 bytes
import sys
from celery import shared_task
if sys.version_info > (3, 0):
    from http import client
    from urllib.parse import urlencode
else:
    import httplib as client
    from urllib import urlencode

@shared_task
def send_report_task(params_dict):
    params = urlencode(params_dict)
    connection = client.HTTPConnection('www.google-analytics.com')
    return connection.request('POST', '/collect', params)
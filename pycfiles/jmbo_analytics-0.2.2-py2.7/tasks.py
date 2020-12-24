# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_analytics/tasks.py
# Compiled at: 2016-09-02 05:17:18
import requests
from celery.task import task

@task(ignore_result=True)
def send_ga_tracking(params):
    utm_url = params.get('utm_url')
    user_agent = params.get('user_agent')
    language = params.get('language')
    headers = {'User-Agent': user_agent, 
       'Accept-Language': language}
    try:
        requests.get(utm_url, headers=headers)
    except requests.HTTPError:
        pass
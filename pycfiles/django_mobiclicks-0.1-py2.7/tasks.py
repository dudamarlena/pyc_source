# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mobiclicks/tasks.py
# Compiled at: 2013-11-20 06:54:07
import requests
from celery import task
from mobiclicks import conf

@task()
def confirm_click(click_ref):
    requests.get(conf.CLICK_CONFIRMATION_URL, params={'action': 'clickReceived', 'authKey': conf.CPA_SECURITY_TOKEN, 
       'clickRef': click_ref})


@task()
def track_registration_acquisition(cpa_token):
    requests.get(conf.ACQUISITION_TRACKING_URL, params={'cpakey': conf.CPA_SECURITY_TOKEN, 'code': cpa_token})
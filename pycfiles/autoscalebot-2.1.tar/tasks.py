# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Data/Users/steven.skoczen/.virtualenvs/project_tomo/src/heroku-web-autoscale/heroku_web_autoscale/tasks.py
# Compiled at: 2012-03-06 21:21:56
from time import sleep
from heroku_web_autoscale import MissingParameter
from heroku_web_autoscale.conf import AutoscaleSettings
from heroku_web_autoscale.models import HerokuAutoscaler

def start_autoscaler(settings=None, in_django=False):
    settings = AutoscaleSettings(settings=settings, in_django=in_django)
    autoscale = HerokuAutoscaler(settings)
    try:
        assert settings.HEARTBEAT_INTERVAL_IN_SECONDS is not None
    except:
        raise MissingParameter('HEARTBEAT_INTERVAL_IN_SECONDS not set.')

    while True:
        last_heartbeat_time_in_seconds = autoscale.full_heartbeat() / 1000
        next_interval = settings.HEARTBEAT_INTERVAL_IN_SECONDS - last_heartbeat_time_in_seconds
        if next_interval > 0:
            sleep(next_interval)

    return
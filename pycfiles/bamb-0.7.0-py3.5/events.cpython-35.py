# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest/events.py
# Compiled at: 2017-09-08 11:38:51
# Size of source mod 2**32: 1285 bytes
from domain import base
import urllib3
from common import constants
from domain import exceptions
from bamb import Bamb
from bamb import Config
from service import event_service
from celery.exceptions import Retry

class EventRedirect(base.Listener):

    def on_event(self, e, queue=''):
        user_id = queue[len(constants.QUEUE_PREFIX_FOR_BACKGROUND_EVENTS):]
        if len(user_id) == 0:
            raise exceptions.IllegalArgumentException('can not determine user id from queue name : ' + queue)
        conf = Bamb.singleton().conf
        if not isinstance(conf, Config):
            raise exceptions.AppException('app is not configured !')
        url = conf.SERVER_PATH + 'events/' + user_id
        params = str(e)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        http = urllib3.PoolManager()
        r = http.request('POST', url, params, headers)
        if r.status != 200:
            pass
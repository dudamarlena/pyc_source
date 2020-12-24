# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider_common/persistent/dw_logger.py
# Compiled at: 2019-04-10 02:28:52
# Size of source mod 2**32: 1441 bytes
import json, requests
from six.moves.urllib.parse import urlencode
from parser_engine.patch import get_redis
from parser_engine.singleton import Singleton

@Singleton
class DwLogger:

    def __init__(self, write_filename='dw_local.txt'):
        from scrapy.utils import project
        settings = project.get_project_settings()
        self.r = get_redis(**settings.getdict('REDIS_PARAMS'))
        self.ENV = settings.get('ENV')
        if write_filename:
            self.f = open(write_filename, 'a+')
        else:
            self.f = None

    def __del__(self):
        if self.f:
            self.f.close()

    def log_to_dw(self, action, **data):
        if self.ENV == 'local':
            if self.f:
                self.f.write(json.dumps(data) + '\n')
            return
        data['event_type'] = 'bxmainsite_aux'
        data['site_id'] = 'bx_crawler'
        data['tracktype'] = 'event'
        data['__debug'] = 1
        url = 'https://www.baixing.com/c/aux/' + action + '?' + urlencode(data)
        resp = requests.get(url)
        retry_times = 2
        while retry_times > 0 and resp.status_code != requests.codes.ok:
            resp = requests.get(url)
            retry_times -= 1

        if resp.status_code != requests.codes.ok:
            self.r.set('faillog:dw:' + action, json.dumps(data))
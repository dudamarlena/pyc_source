# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/http.py
# Compiled at: 2019-12-12 20:40:28
# Size of source mod 2**32: 2886 bytes
import requests, random, time
from clocwalk.libs.core.data import logger
from clocwalk.libs.core.data import conf
from clocwalk.libs.core.common import parse_int
from clocwalk.libs.core.exception import HTTPStatusCodeError

class RequestConnect(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self.timeout = parse_int(kwargs.get('timeout'), conf.http['timeout'])
        timeout_try = parse_int(kwargs.get('timeout_try'), conf.http['tiemout_try'])
        self.session = requests.Session()
        self.session.headers.update(conf.http['headers'])
        self.timeout_try = 1
        if isinstance(timeout_try, int):
            if timeout_try > self.timeout_try:
                self.timeout_try = timeout_try

    def __send_data(self, url, data, method='POST'):
        """

        :param url:
        :param data:
        :param method:
        :return:
        """

        def get_delay_s():
            return round(random.random(), 2) * random.randrange(3, 9)

        result = None
        try_index = 1
        requests.packages.urllib3.disable_warnings()
        while True:
            try:
                if method == 'GET':
                    resp = self.session.get(url, data=data, timeout=(self.timeout), verify=False)
                else:
                    resp = self.session.post(url, json=data, timeout=(self.timeout), verify=False)
                logger.info('URL: {0}, Status:{1}'.format(url, resp.status_code))
                if resp.status_code == 200:
                    result = resp.content
                    break
                else:
                    if resp.status_code in (404, ):
                        result = ''
                        break
                    else:
                        logger.warning('status_code: {0}, reason: {1}'.format(resp.status_code, resp.reason))
                        raise HTTPStatusCodeError(resp.reason)
            except (requests.exceptions.Timeout, requests.exceptions.ProxyError, HTTPStatusCodeError) as ex:
                try:
                    logger.warn(ex)
                    time.sleep(get_delay_s())
                    if try_index >= self.timeout_try + 1:
                        break
                    else:
                        logger.warning('[-] Start {0} attempts to send data...'.format(try_index))
                        try_index += 1
                finally:
                    ex = None
                    del ex

        return result

    def post_data(self, url, data):
        """

        :param url:
        :param data:
        :return:
        """
        return self._RequestConnect__send_data(url=url, data=data, method='POST')

    def get_data(self, url, data=None):
        """

        :param url:
        :param data:
        :return:
        """
        return self._RequestConnect__send_data(url=url, data=data, method='GET')
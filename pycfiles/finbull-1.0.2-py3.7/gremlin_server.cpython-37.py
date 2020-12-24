# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/finbull/lib/gremlin_server.py
# Compiled at: 2019-08-01 22:03:49
# Size of source mod 2**32: 2269 bytes
"""
File: gremlin_server.py.py
Author: wangjiangfeng(wangjiangfeng@pku.edu.cn)
Date: 2019-07-31 20:01
"""
import random, requests, json, finbull.error

class GremlinServer(object):
    __doc__ = 'Summary\n\n    Attributes\n        ip_list (list or str): [IP:Port, IP:Port]\n        username (str): username\n        password (str): password\n    '

    def __init__(self, ip_list=None, **kwargs):
        """
        初始化函数
        :param ip_list:
        :param kwargs:
        """
        self.ip_list = ip_list
        self.client_kwargs = kwargs
        if self.ip_list is None:
            raise finbull.error.BaseError(errno=(finbull.error.ERRMSG_FRAMEWORK),
              errmsg='ip_list is empty both.')
        if not isinstance(self.ip_list, list):
            self.ip_list = [
             self.ip_list]
        self.username = kwargs['username'] if 'username' in kwargs else ''
        self.password = kwargs['password'] if 'password' in kwargs else ''

    def _get_client(self):
        """

        :return:
        """
        if self.ip_list is not None:
            server = random.choice(self.ip_list)
            ip, port = server.split(':')
            return 'http://%s:%s' % (ip, port)
        raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
          errmsg='Gremlin Server Ip List Error')

    def query(self, cmd):
        """

        :param cmd:
        :return:
        """
        return self._send_request(cmd)

    def _send_request(self, cmd):
        """

        :param cmd:
        :return:
        """
        header = {'Content-Type':'application/json; charset=UTF-8', 
         'Connection':'close'}
        request_data = dict()
        request_data['gremlin'] = cmd
        request_url = self._get_client()
        r = requests.post(request_url, data=(json.dumps(request_data)), headers=header)
        response_data = r.text
        return json.loads(response_data)
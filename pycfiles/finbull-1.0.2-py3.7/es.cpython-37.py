# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/finbull/lib/es.py
# Compiled at: 2019-08-01 05:16:48
# Size of source mod 2**32: 5534 bytes
import gzip, io, random, time, tornado.escape, tornado.gen, tornado.httpclient, finbull.error, finbull.log

class ElasticSearchDB(object):
    __doc__ = 'Summary\n\n    Attributes:\n        addresses (list): Description\n        client_type (str): Description\n        index (TYPE): Description\n        password (TYPE): Description\n        type (TYPE): Description\n        username (TYPE): Description\n    '
    RETRY_TIMES = 3
    REQUEST_TIMEOUT = 2

    def __init__(self, ip_list=None, consts=None, **kwargs):
        self.addresses = []
        self.consts = consts or {}
        self.ip_list = ip_list
        if self.ip_list is None:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='ip_list is empty both.')
        else:
            if not isinstance(self.ip_list, list):
                self.ip_list = [
                 self.ip_list]
            if 'index' in kwargs:
                self.index = kwargs['index']
            else:
                raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
                  errmsg='can not find index in service.conf')
        self.username = kwargs['username'] if 'username' in kwargs else ''
        self.password = kwargs['password'] if 'password' in kwargs else ''

    def get_client(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if self.ip_list is not None:
            server = random.choice(self.ip_list)
            ip, port = server.split(':')
            return 'http://%s:%s/%s' % (ip, port, self.index)
        raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
          errmsg='ElasticSearch Server Ip List Error')

    @tornado.gen.coroutine
    def query(self, body, option='_search'):
        """query interface

        Args:
            body (dict): json body
            **kwargs (dict): params

        Returns:
            dict: json string

        Raises:
            gen.Return: Description
        """
        client = tornado.httpclient.AsyncHTTPClient()
        url = self.get_client()
        if option != '_msearch':
            body = tornado.escape.json_encode(body)
        for i in range(self.RETRY_TIMES):
            _start = int(round(time.time() * 1000))
            response = yield client.fetch((url + '/%s' % option),
              raise_error=False,
              method='POST',
              body=(self._gzip_data(body)),
              headers={'Content-Encoding':'gzip', 
             'Content-Type':'application/gzip'},
              auth_username=(self.username),
              auth_password=(self.password),
              allow_nonstandard_methods=True,
              request_timeout=(self.REQUEST_TIMEOUT))
            _stop = int(round(time.time() * 1000)) - _start
            if response.code == 599:
                finbull.log.service_warning({'finbull.lib.es':'es requested timeout', 
                 'url':url, 
                 'http_code':response.code, 
                 'time':_stop, 
                 'retry':'%d/%d' % (i + 1, self.RETRY_TIMES)})
                continue
            else:
                finbull.log.service_debug({'finbull.lib.es':'es requested', 
                 'url':url, 
                 'req':body, 
                 'res':response.body, 
                 'http_code':response.code, 
                 'time':_stop, 
                 'retry':'%d/%d' % (i + 1, self.RETRY_TIMES)})
                finbull.log.service_notice({'finbull.lib.es':'es requested', 
                 'url':url, 
                 'http_code':response.code, 
                 'time':_stop, 
                 'retry':'%d/%d' % (i + 1, self.RETRY_TIMES)})
                result = tornado.escape.json_decode(response.body).get('responses', [])
                raise tornado.gen.Return(result)

        finbull.log.service_warning({'finbull.lib.es':'can not request the elasticsearch', 
         'url':url, 
         'retry_times':self.RETRY_TIMES})
        raise tornado.gen.Return([])

    @tornado.gen.coroutine
    def multi_query(self, bodies):
        """
        multi query
        """
        body = '\n'.join(['\n'.join([tornado.escape.json_encode(h), tornado.escape.json_encode(b)]) for h, b in bodies]) + '\n'
        result = yield self.query(body, option='_msearch')
        raise tornado.gen.Return(result)

    def _gzip_data(self, content):
        """
        compress the request data and response data.
        """
        zbuf = io.StringIO()
        zfile = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=zbuf)
        zfile.write(content)
        zfile.close()
        return zbuf.getvalue()
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/py56/ApiAbstract.py
# Compiled at: 2014-11-25 01:31:36
import time, StringIO
from urllib import urlencode
from hashlib import md5
import pycurl
try:
    from local_config import *
except:
    from config import *

class ApiAbstract(object):
    """
    author: Allan Sun <email: alnsun.cn@gmail.com;QQ:301585>
    """

    def __init__(self, **kwargs):
        if not kwargs:
            if APPKEY and SECRET:
                self.appkey = APPKEY
                self.secret = SECRET
            else:
                print 'Please config APPKEY and SECRET in config.py'
                return
            self.domain = DOMAIN
        self.setConf(**kwargs)
        self.CONNECT_TIMEOUT = 5
        self.READ_TIMEOUT = 5

    def setConf(self, **kwargs):
        if 'appkey' not in kwargs or 'secret' not in kwargs:
            print 'APPKEY and SECRET are requiremnets'
            return
        self.appkey = kwargs['appkey']
        self.secret = kwargs['secret']
        if 'domain' in kwargs:
            self.domain = kwargs['domain']
        elif DOMAIN:
            self.domain = DOMAIN

    def getHttp(self, url, **params):
        u"""
         @description GET 方法

         @access private
         @param mixed url
         @param dict params
         @return json
        """
        url = '%s?%s' % (url, self.signRequest(**params))
        print 'url=', url
        return self.httpCall(url)

    def httpCall(self, url, params='', method='get', connectTimeout=5, readTimeout=5):
        u"""
        @description  curl method,post方法params字符串的位置不同于get

        @access public
        @param mixed url
        @param string params
        @param string method
        @param mixed connectTimeout
        @param mixed readTimeout
        @return json
        """
        result = ''
        timeout = connectTimeout + readTimeout
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        if method.lower() == 'post':
            c.setopt(pycurl.POST, 1)
            c.setope(pycurl.POSTFIELDS, params)
        c.setopt(pycurl.CONNECTTIMEOUT, connectTimeout)
        c.setopt(pycurl.TIMEOUT, timeout)
        c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0')
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        try:
            result = c.perform()
            return b.getvalue()
        except Exception as e:
            print 'Connection error:' + str(e)
            c.close()

    def signRequest(self, **kwargs):
        kv_list = kwargs.items()
        kv_list.sort()
        req = md5(urlencode(kv_list)).hexdigest()
        ts = int(time.time())
        kwargs['appkey'] = self.appkey
        kwargs['sign'] = md5(('#').join([req, self.appkey, self.secret, str(ts)])).hexdigest()
        kwargs['ts'] = str(ts)
        return urlencode(kwargs)
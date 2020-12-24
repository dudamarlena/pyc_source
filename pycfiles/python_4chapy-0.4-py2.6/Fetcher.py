# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Fourchapy/Fetcher.py
# Compiled at: 2012-12-27 12:35:51
""" Provide a base class that makes it easy to add 
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
"""
import logging
logger = logging.getLogger('Fourchapy.' + __name__)
log = logger.log
from urllib import urlopen
import datetime
from json import loads
import time
from Errors import NoDataReturnedError, RequestRateTooHigh, InvalidDataReturnedError, Fetch404Error
last = {}

class Fetch4chan(object):
    """ Base class for classes that need to fetch and process data from
    4chan's JSON API. 
    """
    MinRequestTime = datetime.timedelta(seconds=1)
    URL = None
    lazyAttrs = {}
    shouldSleep = True
    ignoreRateLimit = False

    def __init__(self, proxies={}, url=None, sleep=None, ignoreRateLimit=None):
        """
        @param proxies: A dict of protocol:url strings that indicate what proxy to use
        when accessing a given protocol. Ex: 
        proxies=dict(http="http://p1.someproxy.com:3128",http2="http://p2.someproxy.com:3128") 
        @param url: The URL to fetch when requesting data. Must return JSON data. If
        this is a value other than None, it overrides the per-class default URL. 
        Example: url='https://api.4chan.org/board/res/123456.json'         
        @param sleep: Sleep if needed to keep above MinRequestTime. If non-True
        and we are requesting to frequently, raise Fourchapy.errors.RequestRateTooHigh.
        If None, then use the per-method and/or per-class shouldSleep value. 
        @param ignoreRateLimit: If None, use the per-method and/or per-class 
        ignoreRateLimit value. If True, only INFO-log when going over the rate limit. 
        If False, sleep or raise an error when going over the limit. See 'sleep' param
        for info on sleep vs exception for over-limit conditions.         
        """
        if sleep is not None:
            self.shouldSleep = sleep
        if ignoreRateLimit is not None:
            self.ignoreRateLimit = ignoreRateLimit
        if self.URL and url:
            log(20, 'Overwriting %r with %r' % (self.URL, url))
        if url:
            self.URL = url
        if not self.URL:
            log(40, 'No URL defined')
            raise ValueError, 'No URL defined'
        self.Proxies = proxies
        self._autoFetched = {}
        return

    @classmethod
    def addLazyDataObjDec(cls, attrName):
        """
        @param attrName: The attribute that will be updated with the value 
        update method's return value. The attrName must be unique for a given
        class.
        """
        log(10, 'Going to add lazy data object, %r, to %r', attrName, cls)

        def decorator(func):

            def newFunc(self, *args, **kw):
                log(5, 'Running %r', func)
                ret = func(self, *args, **kw)
                setattr(self, attrName, ret)
                return ret

            newFunc.__doc__ = func.__doc__
            assert attrName not in cls.lazyAttrs
            cls.lazyAttrs[attrName] = newFunc
            log(10, 'Created new func %r and added it to %r', newFunc, cls.lazyAttrs)
            return newFunc

        log(10, 'Built decorator %r', decorator)
        return decorator

    def _isOurMethod(self, attr):
        """ Return True if the lazyAttrs function listed under
        attr is a method of this class. 
        """
        for testAttrName in dir(self):
            testAttr = getattr(self, testAttrName)
            if hasattr(testAttr, 'im_func'):
                func = getattr(testAttr, 'im_func')
                if func == self.lazyAttrs[attr]:
                    log(10, '%r (aka %r) is in %r under %r', func, testAttr, self, attr)
                    return True

        return False

    def __getattr__(self, attr):
        if attr in self.lazyAttrs and self._isOurMethod(attr=attr):
            log(10, 'Incoming request for our information via %r.%r', self, attr)
            setattr(self, attr, None)
            if attr in self._autoFetched and self._autoFetched[attr]:
                log(50, "We've (%r) already tried to update. We didn't succeed for some reason. Not re-running fetch. ", self)
                raise RuntimeError('Already run an update for %r once on %r- Not running it again. ' % (attr, self))
            self._autoFetched[attr] = True
            method = self.lazyAttrs[attr]
            value = method(self)
            log(5, 'Got %r from %r on %r', value, method, self)
            assert hasattr(self, attr)
            return value
        else:
            raise AttributeError('%r object has no attribute %r' % (self, attr))
            return

    def fetchText(self, data='', sleep=None, ignoreRateLimit=None):
        """ Fetch all data from self.URL
        @param data: A key:value mapping of post data to send with the request 
        @param sleep: Sleep if needed to keep above MinRequestTime. If non-True
        and we are requesting to frequently, raise Fourchapy.errors.RequestRateTooHigh.
        If None, then use the per-object or per-class shouldSleep value. 
        @param ignoreRateLimit: If None, use the per-object or per-class ignore
        rate limit value. If True, only INFO-log when going over the rate limit. 
        If False, sleep or raise an error when going over the limit. See 'sleep' param
        for info on sleep vs exception for over-limit conditions.  
        """
        t = type(self).__name__
        if last.has_key(t):
            log(5, 'Last request: %r', last[t])
            delta = datetime.datetime.now() - last[t]
            if delta < datetime.timedelta.min:
                log(10, 'Time seems to have gone backwards by %r. Letting request proceed as-is. ', delta)
            elif delta < self.MinRequestTime:
                if ignoreRateLimit or self.ignoreRateLimit:
                    log(20, "Ignoring rate limit! We're requesting too fast. Last request was %r ago. Min normally required is %r. ", delta, self.MinRequestTime)
                elif sleep or sleep is None and self.shouldSleep:
                    sleepTime = self.MinRequestTime - delta
                    sleepTimeFloat = float(sleepTime.days * 86400 + sleepTime.seconds + sleepTime.microseconds / 1000000.0)
                    log(10, 'Request rate too high. Sleeping for %r (aka %r seconds). ', sleepTime, sleepTimeFloat)
                    time.sleep(sleepTimeFloat)
                else:
                    raise RequestRateTooHigh('Request rate is too high. Last request was %r ago. Min time since last request must be %r. ' % (delta, self.MinRequestTime))
        else:
            log(5, 'First request - No need to rate limit yet. ')
        last[t] = datetime.datetime.now()
        if data is None:
            data = ''
        else:
            if isinstance(data, dict):
                for (k, v) in data.items():
                    if k is None or v is None:
                        del data[k]

            elif isinstance(data, str):
                pass
            else:
                log.warn('Unknown data value type. Got %r. ', data)
            log(10, 'Going to open %r with data %r', self.URL, data)
            if data:
                fHandle = urlopen(url=self.URL, data=data, proxies=self.Proxies)
            else:
                fHandle = urlopen(url=self.URL, proxies=self.Proxies)
            log(10, 'Successfully opened url: %r', fHandle)
            try:
                log(5, 'Starting to read data')
                text = fHandle.read()
                log(10, 'Read %d bytes', len(text))
                self._raw_text = text
                return text
            finally:
                fHandle.close()

            return

    RE_404_MATCH = '^\\s*<html>\\s*<head>\\s*<title>404 Not Found</title>'

    def fetchJSON(self, data='', sleep=None, ignoreRateLimit=None):
        """ Fetch all JSON from self.URL and return decoded
        @param data: A key:value mapping of post data to send with the request 
        @param sleep: Sleep if needed to keep above MinRequestTime. If non-True
        and we are requesting to frequently, raise Fourchapy.errors.RequestRateTooHigh.
        If None, then use the per-object or per-class shouldSleep value. 
        @param ignoreRateLimit: If None, use the per-object or per-class ignore
        rate limit value. If True, only INFO-log when going over the rate limit. 
        If False, sleep or raise an error when going over the limit. See 'sleep' param
        for info on sleep vs exception for over-limit conditions. 
        """
        log(10, 'Going to fetch %r as JSON', self.URL)
        text = self.fetchText(data=data, sleep=sleep, ignoreRateLimit=ignoreRateLimit)
        if len(text) == 0:
            raise NoDataReturnedError, 'A zero byte file was returned'
        i = 1
        while i * 50 < len(text):
            log(5, 'Fetched data (line %05d): %r' % (i, text[(i - 1) * 50:i * 50]))
            i += 1

        log(10, 'Translating JSON into objects')
        try:
            ret = loads(text)
        except ValueError, e:
            log(10, 'Failed to decode JSON with %r', e)
            if '404 Not Found' in text[:200]:
                import re
                if re.match(self.RE_404_MATCH, text, re.MULTILINE | re.DOTALL):
                    log(30, 'Got a 404 error from %r', self.URL)
                    raise Fetch404Error('Got a 404 error from %r' % self.URL)
                else:
                    log(40, "Didn't get valid JSON but isn't a 404 - Something's amiss with %r", self.URL)
            log(10, '----------' + ' Begin Data ' + '----------')
            for line in text.splitlines():
                log(10, 'Line: %r' % line)

            log(10, '----------End Data' + '----------')
            raise InvalidDataReturnedError("Data from 4chan wasn't JSON")

        log(5, 'Decoded %r', ret)
        return ret
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/pyjznet/utils.py
# Compiled at: 2014-12-12 03:34:14
from __future__ import print_function
import json, time
from datetime import datetime, timedelta

def try_parse_json(text):
    if text is None:
        return
    else:
        try:
            return json.loads(text)
        except Exception as e:
            return

        return


def safeunicode(obj, encoding='utf-8'):
    r"""
    Converts any given object to unicode string.

        >>> safeunicode('hello')
        u'hello'
        >>> safeunicode(2)
        u'2'
        >>> safeunicode('\xe1\x88\xb4')
        u'\u1234'
    """
    t = type(obj)
    if t is unicode:
        return obj
    if t is str:
        return obj.decode(encoding, 'ignore')
    if t in [int, float, bool]:
        return unicode(obj)
    if hasattr(obj, '__unicode__') or isinstance(obj, unicode):
        try:
            return unicode(obj)
        except Exception as e:
            return ''

    else:
        return str(obj).decode(encoding, 'ignore')


class TimeoutException(Exception):
    pass


class ValueFuture(object):

    def __init__(self):
        self.fulfill_callbacks = []
        self.reject_callbacks = []
        self.value = None
        self._is_done = False
        return

    def done(self):
        self._is_done = True

    def is_done(self):
        return self._is_done

    def set(self, value):
        self.value = value

    def set_result(self, value):
        if self.is_done():
            return
        self.set(value)
        self.done()
        self.call_fulfills(value)

    def call_fulfills(self, value):
        for fulfill in self.fulfill_callbacks:
            if fulfill is not None:
                try:
                    fulfill(value)
                except Exception as e:
                    pass

        return

    def call_rejects(self, exception):
        for reject in self.reject_callbacks:
            if reject is not None:
                try:
                    reject(exception)
                except Exception as e:
                    pass

        return

    def cancel(self, may_interrupt_if_running=False):
        self._is_done = True
        self.call_rejects(Exception('future task canceled'))

    def get(self, timeout=5000):
        if self.is_done():
            return self.value
        start_time = datetime.now()

        def timedout():
            return start_time + timedelta(milliseconds=timeout) < datetime.now()

        while not self.is_done() and not timedout():
            time.sleep(0.05)

        if not self.is_done():
            raise TimeoutException()
        return self.value

    def fulfill(self, callback):
        if callback is not None:
            self.fulfill_callbacks.append(callback)
            if self.is_done():
                try:
                    callback(self.get())
                except Exception as e:
                    pass

        return

    def reject(self, callback):
        if callback is not None:
            self.reject_callbacks.append(callback)
        return
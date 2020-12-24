# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ojcrawler/tests/test_sync_func.py
# Compiled at: 2018-12-27 10:27:24
from __future__ import absolute_import, division, print_function, unicode_literals
import inspect

def sample_sync_func(status, *args, **kwargs):
    pass


class Controller(object):

    def __init__(self, oj_name, sync_func=sample_sync_func):
        self.oj = oj_name
        args = inspect.getargspec(sync_func)[0]
        if len(args) < 1 or args[0] != b'status':
            raise ValueError((b'sync_func的第一个参数必须为status而不是{}, sample: sync_func(status, *args, **kwargs)').format(args[0]))
        self.func = sync_func

    def run(self, *args, **kwargs):
        self.func(b'test', *args, **kwargs)


def sync_fun(status, ip, port):
    print(b'status:', status)
    print(b'ip:', ip)
    print(b'port:', port)


if __name__ == b'__main__':
    c = Controller(b'x')
    c.run()
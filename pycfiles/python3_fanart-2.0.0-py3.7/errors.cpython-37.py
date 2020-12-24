# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fanart/errors.py
# Compiled at: 2019-03-10 14:53:05
# Size of source mod 2**32: 306 bytes


class FanartError(Exception):

    def __str__(self):
        return ', '.join(map(str, self.args))

    def __repr__(self):
        name = self.__class__.__name__
        return '%s%r' % (name, self.args)


class ResponseFanartError(FanartError):
    pass


class RequestFanartError(FanartError):
    pass
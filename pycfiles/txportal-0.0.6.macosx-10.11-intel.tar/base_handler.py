# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/txportal/simulator/handlers/base_handler.py
# Compiled at: 2016-03-18 12:19:39
from twisted.internet import defer
from txradius import client
import functools

class ACError(BaseException):
    pass


class BasicHandler:

    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger
        self.secret = str(self.config.get('secret', 'secret'))
        self.vendor = str(self.config.get('vendor', 'vendor'))

    def process(self, req, rundata):
        if 'cmccv1' in self.vendor:
            return self.proc_cmccv1(req, rundata)
        if 'cmccv2' in self.vendor:
            return self.proc_cmccv2(req, rundata)
        if 'huaweiv1' in self.vendor:
            return self.proc_huaweiv1(req, rundata)
        if 'huaweiv2' in self.vendor:
            return self.proc_huaweiv2(req, rundata)
        raise ACError(('vendor {0} not support').format(self.vendor))

    def proc_cmccv1(self, req, rundata):
        raise ACError('does not support')

    def proc_cmccv2(self, req, rundata):
        raise ACError('does not support')

    def proc_huaweiv1(self, req, rundata):
        raise ACError('does not support')

    def proc_huaweiv2(self, req, rundata):
        raise ACError('does not support')


class EmptyHandler(BasicHandler):

    def process(self, req, rundata):
        self.logger.error(('do nothing for {0}').format(repr(req)))
        return
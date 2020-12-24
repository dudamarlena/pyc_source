# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/filter.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Filter', 'LogFilter']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractmethod
import logging
LOGGER = logging.getLogger(__name__)

class Filter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def filter(self, request):
        pass

    @abstractmethod
    def get_order(self):
        pass


class LogFilter(Filter):

    def filter(self, request):
        LOGGER.info('%s.%s() is invoked, ' % (request.class_name, request.method_name) + 'with arguments: %s, ' % (request.args,) + 'keyword arguments: %s, ' % (request.kwargs,) + 'meta: %s' % request.meta)

    def get_order(self):
        import sys
        return sys.maxint
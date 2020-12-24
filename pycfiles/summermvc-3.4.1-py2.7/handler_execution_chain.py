# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/handler_execution_chain.py
# Compiled at: 2018-05-30 05:46:35
__all__ = [
 'HandlerExecutionChain']
__authors__ = ['Tim Chow']
from .exception import InterceptError

class HandlerExecutionChain(object):

    def __init__(self, handler, interceptors):
        self._handler = handler
        self._interceptors = interceptors

    def handle(self, request, response, mv, *args, **kwargs):
        for hi in self.interceptors:
            try:
                hi.pre_handle(request, response, mv)
            except InterceptError:
                return

        result = self.handler.invoke(*args, **kwargs)
        for hi in self.interceptors:
            try:
                hi.post_handle(request, response, mv)
            except InterceptError:
                break

        return result

    @property
    def handler(self):
        return self._handler

    @property
    def interceptors(self):
        return self._interceptors
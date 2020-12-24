# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/invoker.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Invoker', 'RpcInvoker']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractmethod
from concurrent.futures import TimeoutError
from .result import Result
from .exception import *

class Invoker(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def invoke(self, request, connection, serializer, write_timeout, read_timeout):
        pass


class RpcInvoker(Invoker):

    def invoke(self, request, connection, serializer, write_timeout, read_timeout):
        buff = serializer.dumps(request)
        transaction_id, write_future = connection.write(buff, write_timeout)
        read_future = connection.read(transaction_id)
        transaction_id = write_future.result()
        try:
            response = read_future.result(read_timeout)
        except TimeoutError:
            raise ConnectionReadTimeout('timeout: %s' % read_timeout)

        result = serializer.loads(response)
        if not isinstance(result, Result):
            raise InvalidResponseError('expect Result, not %s' % type(result).__name__)
        if result.exc is not None:
            raise result.exc
        return result.result
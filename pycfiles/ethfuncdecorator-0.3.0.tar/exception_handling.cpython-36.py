# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/exception_handling.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 671 bytes
from web3.utils.toolz import excepts

def construct_exception_handler_middleware(method_handlers=None):
    if method_handlers is None:
        method_handlers = {}

    def exception_handler_middleware(make_request, web3):

        def middleware(method, params):
            if method in method_handlers:
                exc_type, handler = method_handlers[method]
                return excepts(exc_type, make_request, handler)(method, params)
            else:
                return make_request(method, params)

        return middleware

    return exception_handler_middleware
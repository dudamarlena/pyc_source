# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/exceptions/implicit_cast_exception.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 916 bytes


class ImplicitCastException(Exception):

    def __init__(self, code, message, resulting_type):
        self.code = code
        self.message = message
        self.resulting_type = resulting_type
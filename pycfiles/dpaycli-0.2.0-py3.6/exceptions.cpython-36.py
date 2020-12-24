# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycliapi/exceptions.py
# Compiled at: 2018-10-14 09:33:48
# Size of source mod 2**32: 1642 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import re

def decodeRPCErrorMsg(e):
    """ Helper function to decode the raised Exception and give it a
        python Exception class
    """
    found = re.search('(10 assert_exception: Assert Exception\n|3030000 tx_missing_posting_auth).*: (.*)\n',
      (str(e)),
      flags=(re.M))
    if found:
        return found.group(2).strip()
    else:
        return str(e)


class UnauthorizedError(Exception):
    __doc__ = 'UnauthorizedError Exception.'


class RPCConnection(Exception):
    __doc__ = 'RPCConnection Exception.'


class RPCError(Exception):
    __doc__ = 'RPCError Exception.'


class RPCErrorDoRetry(Exception):
    __doc__ = 'RPCErrorDoRetry Exception.'


class NumRetriesReached(Exception):
    __doc__ = 'NumRetriesReached Exception.'


class CallRetriesReached(Exception):
    __doc__ = 'CallRetriesReached Exception. Only for internal use'


class MissingRequiredActiveAuthority(RPCError):
    pass


class UnkownKey(RPCError):
    pass


class NoMethodWithName(RPCError):
    pass


class NoApiWithName(RPCError):
    pass


class ApiNotSupported(RPCError):
    pass


class UnhandledRPCError(RPCError):
    pass


class NoAccessApi(RPCError):
    pass


class InvalidEndpointUrl(Exception):
    pass


class UnnecessarySignatureDetected(Exception):
    pass


class WorkingNodeMissing(Exception):
    pass


class TimeoutException(Exception):
    pass
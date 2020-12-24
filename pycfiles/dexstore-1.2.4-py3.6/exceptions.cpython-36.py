# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstoreapi/exceptions.py
# Compiled at: 2019-03-19 09:04:59
# Size of source mod 2**32: 851 bytes
import re
from grapheneapi.exceptions import RPCError

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


class MissingRequiredActiveAuthority(RPCError):
    pass


class NoMethodWithName(RPCError):
    pass


class UnhandledRPCError(RPCError):
    pass


class NumRetriesReached(Exception):
    pass


class InvalidEndpointUrl(Exception):
    pass


class AccountCouldntBeFoundException(Exception):
    pass


class InvalidAccountNameException(Exception):
    pass
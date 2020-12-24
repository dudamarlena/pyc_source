# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/rpc/exceptions.py
# Compiled at: 2014-10-03 04:21:29
"""

  RPC exceptions
  ~~~~~~~~~~~~~~

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
from . import ServerException
from . import ClientException
from . import Exception as Error

class InternalRPCException(Error):
    """ Base class for all errors in service handlers module. """
    pass


class ServiceConfigurationError(InternalRPCException):
    """ When service configuration is incorrect. """
    pass


class RequestError(ClientException):
    """ Error occurred when building request. """
    pass


class ResponseError(ServerException):
    """ Error occurred when building response. """
    pass
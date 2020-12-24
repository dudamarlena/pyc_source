# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/exceptions.py
# Compiled at: 2018-01-29 12:10:54
# Size of source mod 2**32: 3103 bytes
import sys, traceback

class MercuryGeneralException(Exception):
    pass


class MercuryBackendError(MercuryGeneralException):
    pass


class MercuryIdException(MercuryGeneralException):
    pass


class MercuryCritical(MercuryGeneralException):
    pass


class MercuryUserError(MercuryGeneralException):
    pass


class MercuryRecoverableError(MercuryGeneralException):
    pass


class MercuryConfigurationError(MercuryGeneralException):
    pass


class MercuryTaskTimeout(MercuryGeneralException):
    pass


class MercuryClientException(MercuryGeneralException):
    pass


class HPFirmwareException(MercuryGeneralException):
    pass


class MercuryFirmwareException(MercuryGeneralException):
    pass


class MercuryTransportError(MercuryGeneralException):
    pass


class EndpointError(MercuryGeneralException):

    def __init__(self, message, endpoint, request=None):
        """
        Raised when an exception is encountered while processing an endpoint
        request
        :param message: Description of the error
        :param endpoint: The called endpoint
        :param request: The data used to trigger the exception
        """
        self.message = message
        self.endpoint = endpoint
        self.request = request


def tb_to_dict(path, line, scope, code):
    return {'path':path, 
     'line':line, 
     'scope':scope, 
     'code':code}


def parse_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return {'exc_type':str(exc_type), 
     'exc_value':str(exc_value), 
     'stack':[tb_to_dict(*tb) for tb in traceback.extract_tb(exc_traceback)]}


def find_window(stack):
    """
    Using extract_stack vs extract_tb would require use to inspect the relevant entries. Essentially anything
    :param stack:
    :return:
    """
    return stack[(-1)]


def fancy_traceback_short(exc_dict, preamble='Exception info: '):
    """

    :param exc_dict:
    :param preamble:
    :return:
    """
    output = '{preamble} ({exc_type} : {exc_value}): '.format(preamble=preamble, exc_type=(exc_dict['exc_type']),
      exc_value=(exc_dict['exc_value']))
    current_window = find_window(exc_dict['stack'])
    output += ('scope={scope}, path={path}, line={line}, code={code}'.format)(**current_window)
    return output
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/foxtrot-api-client/lib/python3.4/site-packages/foxtrot/errors.py
# Compiled at: 2015-05-24 07:26:02
# Size of source mod 2**32: 682 bytes


class FoxtrotError(RuntimeError):

    def __init__(self, message):
        super(FoxtrotError, self).__init__(message)


class ParameterError(FoxtrotError):

    def __init__(self, param):
        self.parameter = param
        super(ParameterError, self).__init__('Missing parameter: {}'.format(param))


class APIResponseError(FoxtrotError):
    pass


class APIJSONError(FoxtrotError):

    def __init__(self, response):
        self.response = response
        super(APIJSONError, self).__init__('Response was invalid JSON.')


class APITimeoutError(FoxtrotError):

    def __init__(self, count):
        self.count = count
        super(APITimeoutError, self).__init__('Request timed out after {} seconds.'.format(count))
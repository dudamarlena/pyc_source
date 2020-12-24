# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/breinify/BreinExceptions.py
# Compiled at: 2016-08-05 17:06:47
# Size of source mod 2**32: 764 bytes


class BreinAPIConnectionError(ConnectionError):

    def __init__(self, response):
        super(BreinAPIConnectionError, self).__init__('Non-normal lookup response: ' + str(response.status_code), response)


class invalidArguementException(ValueError):

    def __init__(self, value, expected):
        super(invalidArguementException, self).__init__("Got '" + str(value) + "' expected one of " + str(expected), value)


class noSecretKeyException(ValueError):

    def __init__(self):
        super(noSecretKeyException, self).__init__('Tried to sign message, but no secret key found. Either disable signing or call breinify.setSecret(...)')
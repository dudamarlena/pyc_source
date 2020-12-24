# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/wimsapi/exceptions.py
# Compiled at: 2020-05-04 16:09:45
# Size of source mod 2**32: 987 bytes


class WimsAPIError(Exception):
    __doc__ = 'Base exception for WimsAPI.'


class InvalidResponseError(WimsAPIError):
    __doc__ = 'Raised when WIMS send a badly formatted response.'

    def __init__(self, message, response):
        self.message = message
        self.response = response

    def __str__(self):
        return self.message


class AdmRawError(WimsAPIError):
    __doc__ = 'Raised when an error occurs while communicating with the WIMS server.'

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "WIMS' server responded with an ERROR: " + self.message


class NotSavedError(WimsAPIError):
    __doc__ = 'Raised trying to use a method needing an object to be saved, without the object being\n    actually saved (eg. deleting an unsaved class).'


class InvalidItemTypeError(WimsAPIError):
    __doc__ = 'Raised when trying to add/get/delete an invalide type from a WIMS class.'
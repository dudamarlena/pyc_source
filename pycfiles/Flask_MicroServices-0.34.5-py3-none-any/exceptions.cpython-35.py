# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Projects\flask-microservices\flask_microservices\exceptions.py
# Compiled at: 2017-01-26 00:24:27
# Size of source mod 2**32: 735 bytes


class InvalidModulePath(Exception):
    __doc__ = 'Raised when an invalid module path is provided to\n  `MicroServicesApp.register_urls()`\n  '


class InvalidURLFunction(Exception):
    __doc__ = 'Raised when a url is passed a non-function value.\n  '


class InvalidURLPattern(Exception):
    __doc__ = 'Raised when a non `flask_microservices.url` value is\n  given as a URLPattern.\n  '


class InvalidURLRule(Exception):
    __doc__ = 'Raised when a non-string value is passed as a rule.\n  '


class InvalidURLName(Exception):
    __doc__ = 'Raised when a non-string value is passed as a name.\n  '


class UnspecifiedURLMethods(Exception):
    __doc__ = 'Raised when an empty list, or a list of blank strings\n   is passed as a method.\n  '
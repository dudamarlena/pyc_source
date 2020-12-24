# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/errors.py
# Compiled at: 2015-11-05 07:02:27
# Size of source mod 2**32: 673 bytes


class HoerApiError(Exception):
    pass


class InvalidJsonError(HoerApiError):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return repr(self.text)


class ApiError(HoerApiError):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class NoDataError(HoerApiError):
    pass


class InvalidDataError(HoerApiError):

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return repr(self.err)


class MissingAttributeError(InvalidDataError):

    def __init__(self, attr):
        self.attr = attr

    def __str__(self):
        return repr(self.attr)
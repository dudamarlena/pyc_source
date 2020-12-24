# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/tmp/Flask-SocketAPI/venv/lib/python3.5/site-packages/flask_socketapi/exc.py
# Compiled at: 2016-07-11 08:08:31
# Size of source mod 2**32: 204 bytes


class SocketAPIError(Exception):
    pass


class InvalidRequestError(SocketAPIError):
    pass


class InvalidURIError(InvalidRequestError):
    pass


class NotFoundError(InvalidRequestError):
    pass
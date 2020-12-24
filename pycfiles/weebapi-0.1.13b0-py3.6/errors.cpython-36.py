# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\weebapi\errors.py
# Compiled at: 2018-04-13 12:27:43
# Size of source mod 2**32: 368 bytes


class RequireFormatting(Exception):
    pass


class MissingRequiredArguments(Exception):
    pass


class WeirdResponse(Exception):
    pass


class SpecifyClient(Exception):
    pass


class Forbidden(Exception):
    pass


class DiscordPyNotInstalled(Exception):
    pass


class NotFound(Exception):
    pass
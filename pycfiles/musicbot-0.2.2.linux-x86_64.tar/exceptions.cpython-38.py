# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/exceptions.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 195 bytes


class MusicbotError(Exception):
    pass


class MusicbotConfigError(MusicbotError):
    pass


class FailedAuthentication(MusicbotError):
    pass


class FailedRequest(MusicbotError):
    pass
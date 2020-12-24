# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cuiows/exc.py
# Compiled at: 2016-12-22 09:51:49
# Size of source mod 2**32: 379 bytes


class WebsocketError(Exception):
    """WebsocketError"""
    pass


class WebsocketClosedError(WebsocketError):
    """WebsocketClosedError"""

    def __init__(self, code: int, reason: str):
        self.code = code
        self.reason = reason
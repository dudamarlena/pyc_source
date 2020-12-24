# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/sciroccoclient/responses.py
# Compiled at: 2016-11-22 16:46:46
# Size of source mod 2**32: 497 bytes


class ClientMessageResponse:
    __doc__ = '\n    This object is filled by DAL layer and received by client.\n    '

    def __init__(self):
        self._metadata = None
        self._payload = None

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, data):
        self._metadata = data

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellexer/core/response_wrapper.py
# Compiled at: 2019-04-16 11:15:40
# Size of source mod 2**32: 992 bytes
import json
from . import errors

class Response:
    __slots__ = ('__request_functin', '__response_builder', '__response')

    def __init__(self, response_builder, request_functin=None, response=None):
        self._Response__request_functin = request_functin
        self._Response__response_builder = response_builder
        self._Response__response = response

    def __response_handler(self):
        try:
            response = self._Response__request_functin()
            decoded_response = response.read().decode()
            if response.status == 200:
                return decoded_response
            if response.status in range(400, 500):
                raise errors.BadRequest400(decoded_response)
            if response.status in range(500, 600):
                raise errors.BadRequest500(decoded_response)
        finally:
            response.release_conn()

    @property
    def raw(self):
        if not self._Response__response:
            self._Response__response = self._Response__response_handler()
        return self._Response__response

    @property
    def data(self):
        return self._Response__response_builder(self.raw)

    @property
    def json(self):
        return json.loads(self.raw)
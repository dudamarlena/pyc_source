# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jazg/work/kristall/src/kristall/request.py
# Compiled at: 2020-01-02 16:13:45
# Size of source mod 2**32: 2412 bytes
import json
from typing import Optional, Type, Union
from werkzeug.exceptions import RequestEntityTooLarge
import werkzeug.wrappers as WRequest

class Request(WRequest):
    __doc__ = 'Wrapper over :class:`~werkzeug.wrappers.Request` that has built in\n    support for JSON content. Maximum content length is set to 4 megabytes.\n    '
    MAX_CONTENT_LENGTH = 4194304

    def __init__(self, environ, populate_request=True, shallow=False, json_decoder=None):
        """Object initializer that allows setting JSON decoder class to be used
        when decoding JSON content. For complete description of other arguments
        see Werkzeug documentation for :class:`~werkzeug.wrappers.BaseRequest`.
        """
        super().__init__(environ, populate_request, shallow)
        self.decoder = json_decoder
        if self.decoder is None:
            self.decoder = json.JSONDecoder

    def get_data(self, cache=True, as_text=True, parse_form_data=False):
        """Overwritten method that retrieves request data. Difference is that
        by default it fetches data as text. For complete description of call
        arguments see Werkzeug documentation for
        :meth:`~werkzeug.wrappers.BaseRequest.get_data`. This method raises
        :exc:`~werkzeug.exceptions.RequestEntityTooLarge` if content length
        exceeds allowed size (default is 4 megabytes).
        """
        if self.content_length > self.MAX_CONTENT_LENGTH:
            raise RequestEntityTooLarge(f"Request size exceeds allowed {self.MAX_CONTENT_LENGTH} bytes")
        return super().get_data(cache, as_text, parse_form_data)

    def get_json(self, decoder: Optional[Type]=None) -> dict:
        """A method to retrieve JSON from request data, optionally using
        specified JSON decoder class. If not provided default decoder class
        is used.

        :param decoder: JSON decoder class, defaults to None
        :type decoder: Optional[Type], optional
        :return: request data as parsed JSON
        :rtype: dict
        """
        if decoder is None:
            decoder = self.decoder
        data = self.get_data()
        return json.loads(data, cls=decoder)
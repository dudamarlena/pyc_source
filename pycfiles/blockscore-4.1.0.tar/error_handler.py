# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/http_client/error_handler.py
# Compiled at: 2015-03-04 21:31:22
from blockscore.error import BlockscoreError, AuthorizationError, InternalServerError, ValidationError, ParameterError, NotFoundError
from blockscore.http_client.response_handler import ResponseHandler

class ErrorHandler:

    def check_error(self, response, *args, **kwargs):
        code = response.status_code
        if 200 <= code < 300:
            return
        else:
            self.body = ResponseHandler.get_body(response)
            self.message = self.get_message(self.body)
            self.error_type = self.error_code = self.param = None
            if 'error' in self.body.keys():
                error = self.body['error']
                self.error_type = self.get_value(error, 'type')
                self.error_code = self.get_value(error, 'code')
                self.param = self.get_value(error, 'param')
            self.process_code(code)
            return

    def process_code(self, code):
        if code == 400:
            if self.param is not None:
                raise ValidationError(self.message, self.body, self.param, self.error_type, self.error_code)
            else:
                raise ParameterError(self.message, self.body, self.error_type)
        elif code == 404:
            raise NotFoundError(self.message, self.body, self.error_type)
        elif code == 401:
            raise AuthorizationError(self.message, self.body, self.error_type)
        elif code == 500:
            raise InternalServerError(self.message, self.body, self.error_type)
        else:
            raise BlockscoreError(self.message, self.body)
        return

    @staticmethod
    def get_message(body):
        message = ''
        if isinstance(body, str):
            message = body
        elif isinstance(body, dict):
            if 'error' in body.keys():
                message = body['error']['message']
            else:
                message = 'Unable to select error message from json returned by request responsible for error'
        else:
            message = 'Unable to understand the content type of response returned by request responsible for error'
        return message

    @staticmethod
    def get_value(obj, key):
        if key in obj.keys():
            return obj[key]
        else:
            return
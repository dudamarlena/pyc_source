# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/meya_api.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import re, copy, os, requests
from meya_cli.meya_config import REST_API_VERSION, USER_AGENT_STRING

class MeyaAPIException(Exception):
    PATTERN = re.compile('.*')
    MESSAGE = None

    @classmethod
    def raise_if_match(cls, error):
        for error in error:
            if cls.PATTERN.match(error):
                raise cls(cls.MESSAGE or error)


class MeyaNoSuchFileException(MeyaAPIException):
    PATTERN = re.compile('No such.*file.*')


class MeyaFileTooBigException(MeyaAPIException):
    PATTERN = re.compile('.*Ensure this field has no more than .* characters.*')


class MeyaInvalidAPIKey(MeyaAPIException):
    PATTERN = re.compile('.*Invalid API key.*')
    MESSAGE = 'The API key you are trying to use is invalid. Please check the API key of the bot you intend to use on its Settings page.'


class MeyaVersionUnsupported(MeyaAPIException):
    PATTERN = re.compile('.*API version.*exceeds.*')

    def __init__(self, message):
        super(MeyaVersionUnsupported, self).__init__('Server reported: ' + message + '\nmeya-cli is out of date. ' + "Please run 'pip install --upgrade meya-cli'.")


ERROR_TYPES = [
 MeyaNoSuchFileException,
 MeyaFileTooBigException,
 MeyaInvalidAPIKey,
 MeyaVersionUnsupported,
 MeyaAPIException]

class MeyaAPI(object):
    REQUEST_TIMEOUT = 60

    def __init__(self, api_key, base_url, command_string=''):
        self.api_key = api_key
        self.base_url = base_url
        self.command_string = command_string

    def _add_metadata(self, base_json):
        json = copy.copy(base_json)
        json['version'] = REST_API_VERSION
        json['user_agent'] = USER_AGENT_STRING
        if self.command_string:
            json['command'] = self.command_string
        return json

    def _send_request(self, send_method, path, data={}):
        return send_method(os.path.join(self.base_url, path), headers={'content-type': 'application/json'}, json=self._add_metadata(data), auth=(
         self.api_key, None), timeout=self.REQUEST_TIMEOUT)

    def _handle_response(self, response):
        errors, warnings = self._parse_errors_and_warnings(response)
        if response.status_code < 200 or response.status_code >= 300:
            self._raise_error(errors, response)
        self._print_warnings(warnings)
        return response.json()

    def _parse_errors_and_warnings(self, response):
        try:
            response_data = response.json()
            errors = response_data.get('errors', [])
            if 'detail' in response_data:
                errors.append(response_data['detail'])
            warnings = response_data.get('warnings', [])
        except ValueError:
            errors = []
            warnings = []

        return (
         errors, warnings)

    def _raise_error(self, errors, response):
        if not errors:
            if response.status_code == 404:
                errors = ["Got 404 from '" + response.request.url + "'. This URL format might be incorrect, or an incorrect 'api_root' might be set."]
            else:
                errors = [
                 'Unexpected server error. Got back: ' + response.text]
        for cls in ERROR_TYPES:
            cls.raise_if_match(errors)

    def _print_warnings(self, warnings):
        for warning in warnings:
            print(warning)

    def get(self, path):
        response = self._send_request(requests.get, path)
        return self._handle_response(response)

    def post(self, path, data):
        response = self._send_request(requests.post, path, data)
        return self._handle_response(response)

    def delete(self, path):
        response = self._send_request(requests.delete, path)
        return self._handle_response(response)
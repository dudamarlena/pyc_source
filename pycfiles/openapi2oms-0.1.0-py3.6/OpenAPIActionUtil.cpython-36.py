# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openapi2oms/utils/OpenAPIActionUtil.py
# Compiled at: 2019-10-16 02:14:28
# Size of source mod 2**32: 2327 bytes
import re
from openapi2oms.exceptions.MappingError import MappingError

class OpenAPIActionUtil:
    PATTERN_WORD = re.compile('[a-z{}A-Z0-9]*')
    PATTERN_SANITIZE = re.compile('((?![a-zA-Z0-9]).)')

    @staticmethod
    def _gen_action_name(path: str, http_method: str, content: dict):
        res = OpenAPIActionUtil.PATTERN_WORD.finditer(path)
        action_name = http_method
        first_param_encountered = False
        for part in res:
            word = part.group()
            if word == '':
                pass
            else:
                if word.startswith('{'):
                    ext = 'By'
                    if first_param_encountered:
                        ext = 'And'
                    append = ext + word[1:-1].capitalize()
                    first_param_encountered = True
                else:
                    append = word.capitalize()
            action_name += OpenAPIActionUtil._sanitize(append)

        return action_name

    @staticmethod
    def _sanitize(string: str) -> str:
        return re.sub(OpenAPIActionUtil.PATTERN_SANITIZE, '', string)

    @staticmethod
    def generate_action_name(path: str, http_method: str, content: dict):
        if content.get('operationId'):
            return content['operationId']
        else:
            return OpenAPIActionUtil._gen_action_name(path, http_method, content)

    _types = {'integer':'int', 
     'number':'number', 
     'string':'string', 
     'boolean':'boolean', 
     'array':'list', 
     'object':'object'}

    @staticmethod
    def to_oms_type(openapi_type: str):
        oms_type = OpenAPIActionUtil._types.get(openapi_type)
        if oms_type is None:
            raise MappingError(f"The OpenAPI type {openapi_type} could not be mapped to an OMS type.")
        return oms_type

    _locations = {'query':'query', 
     'path':'path', 
     'header':'header'}

    @staticmethod
    def to_oms_argument_location(openapi_location: str):
        oms_location = OpenAPIActionUtil._locations.get(openapi_location)
        if oms_location is None:
            raise MappingError(f"The OpenAPI parameter location {openapi_location} could not be mapped to an OMS parameter location.")
        return oms_location
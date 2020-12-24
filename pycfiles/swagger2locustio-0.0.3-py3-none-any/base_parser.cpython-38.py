# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/parsers/base_parser.py
# Compiled at: 2020-05-07 07:40:51
# Size of source mod 2**32: 2616 bytes
"""Module: Base Parser"""
from abc import ABC, abstractmethod
from typing import Set, Dict

class SwaggerBaseParser(ABC):
    __doc__ = 'Class: Swagger Base Parser'

    def parse_swagger_file(self, file_content: dict, mask: Dict[(str, Set[str])]) -> dict:
        """Method: parse swagger file"""
        data = {'host':self.parse_host_data(file_content), 
         'security':self.parse_security_data(file_content), 
         'paths':self.parse_paths_data(file_content, mask)}
        return data

    @staticmethod
    def parse_host_data(file_content: dict) -> str:
        """Method: parse host data"""
        return file_content.get('host', '')

    @staticmethod
    def parse_security_data(file_content: dict) -> dict:
        """Method: parse security data"""
        security = {}
        security_definitions = file_content.get('securityDefinitions', {})
        for security_config in security_definitions.values():
            security_type = security_config.get('type', '')
            security[security_type] = security_config
        else:
            return security

    def parse_paths_data(self, file_content: dict, mask: Dict[(str, Set[str])]) -> dict:
        """Method: parse paths data"""
        paths_white_list = mask['paths_white_list']
        paths_black_list = mask['paths_black_list']
        tags_white_list = mask['tags_white_list']
        tags_black_list = mask['tags_black_list']
        api_paths = {}
        paths = file_content.get('paths')
        if paths is None:
            raise ValueError('No paths is found in swagger file')
        for path, path_data in paths.items():
            valid_path_methods = {}
            if paths_white_list and path.lower() not in paths_white_list or path.lower() in paths_black_list:
                pass
            else:
                for path_method, method_data in path_data.items():
                    if path_method.lower() not in mask['operations_white_list']:
                        pass
                    else:
                        tags = set((tag.lower() for tag in method_data.get('tags', [])))
                        if tags_white_list:
                            if tags_white_list.intersection(tags):
                                if tags_black_list.intersection(tags):
                                    pass
                                else:
                                    valid_path_methods[path_method] = {'params':self._parse_params(method_data.get('parameters', [])), 
                                     'responses':method_data.get('responses', {})}
                            api_paths[path] = valid_path_methods
                        return api_paths

    @staticmethod
    @abstractmethod
    def _parse_params(params: dict) -> dict:
        raise NotImplementedError()
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/strategy/base_strategy.py
# Compiled at: 2020-05-07 07:40:51
# Size of source mod 2**32: 1700 bytes
"""Module: Base Strategy"""
from pathlib import Path
from typing import Set, Dict
from swagger2locustio.parsers.base_parser import SwaggerBaseParser
from swagger2locustio.parsers.swagger_v2 import SwaggerV2Parser
from swagger2locustio.parsers.swagger_v3 import SwaggerV3Parser
from swagger2locustio.generators.base_generator import BaseGenerator

class BaseStrategy:
    __doc__ = 'Class: Base Strategy'

    def __init__(self, file_content: dict, results_path: Path, mask: Dict[(str, Set[str])], strict_level: int):
        self.swagger_file_content = file_content
        self.mask = mask
        self.generator = BaseGenerator(results_path, strict_level)
        results_path.mkdir(exist_ok=True)

    def get_specific_version_parser(self) -> SwaggerBaseParser:
        """Method: get specific version parser"""
        swagger_version = self.swagger_file_content.get('swagger')
        openapi_version = self.swagger_file_content.get('openapi')
        version = swagger_version if swagger_version else openapi_version
        if not version:
            raise ValueError('No swagger version is specified')
        else:
            version = int(version[0])
            if version == 2:
                parser = SwaggerV2Parser()
            else:
                if version == 3:
                    parser = SwaggerV3Parser()
                else:
                    raise ValueError('There is no support for %s version of swagger' % version)
        return parser

    def process(self):
        """Method: process"""
        specific_version_parser = self.get_specific_version_parser()
        swagger_data = specific_version_parser.parse_swagger_file(self.swagger_file_content, self.mask)
        self.generator.generate_locustfiles(swagger_data)
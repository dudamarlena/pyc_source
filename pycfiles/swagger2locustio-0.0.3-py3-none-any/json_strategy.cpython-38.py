# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/strategy/json_strategy.py
# Compiled at: 2020-05-07 07:04:45
# Size of source mod 2**32: 1052 bytes
"""Module: JSON Strategy"""
import json
from swagger2locustio.strategy.base_strategy import BaseStrategy
from swagger2locustio.parsers.base_parser import SwaggerBaseParser
from swagger2locustio.parsers.json_parsers.swagger_v2 import SwaggerV2JsonParser

class JsonStrategy(BaseStrategy):
    __doc__ = 'Class: JSON Strategy'

    @staticmethod
    def read_file_content--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'file_name'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           32  'to 32'
                8  STORE_FAST               'file'

 L.  16        10  LOAD_GLOBAL              json
               12  LOAD_METHOD              load
               14  LOAD_FAST                'file'
               16  CALL_METHOD_1         1  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        6  '6'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20

    def get_specific_version_parser(self) -> SwaggerBaseParser:
        swagger_version = self.swagger_file_content.get'swagger'
        openapi_version = self.swagger_file_content.get'openapi'
        version = swagger_version if swagger_version else openapi_version
        if not version:
            raise ValueError('No swagger version is specified')
        else:
            version = int(version[0])
            if version == 2:
                parser = SwaggerV2JsonParser()
            else:
                raise ValueError('There is no support for %s version of swagger' % version)
        return parser
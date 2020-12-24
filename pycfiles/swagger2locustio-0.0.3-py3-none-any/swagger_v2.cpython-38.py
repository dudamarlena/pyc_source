# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/parsers/swagger_v2.py
# Compiled at: 2020-05-07 07:40:51
# Size of source mod 2**32: 722 bytes
"""Module: SwaggerV2 parser"""
from copy import deepcopy
from swagger2locustio.parsers.base_parser import SwaggerBaseParser

class SwaggerV2Parser(SwaggerBaseParser):
    __doc__ = 'Class: SwaggerV2 parser'

    @staticmethod
    def _parse_params(params: dict) -> dict:
        param_data = {}
        for param in params:
            param_name = param.get('name')
            if param_name:
                if param.get('in') or param.get('required'):
                    raise ValueError('Not full info about required param')
                else:
                    param_data[param_name] = deepcopy(param)
            return param_data
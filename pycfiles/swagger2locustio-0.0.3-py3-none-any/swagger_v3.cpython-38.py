# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/parsers/swagger_v3.py
# Compiled at: 2020-05-07 07:40:51
# Size of source mod 2**32: 277 bytes
"""Module: SwaggerV3 parser"""
from swagger2locustio.parsers.base_parser import SwaggerBaseParser

class SwaggerV3Parser(SwaggerBaseParser):
    __doc__ = 'Class: SwaggerV3 parser'

    @staticmethod
    def _parse_params(params: dict) -> dict:
        raise NotImplementedError()
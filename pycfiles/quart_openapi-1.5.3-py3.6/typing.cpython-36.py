# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quart_openapi/typing.py
# Compiled at: 2020-04-13 15:04:18
# Size of source mod 2**32: 681 bytes
"""typing.py

Provide type definitions for use in other modules
"""
from typing import Union, Tuple, Iterable, Dict, Any, Type
from jsonschema import Draft3Validator, Draft4Validator, Draft6Validator, Draft7Validator
PyTypes = Union[(Type[int], Type[float], Type[str], Type[bool])]
ValidatorType = Union[(PyTypes, str, Draft3Validator, Draft4Validator, Draft6Validator, Draft7Validator)]
ValidatorTypes = Union[(ValidatorType, Iterable['ValidatorType'])]
ExpectedDescList = Union[(ValidatorTypes, Tuple[ValidatorTypes], Tuple[(ValidatorTypes, str)],
 Tuple[(ValidatorTypes, str, Dict[(str, Any)])])]
HeaderType = Union[(ValidatorType, Iterable[PyTypes], Dict[(str, Any)])]
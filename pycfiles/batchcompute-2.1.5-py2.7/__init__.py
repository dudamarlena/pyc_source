# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/batchcompute/__init__.py
# Compiled at: 2019-12-23 21:36:39
"""A simple implementation for BatchCompute service SDK.
"""
__version__ = '2.1.5'
__all__ = [
 'Client', 'ClientError', 'FieldError', 'ValidationError', 'JsonError',
 'ConfigError', 'CN_QINGDAO', 'CN_HANGZHOU', 'CN_SHENZHEN', 'CN_BEIJING',
 'CN_ZHANGJIAKOU', 'CN_HUHEHAOTE', 'CN_SHANGHAI',
 'CN_HONGKONG', 'AP_SOUTHEAST_1', 'EU_CENTRAL_1', 'US_WEST_1', 'US_EAST_1']
__author__ = 'crisish'
from .client import Client
from .core import ClientError, FieldError, ValidationError, JsonError
from .utils import CN_QINGDAO, CN_SHENZHEN, CN_HANGZHOU, CN_BEIJING, CN_ZHANGJIAKOU, CN_HUHEHAOTE, CN_SHANGHAI, CN_HONGKONG, AP_SOUTHEAST_1, EU_CENTRAL_1, US_WEST_1, US_EAST_1, ConfigError
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/depo/__init__.py
# Compiled at: 2019-09-29 18:26:10
from .error import APIConnectionError, APIError, DepoError, PlaceUnavailableError
from .resource import Order, Place
from .utils import JSONEncoder
api_credentials = None
DEPO_API_ENDPOINT = 'https://admin.depo.sk/v2/api/'
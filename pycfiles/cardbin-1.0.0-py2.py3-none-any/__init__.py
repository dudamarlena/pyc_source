# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cardberg/__init__.py
# Compiled at: 2019-10-03 03:26:20
from .error import CardbergError, APIConnectionError, APIError
from .resource import Card
api_credentials = None
timeout = 30
CARDBERG_API_ENDPOINT = 'http://loys.cardberg.com/api/'
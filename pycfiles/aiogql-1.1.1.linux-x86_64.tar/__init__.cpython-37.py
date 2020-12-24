# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/aiogql/__init__.py
# Compiled at: 2020-01-21 09:02:42
# Size of source mod 2**32: 83 bytes
from .gql import gql
from .client import GQLClient
__all__ = ['gql', 'GQLClient']
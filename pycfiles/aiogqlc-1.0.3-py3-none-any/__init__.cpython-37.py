# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/aiogql/__init__.py
# Compiled at: 2020-01-21 09:02:42
# Size of source mod 2**32: 83 bytes
from .gql import gql
from .client import GQLClient
__all__ = ['gql', 'GQLClient']
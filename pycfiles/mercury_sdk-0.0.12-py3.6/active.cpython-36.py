# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/http/active.py
# Compiled at: 2018-01-17 16:29:11
# Size of source mod 2**32: 141 bytes
from mercury_sdk.http.query import QueryInterfaceBase

class ActiveComputers(QueryInterfaceBase):
    SERVICE_URI = 'api/active/computers'
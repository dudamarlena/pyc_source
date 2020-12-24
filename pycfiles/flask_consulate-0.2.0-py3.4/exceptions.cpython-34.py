# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_consulate/exceptions.py
# Compiled at: 2017-04-16 13:46:21
# Size of source mod 2**32: 189 bytes
from requests.exceptions import ConnectionError

class ConsulConnectionError(ConnectionError):
    __doc__ = '\n    A connection error related to Consul happened.\n    '
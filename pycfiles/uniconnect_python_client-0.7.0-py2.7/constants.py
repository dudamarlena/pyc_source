# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/uniconnect/constants.py
# Compiled at: 2019-08-27 00:58:09
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typing import Any, Optional, Text
DEFAULT_PORT = 8080
DEFAULT_SOURCE = 'uniconnect-python-client'
DEFAULT_CATALOG = None
DEFAULT_SCHEMA = None
DEFAULT_AUTH = None
DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_REQUEST_TIMEOUT = 30.0
HTTP = 'http'
HTTPS = 'https'
URL_STATEMENT_PATH = '/v1/statement'
HEADER_PREFIX = 'X-uniconnect-'
HEADER_CATALOG = HEADER_PREFIX + 'Catalog'
HEADER_SCHEMA = HEADER_PREFIX + 'Schema'
HEADER_SOURCE = HEADER_PREFIX + 'Source'
HEADER_USER = HEADER_PREFIX + 'User'
HEADER_SESSION = HEADER_PREFIX + 'Session'
HEADER_SET_SESSION = HEADER_PREFIX + 'Set-Session'
HEADER_CLEAR_SESSION = HEADER_PREFIX + 'Clear-Session'
HEADER_STARTED_TRANSACTION = HEADER_PREFIX + 'Started-Transaction-Id'
HEADER_TRANSACTION = HEADER_PREFIX + 'Transaction-Id'
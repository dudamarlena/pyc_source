# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/examples/api_settings.py
# Compiled at: 2013-08-11 10:36:51
from pyws.protocols import RestProtocol, JsonProtocol
from authenticate import authenticate, soap_headers_schema
DEBUG = True
PROTOCOLS = (
 RestProtocol(),
 JsonProtocol())
SOAP_PROTOCOL_PARAMS = (
 'Test',
 'http://example.com/',
 'http://localhost:8000/api/soap',
 soap_headers_schema)
CREATE_CONTEXT = authenticate
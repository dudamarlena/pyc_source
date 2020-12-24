# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/examples/server.py
# Compiled at: 2013-08-11 10:36:51
from pyws.server import SoapServer
import api_settings
server = SoapServer(api_settings, *api_settings.SOAP_PROTOCOL_PARAMS)
import functions
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/common_dibbs/misc.py
# Compiled at: 2016-10-06 08:41:39
import base64

def configure_basic_authentication(swagger_client, username, password):
    authentication_string = '%s:%s' % (username, password)
    base64_authentication_string = base64.b64encode(bytes(authentication_string))
    header_key = 'Authorization'
    header_value = 'Basic %s' % (base64_authentication_string,)
    swagger_client.api_client.default_headers[header_key] = header_value
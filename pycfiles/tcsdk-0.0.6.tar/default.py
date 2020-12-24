# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/workspace/workspace/tcsdk_deploy/tcsdk/tcsdk/common/default.py
# Compiled at: 2019-12-26 02:59:48
import logging, platform

def get(value, default_value):
    if value is None:
        return default_value
    else:
        return value
        return


connect_timeout = 60
request_retries = 3
http_session_size = 10
USER_AGENT = ('tcsdk-python/{}/{}/{}/{}').format(platform.system(), platform.release(), platform.machine(), platform.python_version())
REQUEST_ID = 'x-tcsdk-request-id'
CODE = 'code'
MESSAGE = 'message'
HEADER_SDK_VERSION = 'sdk_version'
NAME = 'tcsdk'
LOGGER_LEVEL = logging.DEBUG
CLIENT_ERROR = 1000
SERVER_ERROR = 1001
REQUEST_ERROR = 1002
ENDPOINT_TYPE_IP = 2001
ENDPOINT_TYPE_CNAME = 2002
MAIN_VERSION = 0
SUB_VERSION = 0
FIX_VERSION = 6
TCSDK_VERSION = ('{}.{}.{}').format(MAIN_VERSION, SUB_VERSION, FIX_VERSION)
GET_METHOD = 'get'
POST_METHOD = 'post'
DELETE_METHOD = 'put'
PUT_METHOD = 'put'
TCSDK_LOGO = ('\n_____  ___     \n  |   /       \n  |   \\ __ loud \n<<<<<{}.{}.{}>>>>> \n').format(MAIN_VERSION, SUB_VERSION, FIX_VERSION)
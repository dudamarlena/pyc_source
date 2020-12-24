# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\settings.py
# Compiled at: 2018-05-11 07:11:27
# Size of source mod 2**32: 555 bytes
from .utils import build_user_agent
DEFAULT_HEADERS = {'User-Agent': build_user_agent()}
TIMEOUT = 1
ENCODING = 'utf-8'
RETRYS = 3
RETRY_BACKOFF_FACTOR = 0.1
RETRY_STATUS_FORCELIST = frozenset([500, 502, 504])
OAUTH_HOST = 'open.weixin.qq.com'
AUTH_EXPIRED_CODES = frozenset([40014, 41001, 42001])
TRADE_TYPE_JSAPI = 'JSAPI'
TRADE_TYPE_NATIVE = 'NATIVE'
TRADE_TYPE_APP = 'APP'
SIGN_TYPE = 'MD5'
SIGN_NONCE_STR_LEN = 32
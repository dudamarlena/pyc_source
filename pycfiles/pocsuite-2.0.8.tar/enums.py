# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/enums.py
# Compiled at: 2018-11-28 03:20:09
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

class CUSTOM_LOGGING:
    SYSINFO = 9
    SUCCESS = 8
    ERROR = 7
    WARNING = 6


class OUTPUT_STATUS:
    SUCCESS = 1
    FAILED = 0


class HTTP_HEADER:
    ACCEPT = 'Accept'
    ACCEPT_CHARSET = 'Accept-Charset'
    ACCEPT_ENCODING = 'Accept-Encoding'
    ACCEPT_LANGUAGE = 'Accept-Language'
    AUTHORIZATION = 'Authorization'
    CACHE_CONTROL = 'Cache-Control'
    CONNECTION = 'Connection'
    CONTENT_ENCODING = 'Content-Encoding'
    CONTENT_LENGTH = 'Content-Length'
    CONTENT_RANGE = 'Content-Range'
    CONTENT_TYPE = 'Content-Type'
    COOKIE = 'Cookie'
    SET_COOKIE = 'Set-Cookie'
    HOST = 'Host'
    LOCATION = 'Location'
    PRAGMA = 'Pragma'
    PROXY_AUTHORIZATION = 'Proxy-Authorization'
    PROXY_CONNECTION = 'Proxy-Connection'
    RANGE = 'Range'
    REFERER = 'Referer'
    SERVER = 'Server'
    USER_AGENT = 'User-Agent'
    TRANSFER_ENCODING = 'Transfer-Encoding'
    URI = 'URI'
    VIA = 'Via'


class PROXY_TYPE:
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    SOCKS4 = 'SOCKS4'
    SOCKS5 = 'SOCKS5'


class ERROR_TYPE_ID:
    NOTIMPLEMENTEDERROR = 2
    CONNECTIONERROR = 3.0
    HTTPERROR = 3.1
    CONNECTTIMEOUT = 3.2
    TOOMANYREDIRECTS = 3.3
    OTHER = 4
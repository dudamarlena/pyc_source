# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\curl_http\test.py
# Compiled at: 2018-06-09 05:28:00
# Size of source mod 2**32: 820 bytes
from curl_http import HTTP
http = HTTP()
http.set_header('Host', 'it592.com')
http.set_timeout(10)
http.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36')
http.set_proxy('114.212.12.4', '31228')
http.set_cookie('name', 'DoubleL')
http.set_foreign_ip('0.0.0.0')
http.request('www.baidu.com', referer='')
http.request('www.baidu.com', {'name': 123}, referer='')
http.get_header(key='')
http.get_code()
http.get_cookie(key='')
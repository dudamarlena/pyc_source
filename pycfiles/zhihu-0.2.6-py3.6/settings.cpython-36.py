# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zhihu\settings.py
# Compiled at: 2017-07-26 04:49:41
# Size of source mod 2**32: 604 bytes
import os.path
user_agent_list = [
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36']
USER_AGENT = user_agent_list[0]
HEADERS = {'Host':'www.zhihu.com', 
 'Referer':'https://www.zhihu.com/', 
 'User-Agent':USER_AGENT}
ZHUANLAN_HEADERS = {'Host':'zhuanlan.zhihu.com', 
 'Referer':'https://zhuanlan.zhihu.com/', 
 'User-Agent':USER_AGENT}
COOKIES_FILE = os.path.join(os.path.expanduser('~'), 'cookies.txt')
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\m3u8Helper.py
# Compiled at: 2019-08-30 12:41:18
# Size of source mod 2**32: 804 bytes
"""
@File    :   m3u8Helper.py
@Time    :   2019/08/23
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""
import re
from aigpy import netHelper

def getM3u8TsUrls(url):
    content = netHelper.downloadString(url, None)
    pattern = re.compile('(?<=http).+?(?=\\\\n)')
    plist = pattern.findall(str(content))
    urllist = []
    for item in plist:
        urllist.append('http' + item)

    return urllist
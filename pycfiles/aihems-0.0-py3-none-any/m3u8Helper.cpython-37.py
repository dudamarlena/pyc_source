# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\m3u8Helper.py
# Compiled at: 2019-08-30 12:41:18
# Size of source mod 2**32: 804 bytes
__doc__ = '\n@File    :   m3u8Helper.py\n@Time    :   2019/08/23\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
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
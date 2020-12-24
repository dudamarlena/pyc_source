# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ThunderParser/parser_qqdl.py
# Compiled at: 2016-03-13 23:38:38
"""
  Author:  fly --<yafeile@sohu.com>
  Purpose: 
  Created: Monday, March 14, 2016
"""
import base64

def parser(url):
    u"""解析QQ旋风下载地址"""
    try:
        url = base64.b64decode(url)
        return url
    except TypeError:
        return 'The Given URL is unvalid'


if __name__ == '__main__':
    unittest.main()
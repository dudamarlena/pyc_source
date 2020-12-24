# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ThunderParser/__init__.py
# Compiled at: 2016-03-14 00:50:14
"""
  Author:  fly --<yafeile@sohu.com>
  Purpose: 
  Created: Monday, March 14, 2016
"""

def parser(url):
    u"""解析迅雷或QQ旋风下载链接"""
    protocol, url = url.split('://')
    length = len(url)
    d, c = divmod(length, 4)
    if c > 0:
        url = url + (4 - c) * '='
    protocol = protocol.lower()
    if protocol == 'thunder':
        import parser_thunder as thunder
        return thunder._parser(url)
    else:
        if protocol == 'qqdl':
            import parser_qqdl as qqdl
            return qqdl.parser(url)
        if protocol == 'flashget':
            import parser_flashget as flashget
            return flashget.parser(url)
        return NotImplemented
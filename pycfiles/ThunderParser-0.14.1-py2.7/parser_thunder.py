# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ThunderParser/parser_thunder.py
# Compiled at: 2016-03-14 00:55:43
"""
Created on Tue Aug 18 23:23:24 2015

@author: fly
"""
import base64

def _parser(url):
    u"""解析迅雷下载链接"""
    try:
        url = base64.b64decode(url)
        url = url[2:-2]
        return url
    except TypeError:
        return 'The Given URL is unvalid'


def parser(url):
    u"""兼容0.14.1之前版本的下载链接"""
    protocol, url = url.split('://')
    length = len(url)
    d, c = divmod(length, 4)
    if c > 0:
        url = url + (4 - c) * '='
    protocol = protocol.lower()
    if protocol == 'thunder':
        _parser(url)
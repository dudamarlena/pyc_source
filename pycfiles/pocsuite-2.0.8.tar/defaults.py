# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/defaults.py
# Compiled at: 2018-11-28 03:20:09
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
from pocsuite.lib.core.datatype import AttribDict
defaults = {'threads': 1, 
   'timeout': 10}
HTTP_DEFAULT_HEADER = {'Accept': '*/*', 
   'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3', 
   'Accept-Language': 'zh-CN,zh;q=0.8', 
   'Cache-Control': 'max-age=0', 
   'Connection': 'keep-alive', 
   'Referer': 'http://www.baidu.com', 
   'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'}
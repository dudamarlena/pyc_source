# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/defaults.py
# Compiled at: 2018-11-28 03:20:09
__doc__ = "\nCopyright (c) 2014-2016 pocsuite developers (https://seebug.org)\nSee the file 'docs/COPYING' for copying permission\n"
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
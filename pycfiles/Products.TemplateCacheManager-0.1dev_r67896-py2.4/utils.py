# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/TemplateCacheManager/Extensions/utils.py
# Compiled at: 2008-07-03 18:43:12
from md5 import md5

def md5_hexdigest(self, s):
    """returns hexdigest of md5 sum"""
    return md5(str(s)).hexdigest()
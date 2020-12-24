# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/py56/video/VideoCustom.py
# Compiled at: 2014-10-30 02:57:25
from py56 import ApiAbstract

class VideoCustom(ApiAbstract):
    """
    params: sid css rurl ourl
    """

    def get(self, **kwargs):
        url = '%s%s' % (self.domain, '/video/custom.plugin')
        return '%s?%s' % (url, self.signRequest(**kwargs))
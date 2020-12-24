# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/py56/user/App2Videos.py
# Compiled at: 2014-11-24 23:17:23
from py56 import ApiAbstract

class UserApp2Videos(ApiAbstract):

    def get(self, **kwargs):
        u"""
        @description 获取当前应用上传视频列表(新)
        @param page->页码，rows->每页显示多少
        @link  /user/app2Videos.json
        @return json
        """
        url = '%s%s' % (self.domain, '/user/app2Videos.json')
        return self.getHttp(url, **kwargs)
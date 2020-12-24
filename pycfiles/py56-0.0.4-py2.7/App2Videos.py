# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
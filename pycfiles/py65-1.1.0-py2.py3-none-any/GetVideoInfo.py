# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/py56/video/GetVideoInfo.py
# Compiled at: 2014-11-25 01:08:57
from py56 import ApiAbstract

class VideoGetVideoInfo(ApiAbstract):
    """
    Video_GetVideoInfo

    @uses ApiAbstract
    @package
    @author Allan <email:alnsun.cn@gmail.com>
    """

    def get(self, **kwargs):
        u"""
        @description 获取视频信息

          $params=array('vid'=>$flvid);
        @param $flvid 56视频的flvid
        @link /video/getVideoInfo.json
        @return json
        """
        url = '%s%s' % (self.domain, '/video/getVideoInfo.json')
        return self.getHttp(url, **kwargs)
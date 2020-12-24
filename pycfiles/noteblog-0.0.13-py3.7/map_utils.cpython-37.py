# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/map_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 987 bytes
"""
@author = super_fazai
@File    : map_utils.py
@connect : superonesfazai@gmail.com
"""
from .internet_utils import get_base_headers
from .common_utils import json_2_dict
from .aio_utils import unblock_request
__all__ = [
 'async_get_location_info_by_lng_and_lat']

async def async_get_location_info_by_lng_and_lat(baidu_api_key: str, lng: float, lat: float) -> dict:
    """
    异步通过经纬度在百度地图api中获取定位信息(得设置ip白名单)
    :param baidu_api_key:
    :param lng:
    :param lat:
    :return:
    """
    url = 'http://api.map.baidu.com/geocoder'
    params = (
     (
      'location', '{},{}'.format(lat, lng)),
     ('output', 'json'),
     (
      'key', baidu_api_key))
    return json_2_dict(json_str=(await unblock_request(url=url, headers=(get_base_headers()), params=params)),
      default_res={})
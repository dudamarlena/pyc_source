# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/spider/app_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 3554 bytes
"""
@author = super_fazai
@File    : app_utils.py
@connect : superonesfazai@gmail.com
"""
from gc import collect
from asyncio import get_event_loop
from pprint import pprint
from ..common_utils import _print
from spider.async_always import async_sleep
__all__ = [
 'u2_page_back',
 'u2_get_device_display_h_and_w',
 'u2_get_some_ele_height',
 'u2_up_swipe_some_height',
 'async_get_u2_ele_info',
 'get_mitm_flow_request_headers_user_agent']

async def u2_page_back(d, back_num=1):
    """
    u2的页面返回
    :param d: eg: u2 d
    :param back_num:
    :return:
    """
    while back_num > 0:
        d.press('back')
        back_num -= 1
        await async_sleep(0.3)


async def u2_get_device_display_h_and_w(d) -> tuple:
    """
    u2获取设备的高跟宽
    :param d: eg: u2 d
    :return:
    """
    device_height = d.device_info.get('display', {}).get('height')
    device_width = d.device_info.get('display', {}).get('width')
    return (
     device_height, device_width)


async def u2_get_some_ele_height(ele):
    """
    u2得到某一个ele块的height
    :param ele: eg: d(resourceId="com.taobao.taobao:id/topLayout")
    :return:
    """
    return ele.info.get('bounds', {}).get('bottom') - ele.info.get('bounds', {}).get('top')


async def u2_up_swipe_some_height(d, swipe_height, base_height=0.1) -> None:
    """
    u2 上滑某个高度
    :param d:
    :param height:
    :param base_height:
    :return:
    """
    d.swipe(0.0, base_height + swipe_height, 0.0, base_height)


async def async_get_u2_ele_info(ele, logger=None) -> tuple:
    """
    异步获取ele 的info
    :param ele: UiObject [from uiautomator2.session import UiObject]
    :return: (ele, ele_info)
    """

    async def _get_args():
        """获取args"""
        return [
         ele]

    def _get_ele_info(ele) -> dict:
        return ele.info

    loop = get_event_loop()
    args = await _get_args()
    ele_info = {}
    try:
        try:
            ele_info = await (loop.run_in_executor)(None, _get_ele_info, *args)
        except Exception as e:
            try:
                _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
            finally:
                e = None
                del e

    finally:
        return

    try:
        del loop
    except:
        pass

    _print(msg=('[{}] ele: {}'.format('+' if ele_info != {} else '-', ele)),
      logger=logger)
    collect()
    return (
     ele, ele_info)


def get_mitm_flow_request_headers_user_agent(headers, logger=None) -> str:
    """
    获取flow.request.headers的user_agent
    :param headers: flow.request.headers obj
    :return:
    """
    user_agent = ''
    try:
        headers = dict(headers)
        for key, value in headers.items():
            if key == 'user-agent':
                user_agent = value
                break
            continue

        assert user_agent != '', 'user_agent不为空str!'
    except Exception as e:
        try:
            _print(msg='遇到错误',
              logger=logger,
              exception=e,
              log_level=2)
        finally:
            e = None
            del e

    return user_agent
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ojcrawler/utils.py
# Compiled at: 2018-12-29 10:55:16
from __future__ import absolute_import, division, print_function
from ojcrawler.crawlers.config import *
from ojcrawler.crawlers import supports
from time import sleep
import json

def sample_sync_func(data, *args, **kwargs):
    json_data = json.dumps(data)
    print(args, kwargs)
    logger.info('data: ' + json_data)


def sample_save_image(image_url, oj_name):
    print(oj_name, image_url)
    return image_url


def submit_code(oj_name, handle, password, image_func, sync_func, source, lang, pid, *args, **kwargs):
    u"""
    提交代码核心函数
    :param oj_name:     OJ名，需要在support oj list中
    :param handle:      对应oj的用户名
    :param password:    对应oj的密码
    :param image_func:  图片保存函数，参考sample_save_image
    :param sync_func:   状态同步函数，参考sample_sync_func
    :param source:      源代码
    :param lang:        语言
    :param pid:         题目题号
    :param args:        传入状态同步函数的参数
    :param kwargs:      传入状态同步函数的参数
    :return:
    """
    oj = supports[oj_name](handle, password, image_func)
    success, dat = oj.submit_code(source, lang, pid)

    def sync(data):
        return sync_func(data, *args, **kwargs)

    if not success:
        logger.warning(('{} - {}').format(oj.oj_name, dat))
        sync({'status': 'submit failed', 'established': True})
        return (
         False, dat)
    sync({'status': 'submitted', 'established': False})
    pre_status = 'submitted'
    cnt = 0
    fetch_success = False
    while cnt < RESULT_COUNT:
        sleep(RESULT_INTERVAL)
        success, info = oj.get_result_by_rid(dat)
        if success:
            status = info['status']
            if status != pre_status:
                established = True
                for uncertain_status in oj.uncertain_result_status:
                    if uncertain_status in str(status).lower():
                        established = False

                info['established'] = established
                sync(info)
                pre_status = status
                if established:
                    fetch_success = True
                    break
        cnt = cnt + 1

    if not fetch_success:
        sync({'status': 'fetch failed', 'established': False})
        return (
         False, '获取运行结果失败')
    return (
     True, '')
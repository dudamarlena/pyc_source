# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/data/excel_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 2356 bytes
"""
@author = super_fazai
@File    : excel_utils.py
@Time    : 2016/7/24 11:28
@connect : superonesfazai@gmail.com
"""
from pprint import pprint
from pyexcel import iget_records
from os.path import exists
from asyncio import get_event_loop
from gc import collect
from time import time
from ..common_utils import _print
__all__ = [
 'read_info_from_excel_file',
 'async_read_info_from_excel_file']

def read_info_from_excel_file(excel_file_path) -> list:
    """
    本地从excel中读取文件并以list格式返回
    :param excel_file_path:
    :return: a list eg: [{'关键词': '连衣裙', '一级类目': '女装/女士精品', '二级类目': '连衣裙', '三级类目': ''}, ...]
    """
    result = []
    if not exists(excel_file_path):
        raise FileExistsError('在该excel的路径未找到待处理文件, 请检查!')
    else:
        data = iget_records(file_name=excel_file_path)
        added_excel_row_num = 1
        s_time = time()
        for index, row in enumerate(data):
            row = dict(row)
            result.append(row)
            print(('\r--->>> added_excel_row_num: {}'.format(added_excel_row_num)), end='', flush=True)
            added_excel_row_num += 1

        time_consume = time() - s_time
        print('\n执行完毕! 此次耗时 {} s!'.format(round(float(time_consume), 3)))
    return result


async def async_read_info_from_excel_file(excel_file_path: str, logger=None) -> list:
    """
    异步读取excel file
    :param excel_file_path:
    :return:
    """

    async def get_args():
        return [
         excel_file_path]

    loop = get_event_loop()
    args = await get_args()
    res = []
    try:
        try:
            res = await (loop.run_in_executor)(None, read_info_from_excel_file, *args)
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

    collect()
    return res
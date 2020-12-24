# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/data/list_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 2050 bytes
"""
@author = super_fazai
@File    : list_utils.py
@Time    : 2016/8/4 11:46
@connect : superonesfazai@gmail.com
"""
__all__ = [
 'unique_list_and_keep_original_order',
 'list_remove_repeat_dict',
 'list_remove_repeat_dict_plus']

def unique_list_and_keep_original_order(target_list, key=None):
    """
    从列表中删除重复的元素, 同时保留其原始顺序
    :param target_list: 待处理的list
    :param key: 是一个函数，它接受一个参数并返回一个 key 来测试唯一性
    :return:
    """
    key = key or (lambda x: x)
    seen = set()
    unique_list = []
    for value in target_list:
        unique_value = key(value)
        if unique_value in seen:
            continue
        seen.add(unique_value)
        unique_list.append(value)

    return unique_list


def list_remove_repeat_dict(target: list, repeat_key: str) -> list:
    """
    list 子元素为dict的去重
    :param target: 目标list
    :param repeat_key: dict指定唯一去重检测key
    :return:
    """
    repeat_key_list = [i.get(repeat_key) for i in target]
    res = []
    for i in target:
        count = repeat_key_list.count(i.get(repeat_key))
        if count <= 1:
            res.append(i)
            continue

    return res


def list_remove_repeat_dict_plus(target: list, repeat_key: str) -> list:
    """
    list 子元素为dict的去重plus
    :param target: 目标list
    :param repeat_key: dict指定唯一去重检测key
    :return:
    """
    tmp_list = []
    res_list = []
    for item in target:
        repeat_key_value = item.get(repeat_key)
        if repeat_key_value is not None and repeat_key_value not in tmp_list:
            res_list.append(item)
            tmp_list.append(repeat_key_value)

    return res_list
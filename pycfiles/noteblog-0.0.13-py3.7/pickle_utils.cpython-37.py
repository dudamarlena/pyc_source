# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/data/pickle_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 946 bytes
"""
pickle 对象utils
"""
from pickle import loads
from ..common_utils import _print
__all__ = [
 'deserializate_pickle_object',
 'serialize_obj_item_2_dict']

def deserializate_pickle_object(pickle_object, logger=None, default_res=None):
    """
    反序列化pickle对象(python对象)
    :param pickle_object:
    :param default_res: 出错默认返回值
    :return:
    """
    _ = {} if default_res is None else default_res
    try:
        _ = loads(pickle_object)
    except Exception as e:
        try:
            _print(msg='反序列化pickle对象出错!', logger=logger, log_level=2, exception=e)
        finally:
            e = None
            del e

    return _


def serialize_obj_item_2_dict(target) -> list:
    """
    将序列化对象的子对象强转为dict类型
    :param target:
    :return:
    """
    return [dict(item) for item in target]
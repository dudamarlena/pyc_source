# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/json_util.py
# Compiled at: 2019-12-18 04:05:51
# Size of source mod 2**32: 2164 bytes
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : json_util.py
@Desc    : json序列化工具类
"""
import os, json, numpy as np
from wmpy_util.time_util import timer

def json_dump_file(file, data, minify=False):
    prefix, ext = os.path.splitext(file)
    if ext == '':
        ext = '.json'
    file = prefix + ext
    with open(file, 'w', encoding='utf-8') as (f):
        json.dump(data, f, ensure_ascii=False, indent=4)
    if minify:
        file = '%s.min%s' % (prefix, ext)
        with open(file, 'w', encoding='utf-8') as (f):
            json.dump(data, f, ensure_ascii=False)
    return file


def minify_json_file(from_file, to_file):
    """
    压缩某个json文件
    :param from_file:
    :param to_file:
    :return:
    """
    with open(from_file, 'r', encoding='utf-8') as (f):
        datas = json.load(f)
        json_dump_file(to_file, datas, minify=True)


def read_json_file(file_path):
    if not os.path.isfile(file_path):
        raise IOError('File not existed! %s' % file_path)
    result = None
    with open(file_path, 'r', encoding='utf-8') as (f):
        result = json.load(f)
    return result


def json_power_dump(obj):
    """
    处理numpy无法序列化的问题
    :param obj:
    :return:
    """
    return json.dumps(obj, cls=NumpyEncoder, ensure_ascii=False)


def get_dict_type(dict_obj: dict):
    key, value = next(dict_obj.items().__iter__())
    return (type(key), type(value))


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            if isinstance(obj, np.core.floating):
                return float(obj)
            else:
                if isinstance(obj, np.core.signedinteger):
                    return int(obj)
                if isinstance(obj, np.core.unsignedinteger):
                    return int(obj)
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    a = dict((i, 2 * i) for i in range(1000000))
    for i in range(1000000):
        get_dict_type(a)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/path_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 858 bytes
"""
提供处理路径的工具
"""
import os
from contextlib import contextmanager
from os.path import split, splitext
__all__ = [
 'cd',
 'from_file_path_get_file_extension_name']

@contextmanager
def cd(path):
    """
    进入到给定目录的上下文管理器
        用法: eg:
            with cd('/Users/afa'):
                print(True)
    :param path: 绝对路径
    :return:
    """
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)


def from_file_path_get_file_extension_name(file_path) -> str:
    """
    从文件路径得到该文件的扩展名
    :param file_path:
    :return:
    """
    return splitext(split(file_path)[(-1)])[(-1)].replace('.', '')
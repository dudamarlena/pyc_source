# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/max/tools/filetools.py
# Compiled at: 2018-12-05 10:30:38
"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 常用操作类
"""
import os, re, time, subprocess, sys
sys.path.append('..')
from loggers import JFMlogging
logger = JFMlogging().getloger()

def write_file(filename, content, is_cover=False):
    u"""
    写入文件 覆盖写入
    :param filename:
    :param content:
    :param is_cover:是否覆盖写入
    :return:
    """
    try:
        newstr = ''
        if isinstance(content, list or tuple):
            for str in content:
                newstr = newstr + str + '\n'

        else:
            newstr = content
        if is_cover == True:
            file_mode = 'wb'
        else:
            file_mode = 'ab'
        with open(filename, file_mode) as (f_w):
            f_w.write(newstr)
            logger.info(('写{}文件完成').format(filename))
    except Exception as e:
        logger.info(('{}写入异常!{}').format(filename, e))


def del_files(filename):
    u"""
    删除文件
    :param filename:
    :return:
    """
    try:
        if os.path.exists(filename):
            subprocess.call(('rm -rf {}').format(filename), shell=True)
            logger.info(('删除{}完成!').format(filename))
    except Exception as e:
        logger.info(('删除{}异常!{}').format(filename, e))


def mk_dir(foldername):
    u"""
    创建文件目录
    :return:
    """
    try:
        if not os.path.exists(foldername):
            subprocess.call(('mkdir {}').format(foldername), shell=True)
            logger.info(('创建{}完成!').format(foldername))
    except Exception as e:
        logger.info(('创建{}异常!').format(foldername, e))


def read_file(filename):
    u"""
    读取文件
    :return:
    """
    result = ''
    try:
        try:
            with open(filename, 'r') as (f_r):
                result = f_r.readlines()
        except Exception as e:
            logger.info(('{}读取异常!{}').format(e))

    finally:
        if isinstance(result, list) and len(result) == 1:
            return result[0]
        else:
            return result
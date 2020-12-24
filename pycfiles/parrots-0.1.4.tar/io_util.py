# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/parrots/parrots/utils/io_util.py
# Compiled at: 2018-08-27 01:11:12
import logging, os, pickle

def get_logger(name, log_file=None):
    u"""
    logger
    :param name: 模块名称
    :param log_file: 日志文件，如无则输出到标准输出
    :return:
    """
    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if not log_file:
        handle = logging.StreamHandler()
    else:
        handle = logging.FileHandler(log_file)
    handle.setFormatter(format)
    logger = logging.getLogger(name)
    logger.addHandler(handle)
    logger.setLevel(logging.DEBUG)
    return logger


def load_pkl(pkl_path):
    u"""
    加载词典文件
    :param pkl_path:
    :return:
    """
    with open(pkl_path, 'rb') as (f):
        result = pickle.load(f)
    return result


def dump_pkl(vocab, pkl_path, overwrite=True):
    u"""
    存储文件
    :param pkl_path:
    :param overwrite:
    :return:
    """
    if os.path.exists(pkl_path) and not overwrite:
        return
    with open(pkl_path, 'wb') as (f):
        pickle.dump(vocab, f, protocol=0)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sr/logger.py
# Compiled at: 2019-03-17 10:26:41
import logging, os, time
from logzero import setup_logger
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
logger_folder = os.path.join(root_path, 'logger')

def get_current_time():
    u"""
    获取当前时间戳
    :return:
    """
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return current_time


def init_logger():
    u"""
    初始化日志
    :return:
    """
    if not os.path.exists(logger_folder):
        os.mkdir(logger_folder)
    logger_file = os.path.join(logger_folder, 'logger.log')
    logger = setup_logger(name='logger', logfile=logger_file, level=logging.INFO)
    return logger
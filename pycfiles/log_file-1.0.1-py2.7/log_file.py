# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\log_file\log_file.py
# Compiled at: 2018-11-20 19:46:18
"""
工程中我们使用一个名字为config.py的Python模块用来保存全局的配置，
由于logging在工程中每个源代码文件都可能用到，
因此我们把logging模块在config.py中生成一个实例，
这样其它模块只需要引用这个实例就可以了。
在其它模块中，我们使用这样的语句引用logger对象：
# from config import logger
"""
import logging, logging.config, os

def logger():
    path = os.getcwd() + '\\Log'
    if not os.path.exists(path):
        os.mkdir(path)
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('cisdi')
    return logger
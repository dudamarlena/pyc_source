# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/max/Desktop/workspace/CGEA/app/CGEA/lib/CGEA_fxn/lib/log.py
# Compiled at: 2016-01-15 11:13:25
import logging

def slogger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', '%d-%m-%Y %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def logger(name, basepath):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', '%d-%m-%Y %H:%M:%S')
    hfile_info = logging.FileHandler(basepath + 'info.log')
    hfile_info.setFormatter(formatter)
    hfile_info.setLevel(logging.INFO)
    log.addHandler(hfile_info)
    hfile_error = logging.FileHandler(basepath + 'error.log')
    hfile_error.setFormatter(formatter)
    hfile_error.setLevel(logging.ERROR)
    log.addHandler(hfile_error)
    hfile_debug = logging.FileHandler(basepath + 'debug.log')
    hfile_debug.setFormatter(formatter)
    hfile_debug.setLevel(logging.DEBUG)
    log.addHandler(hfile_debug)
    return log
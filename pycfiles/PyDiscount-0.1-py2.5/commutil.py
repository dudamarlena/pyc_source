# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\disc\commutil.py
# Compiled at: 2009-04-16 05:06:14
"""
Created on 2009-4-16

@author: mingqi
"""
import logging, sys

def get_logger(name):
    logger = logging.getLogger(name)
    hdlr = logging.StreamHandler(sys.stdout)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger
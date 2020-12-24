# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\disc\commutil.py
# Compiled at: 2009-04-16 05:06:14
__doc__ = '\nCreated on 2009-4-16\n\n@author: mingqi\n'
import logging, sys

def get_logger(name):
    logger = logging.getLogger(name)
    hdlr = logging.StreamHandler(sys.stdout)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger
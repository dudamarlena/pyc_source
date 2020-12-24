# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/djangopypi/utils.py
# Compiled at: 2015-10-27 08:49:00
import logging

def debug(func):

    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.exception('@debug')

    return _wrapped
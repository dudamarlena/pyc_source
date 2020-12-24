# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/uniconnect/logging.py
# Compiled at: 2019-08-27 00:56:48
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import logging
LEVEL = logging.INFO

def get_logger(name, log_level=LEVEL):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/core/mod_log.py
# Compiled at: 2019-03-16 08:33:40
# Size of source mod 2**32: 989 bytes
"""
# File: mod_log.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: log module
"""
from os.path import sep as SEP
import logging, inspect
from basico.core.mod_env import FILE

def get_logger(name):
    """Returns a new logger with personalized.
    @param name: logger name
    """
    logging.basicConfig(level=(logging.DEBUG), format='%(levelname)7s | %(lineno)4d  |%(name)-25s | %(asctime)s | %(message)s')
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)7s | %(lineno)4d  |%(name)-25s | %(asctime)s | %(message)s')
    fh = logging.FileHandler(FILE['LOG'])
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s | %(message)s')
    fe = logging.FileHandler(FILE['EVENTS'])
    fe.setFormatter(formatter)
    fe.setLevel(logging.INFO)
    log.addHandler(fe)
    return log
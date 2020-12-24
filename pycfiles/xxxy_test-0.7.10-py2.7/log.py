# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/log.py
# Compiled at: 2018-12-27 05:19:41
import logging
logger = logging.getLogger('russell')

def configure_logger(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(message)s', level=log_level)
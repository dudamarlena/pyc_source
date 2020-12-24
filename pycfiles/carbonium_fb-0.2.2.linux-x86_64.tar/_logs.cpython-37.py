# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/_logs.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 339 bytes
"""This module configures logging for Carbonium"""
import logging
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')
log = logging.getLogger('carbonium')
log.setLevel(logging.DEBUG)
_fblog = logging.getLogger('client')
_fblog.setLevel(logging.WARNING)
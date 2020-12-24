# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\RssReader\logger.py
# Compiled at: 2019-12-13 10:00:28
# Size of source mod 2**32: 222 bytes
"""logger redefinition"""
import logging
logging.basicConfig(filename='sample.log', level=(logging.INFO), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger()
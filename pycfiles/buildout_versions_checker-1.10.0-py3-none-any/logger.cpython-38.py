# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/logger.py
# Compiled at: 2020-03-06 05:24:58
# Size of source mod 2**32: 127 bytes
"""Logger for Buildout Versions Checker"""
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
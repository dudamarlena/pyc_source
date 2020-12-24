# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/logger.py
# Compiled at: 2020-03-06 05:24:58
# Size of source mod 2**32: 127 bytes
__doc__ = 'Logger for Buildout Versions Checker'
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/clue/bzrserver/utils.py
# Compiled at: 2009-03-01 11:10:34
import logging
logger = logging.getLogger('clue.bzrserver')
logger.setLevel(level=logging.INFO)
security_logger = logging.getLogger('clue.bzrserver.security')
security_logger.setLevel(level=logging.WARNING)
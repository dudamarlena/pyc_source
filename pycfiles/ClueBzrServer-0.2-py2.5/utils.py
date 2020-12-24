# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/clue/bzrserver/utils.py
# Compiled at: 2009-03-01 11:10:34
import logging
logger = logging.getLogger('clue.bzrserver')
logger.setLevel(level=logging.INFO)
security_logger = logging.getLogger('clue.bzrserver.security')
security_logger.setLevel(level=logging.WARNING)
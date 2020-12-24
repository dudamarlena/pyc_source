# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/monkey.py
# Compiled at: 2017-05-03 05:57:29
import logging
from photologue.models import PhotoSize
logger = logging.getLogger('logger')
logger.info('Patching PhotoSize.name max_length')
PhotoSize._meta.get_field('name').max_length = 255
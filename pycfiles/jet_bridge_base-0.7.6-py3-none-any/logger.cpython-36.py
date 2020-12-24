# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/logger.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 648 bytes
import logging
from jet_bridge_base import settings
logger = logging.getLogger('jet_bridge')
level = logging.DEBUG if settings.DEBUG else logging.INFO
ch = logging.StreamHandler()

class Formatter(logging.Formatter):
    formats = {logging.INFO: '%(message)s'}
    default_format = '%(levelname)s - %(asctime)s: %(message)s'

    def formatMessage(self, record):
        return self.formats.get(record.levelno, self.default_format) % record.__dict__


formatter = Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
ch.setLevel(level)
logger.setLevel(level)
logger.addHandler(ch)
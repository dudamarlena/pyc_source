# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/jlog.py
# Compiled at: 2016-10-25 21:37:30
# Size of source mod 2**32: 622 bytes
import json

class JLog(object):

    def __init__(self, logger, sid, tag='JLOG'):
        self.logger = logger
        self.id = sid
        self.tag = tag

    def _msg(self, info):
        return '<<{}:{}>> {}'.format(self.tag, self.id, json.dumps(info))

    def info(self, info):
        self.logger.info(self._msg(info))

    def debug(self, info):
        self.logger.debug(self._msg(info))

    def exception(self, info):
        self.logger.exception(self._msg(info))

    def error(self, info):
        self.logger.error(self._msg(info))

    def warning(self, info):
        self.logger.warning(self._msg(info))
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/upfluence/error_logger/noop.py
# Compiled at: 2016-10-21 12:25:13
import upfluence.log, opbeat_wrapper

class Client(opbeat_wrapper.Client):

    def __init__(self):
        self.base_service = None
        return

    def capture_exception(self, *args, **kwargs):
        upfluence.log.logger.error('exception:', exc_info=True)
        upfluence.log.logger.error(dict(self._build_base_extra(), **kwargs.get('extra', {})))
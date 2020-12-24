# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/mrlmessage.py
# Compiled at: 2017-08-14 13:34:55
from mrlpy.mevent import MEvent
import logging

class MrlMessage(MEvent):
    name = ''
    method = ''
    data = []
    log = logging.getLogger(__name__)

    def __init__(self, name, method, dat):
        self.log.debug('Creating message structure')
        self.name = name
        self.log.debug('Name set: ' + name)
        self.method = method
        self.log.debug('Method set: ' + method)
        self.data = dat
        self.log.debug('Data set')
        super(MrlMessage, self).__init__(name)
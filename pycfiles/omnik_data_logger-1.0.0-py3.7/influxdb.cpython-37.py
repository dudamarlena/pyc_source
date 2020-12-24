# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/omnik/plugins/influxdb.py
# Compiled at: 2020-01-03 09:42:15
# Size of source mod 2**32: 139 bytes
from omnik.plugins import Plugin

class influxdb(Plugin):

    def process(self, **args):
        self.logger.info('Hello from influxdb')
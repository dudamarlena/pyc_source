# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/converter/forwarder.py
# Compiled at: 2018-01-17 11:05:09
# Size of source mod 2**32: 246 bytes
from online_monitor.converter.transceiver import Transceiver

class Forwarder(Transceiver):

    def interpret_data(self, data):
        return [actual_data[1] for actual_data in data]
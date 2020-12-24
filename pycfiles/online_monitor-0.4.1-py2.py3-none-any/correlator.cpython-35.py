# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/converter/correlator.py
# Compiled at: 2015-10-23 07:39:36
# Size of source mod 2**32: 344 bytes
from online_monitor.converter.transceiver import Transceiver

class Correlator(Transceiver):

    def __init__(self, *args, **kwargs):
        Transceiver.__init__(self, *args, **kwargs)
        if self.n_receivers < 2:
            raise ValueError('A correlator needs at least two receivers! Specify the receive adresses in the config file.')
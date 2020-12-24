# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/freq_source.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 2477 bytes
from __future__ import absolute_import
import logging, psutil
from s_tui.sources.source import Source

class FreqSource(Source):
    __doc__ = ' Source class implementing CPU frequency information polling '

    def __init__(self):
        self.is_available = True
        if not hasattr(psutil, 'cpu_freq'):
            self.is_available = False
            logging.debug('cpu_freq is not available from psutil')
            return
        Source.__init__(self)
        self.name = 'Frequency'
        self.measurement_unit = 'MHz'
        self.pallet = ('freq light', 'freq dark', 'freq light smooth', 'freq dark smooth')
        self.last_measurement = [
         0] * len(psutil.cpu_freq(True))
        if psutil.cpu_freq(False):
            self.last_measurement.append(0)
        self.top_freq = psutil.cpu_freq().max
        self.max_freq = self.top_freq
        if self.top_freq == 0.0:
            if max(self.last_measurement) >= 0:
                self.max_freq = max(self.last_measurement)
        self.available_sensors = [
         'Avg']
        for core_id, _ in enumerate(psutil.cpu_freq(True)):
            self.available_sensors.append('Core ' + str(core_id))

    def update(self):
        self.last_measurement = [psutil.cpu_freq(False).current]
        for core in psutil.cpu_freq(True):
            self.last_measurement.append(core.current)

    def get_maximum(self):
        return self.max_freq

    def get_top(self):
        logging.debug('Returning top %s', self.top_freq)
        return self.top_freq
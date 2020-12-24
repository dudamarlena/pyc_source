# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/util_source.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 2108 bytes
from __future__ import absolute_import
import logging, psutil
from s_tui.sources.source import Source

class UtilSource(Source):

    def __init__(self):
        if not hasattr(psutil, 'cpu_percent'):
            self.is_available = False
            logging.debug('cpu utilization is not available from psutil')
            return
        Source.__init__(self)
        self.name = 'Util'
        self.measurement_unit = '%'
        self.pallet = ('util light', 'util dark', 'util light smooth', 'util dark smooth')
        self.last_measurement = [
         0] * (psutil.cpu_count() + 1)
        self.available_sensors = [
         'Avg']
        for core_id in range(psutil.cpu_count()):
            self.available_sensors.append('Core ' + str(core_id))

    def update(self):
        self.last_measurement = [
         psutil.cpu_percent(interval=0.0, percpu=False)]
        for util in psutil.cpu_percent(interval=0.0, percpu=True):
            logging.info('Core id util %s', util)
            self.last_measurement.append(float(util))

        logging.info('Utilization recorded %s', self.last_measurement)

    def get_is_available(self):
        return self.is_available

    def get_top(self):
        return 100
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/rapl_power_source.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 3450 bytes
""" RaplPowerSource is a s-tui Source, used to gather power usage
information
"""
from __future__ import absolute_import
import time, logging
from s_tui.sources.source import Source
import s_tui.sources.rapl_read as rapl_read
LOGGER = logging.getLogger(__name__)

class RaplPowerSource(Source):
    MICRO_JOULE_IN_JOULE = 1000000.0

    def __init__(self):
        Source.__init__(self)
        self.name = 'Power'
        self.measurement_unit = 'W'
        self.pallet = ('power light', 'power dark', 'power light smooth', 'power dark smooth')
        self.last_probe_time = time.time()
        self.last_probe = rapl_read()
        if not self.last_probe:
            self.is_available = False
            logging.debug('Power reading is not available')
            return
        self.max_power = 1
        self.last_measurement = [0] * len(self.last_probe)
        multi_sensors = []
        for item in self.last_probe:
            name = item.label
            sensor_count = multi_sensors.count(name)
            multi_sensors.append(name)
            if 'package' not in name:
                name += ',Pkg' + str(sensor_count)
            self.available_sensors.append(name)

    def update(self):
        if not self.is_available:
            return
        current_measurement_value = rapl_read()
        current_measurement_time = time.time()
        for m_idx, _ in enumerate(self.last_probe):
            joule_used = (current_measurement_value[m_idx].current - self.last_probe[m_idx].current) / float(self.MICRO_JOULE_IN_JOULE)
            self.last_probe[m_idx] = joule_used
            seconds_passed = current_measurement_time - self.last_probe_time
            logging.debug('seconds passed %s', seconds_passed)
            watts_used = float(joule_used) / float(seconds_passed)
            logging.debug('watts used %s', watts_used)
            logging.info('Joule_Used %d, seconds passed, %d', joule_used, seconds_passed)
            if watts_used > 0:
                self.last_measurement[m_idx] = watts_used
                logging.info('Power reading elapsed')

        self.last_probe = current_measurement_value
        self.last_probe_time = current_measurement_time

    def get_maximum(self):
        return self.max_power

    def get_top(self):
        return 1
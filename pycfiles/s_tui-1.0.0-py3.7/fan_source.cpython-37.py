# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/fan_source.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 2647 bytes
""" This module implements a fan source """
from __future__ import absolute_import
import logging, psutil
from s_tui.sources.source import Source

class FanSource(Source):
    __doc__ = ' Source for fan information '

    def __init__(self):
        if not hasattr(psutil, 'sensors_fans'):
            self.is_available = False
            logging.debug('Fans sensors is not available from psutil')
            return
        Source.__init__(self)
        self.name = 'Fan'
        self.measurement_unit = 'RPM'
        self.pallet = ('fan light', 'fan dark', 'fan light smooth', 'fan dark smooth')
        sensors_dict = dict()
        try:
            sensors_dict = psutil.sensors_fans()
        except IOError:
            logging.debug('Unable to create sensors dict')
            self.is_available = False
            return
        else:
            if not sensors_dict:
                self.is_available = False
                return
            for key, value in sensors_dict.items():
                sensor_name = key
                for sensor_idx, sensor in enumerate(value):
                    sensor_label = sensor.label
                    full_name = ''
                    if not sensor_label:
                        full_name = sensor_name + ',' + str(sensor_idx)
                    else:
                        full_name = sensor_label
                    logging.debug('Fan sensor name %s', full_name)
                    self.available_sensors.append(full_name)

            self.last_measurement = [
             0] * len(self.available_sensors)

    def update(self):
        sample = psutil.sensors_fans()
        self.last_measurement = []
        for sensor in sample.values():
            for minor_sensor in sensor:
                self.last_measurement.append(int(minor_sensor.current))

    def get_edge_triggered(self):
        return False

    def get_top(self):
        return 1
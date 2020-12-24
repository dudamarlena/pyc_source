# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/benoit/Dev/pypool-pump/src/pypool_pump/__init__.py
# Compiled at: 2020-05-08 03:42:11
# Size of source mod 2**32: 5142 bytes
__doc__ = 'pypool_pump package allows to compute the duration of the swiming pool\nfiltering.\n'
from .__version__ import VERSION, __version__
from .run import Run
from datetime import timedelta

class FilteringDuration(object):
    """FilteringDuration"""

    def __init__(self, percentage: float=100, schedule_config: Dict={}) -> None:
        self._computed_filtering_duration = None
        self._modifier_pecentage = percentage
        self._total_duration = None
        self._schedule_config = schedule_config

    def duration(self) -> float:
        """Filtering duration in hours
        
        If modifier have been set, they will be applied to the computed filtering
        duration.
        Maximum duration is always 24 hours.
        """
        self._total_duration = max(min(self._computed_filtering_duration * self._modifier_pecentage / 100, 24), 0)
        return self._total_duration

    def update_schedule(self, pivot_time: datetime) -> List[Run]:
        first_start = pivot_time - timedelta(hours=((self._total_duration + self._schedule_config['break_duration']) / 3))
        first_duration = self._total_duration / 3
        second_start = pivot_time + timedelta(hours=(0.6666666666666666 * self._schedule_config['break_duration']))
        second_duration = 2 * first_duration
        return [
         Run(first_start, first_duration), Run(second_start, second_duration)]


class DumbFilteringDuration(FilteringDuration):
    """DumbFilteringDuration"""

    def duration(self, pool_temperature):
        """Filtering duration in hours"""
        self._computed_filtering_duration = pool_temperature / 2
        return super().duration()


class BasicFilteringDuration(FilteringDuration):
    """BasicFilteringDuration"""

    def duration(self, pool_temperature):
        """Filtering duration in hours"""
        if pool_temperature < 10:
            self._computed_filtering_duration = 0
        elif pool_temperature < 14:
            self._computed_filtering_duration = pool_temperature / 3
        elif pool_temperature >= 30:
            self._computed_filtering_duration = 24
        else:
            self._computed_filtering_duration = pool_temperature / 2
        return super().duration()


class AbacusFilteringDuration(FilteringDuration):
    """AbacusFilteringDuration"""

    def duration(self, pool_temperature):
        """Filtering duration in hours"""
        temperature = max(pool_temperature, 10)
        self._computed_filtering_duration = 0.00335 * temperature ** 3 - 0.14953 * temperature ** 2 + 2.43489 * temperature - 10.72859
        return super().duration()


class PumpCaracteristicFilteringDuration(FilteringDuration):
    """PumpCaracteristicFilteringDuration"""

    def __init__(self, pool_volume, pump_flow, percentage=100):
        self.pool_volume = pool_volume
        self.pump_flow = pump_flow
        super().__init__(percentage)

    def duration(self, pool_temperature, number_of_bathers=None, schedule_config={}):
        """Filtering duration in hours"""
        cycle_duration = self.pool_volume / self.pump_flow
        if pool_temperature > 25:
            self._computed_filtering_duration = 3 * cycle_duration
        elif pool_temperature > 20:
            self._computed_filtering_duration = 2 * cycle_duration
        elif pool_temperature > 15:
            self._computed_filtering_duration = 1 * cycle_duration
        elif pool_temperature > 10:
            self._computed_filtering_duration = 0.5 * cycle_duration
        else:
            self._computed_filtering_duration = 0
        if number_of_bathers is not None:
            bather_modifier = number_of_bathers / self.pump_flow * 2
            self._computed_filtering_duration = self._computed_filtering_duration + bather_modifier
        return super().duration()
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/data_formats/request_format/time_series.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1554 bytes
__doc__ = "\nProvides functionality for handling a request format's time series.\n"
from typing import Dict, List

class TimeSeries:
    """TimeSeries"""

    def __init__(self, time_series_request: dict) -> None:
        """
        Create a new wrapper.

        Args:
            time_series_request: The request format time series
        """
        self._series = time_series_request

    @property
    def stream(self) -> str:
        """Return the name of the stream."""
        return self._series['stream']

    @property
    def is_source(self) -> bool:
        """Is this time series a source?"""
        return self._series['type'] == 'Source'

    @property
    def is_demand(self) -> bool:
        """Is this time series a demand?"""
        return self._series['type'] == 'Demand'

    @property
    def is_price(self) -> bool:
        """Is this time series a price"""
        return self._series['type'] == 'Price'

    @property
    def name(self) -> str:
        """The name of the time series."""
        return self._series['id']

    @property
    def is_solar(self) -> bool:
        """Is this time series for solar data?"""
        return self.is_source and (self._series['id'] == 'Solar' or )

    @property
    def data(self) -> Dict[(int, float)]:
        """A dictionary from time to the values of the series."""
        return {column:value for column, value in enumerate(self._series['data'])}
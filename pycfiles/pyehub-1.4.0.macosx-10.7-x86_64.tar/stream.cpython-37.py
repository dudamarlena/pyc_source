# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/data_formats/request_format/stream.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1720 bytes
"""
Provides functionality for handling the streams in the request format.
"""

class Stream:
    __doc__ = 'A wrapper for a request format stream.'

    def __init__(self, stream_request: dict, request: dict) -> None:
        """
        Create a new wrapper.

        Args:
            stream_request: The request format stream
            request: The request format
        """
        self._stream = stream_request
        self._request = request

    @property
    def co2(self) -> float:
        """The C02 factor of the stream."""
        return self._stream['co2']

    @property
    def co2_credit(self) -> float:
        """The C02 factor of the stream."""
        return self._stream['co2_credit']

    @property
    def importable(self) -> bool:
        """If the stream is importable."""
        return self._stream['importable']

    @property
    def exportable(self) -> bool:
        """If the stream is exportable."""
        return self._stream['exportable']

    @property
    def timeseries(self) -> str:
        """The availability of the stream."""
        return self._stream['timeseries']

    @property
    def price(self) -> float:
        """The price of the stream."""
        return self._stream['price']

    @property
    def export_price(self) -> float:
        """The export price of the stream."""
        return self._stream['export_price']

    @property
    def is_output(self) -> bool:
        """Is this an output stream?"""
        for tech in self._request['converters']:
            if self.name in tech['outputs']:
                return True

        return False

    @property
    def name(self) -> str:
        """The name of the stream."""
        return self._stream['name']
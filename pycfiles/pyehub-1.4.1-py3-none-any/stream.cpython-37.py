# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/data_formats/request_format/stream.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1720 bytes
__doc__ = '\nProvides functionality for handling the streams in the request format.\n'

class Stream:
    """Stream"""

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
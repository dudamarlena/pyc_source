# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\pycker\pick.py
# Compiled at: 2017-09-14 09:37:13
# Size of source mod 2**32: 5031 bytes
"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
from obspy.core.utcdatetime import UTCDateTime
from .quantity_error import QuantityError
__all__ = [
 'Pick']

class Pick:
    __doc__ = '\n    A pick is the observation of an amplitude anomaly in a seismogram at a\n    specific point in time. It is not necessarily related to a seismic event.\n    \n    Parameters\n    ----------\n    time : scalar or None, default None\n        Observed onset time of signal (“pick time”).\n    index : scalar or None, default None\n        Corresponding index on trace.\n    sampling_rate : scalar or None, default None\n        Sampling rate (in Hz).\n    time_errors : QuantityError\n        Observed onset time of signal uncertainties.\n    shift : scalar or None\n        Shift applied to origin time for picking (samples).\n    phase_hint : str or None, default None\n        Tentative phase identification as specified by the picker.\n    '
    _ATTRIBUTES = [
     'time', 'index', 'sampling_rate', 'time_errors', 'shift', 'phase_hint']

    def __init__(self, time=None, index=None, sampling_rate=None, time_errors=QuantityError(), shift=None, phase_hint=None):
        if time is not None and not isinstance(time, (float, UTCDateTime)):
            raise ValueError('time must be a float or UTCDateTime')
        else:
            self._time = time
        if index is not None and not isinstance(index, (int, float)):
            raise ValueError('index must be an integer or float')
        else:
            self._index = index
        if sampling_rate is not None and (not isinstance(sampling_rate, (int, float)) or sampling_rate < 0.0):
            raise ValueError('sampling_rate must be a positive integer or float')
        else:
            self._sampling_rate = sampling_rate
        if not isinstance(time_errors, QuantityError):
            raise ValueError('time_errors must be QuantityError')
        else:
            self._time_errors = time_errors
        if shift is not None and not isinstance(shift, (int, float)):
            raise ValueError('shift must be an integer or float')
        else:
            self._shift = shift
        if phase_hint is not None and not isinstance(phase_hint, str):
            raise ValueError('phase_hint must be a string')
        else:
            self._phase_hint = phase_hint

    def __repr__(self):
        attributes = ['%s: %s' % (attr.rjust(13), self._print_attr(attr)) for attr in self._ATTRIBUTES]
        return '\n'.join(attributes) + '\n'

    def _print_attr(self, attr):
        if attr not in self._ATTRIBUTES:
            raise ValueError("error_type should be either 'time', 'index', 'sampling_rate', 'time_errors', 'shift' or 'phase_hint'")
        else:
            if attr == 'time':
                return self._time
            if attr == 'index':
                return self._index
            if attr == 'sampling_rate':
                return self._sampling_rate
            if attr == 'time_errors':
                return self._time_errors
            if attr == 'shift':
                return self._shift
            if attr == 'phase_hint':
                return self._phase_hint

    @property
    def time(self):
        """
        scalar or None
        Observed onset time of signal (“pick time”).
        """
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def index(self):
        """
        scalar or None
        Corresponding index on trace.
        """
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def sampling_rate(self):
        """
        scalar or None, default None
        Sampling rate (in Hz).
        """
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, value):
        self._sampling_rate = value

    @property
    def time_errors(self):
        """
        QuantityError
        Observed onset time of signal uncertainties.
        """
        return self._time_errors

    @time_errors.setter
    def time_errors(self, value):
        self._time_errors = value

    @property
    def shift(self):
        """
        scalar or None
        Shift applied to origin time for picking (samples).
        """
        return self._shift

    @shift.setter
    def shift(self, value):
        self._shift = value

    @property
    def phase_hint(self):
        """
        str or None
        Tentative phase identification as specified by the picker.
        """
        return self._phase_hint

    @phase_hint.setter
    def phase_hint(self, value):
        self._phase_hint = value
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\downsample_helpers.py
# Compiled at: 2018-01-16 00:28:55
# Size of source mod 2**32: 1863 bytes
"""
Helpers for downsampling code.
"""
from operator import attrgetter
from strategycontainer.utils.input_validation import expect_element
from strategycontainer.utils.numpy_utils import changed_locations
from strategycontainer.utils.sharedoc import templated_docstring, PIPELINE_DOWNSAMPLING_FREQUENCY_DOC
_dt_to_period = {'year_start':attrgetter('year'), 
 'quarter_start':attrgetter('quarter'), 
 'month_start':attrgetter('month'), 
 'week_start':attrgetter('week')}
SUPPORTED_DOWNSAMPLE_FREQUENCIES = frozenset(_dt_to_period)
expect_downsample_frequency = expect_element(frequency=SUPPORTED_DOWNSAMPLE_FREQUENCIES)

@expect_downsample_frequency
@templated_docstring(frequency=PIPELINE_DOWNSAMPLING_FREQUENCY_DOC)
def select_sampling_indices(dates, frequency):
    """
    Choose entries from ``dates`` to use for downsampling at ``frequency``.

    Parameters
    ----------
    dates : pd.DatetimeIndex
        Dates from which to select sample choices.
    {frequency}

    Returns
    -------
    indices : np.array[int64]
        An array condtaining indices of dates on which samples should be taken.

        The resulting index will always include 0 as a sample index, and it
        will include the first date of each subsequent year/quarter/month/week,
        as determined by ``frequency``.

    Notes
    -----
    This function assumes that ``dates`` does not have large gaps.

    In particular, it assumes that the maximum distance between any two entries
    in ``dates`` is never greater than a year, which we rely on because we use
    ``np.diff(dates.<frequency>)`` to find dates where the sampling
    period has changed.
    """
    return changed_locations((_dt_to_period[frequency](dates)),
      include_first=True)
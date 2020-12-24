# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/signal/datachop.py
# Compiled at: 2018-11-21 13:02:33
# Size of source mod 2**32: 2217 bytes


def _calc_start_stop_from_offset(offsets, start_time=-1.0, end_time=2.0, buffer_time=0.5):
    starts = (offsets + (buffer_time * -1000 + start_time * 1000)).astype(int)
    stops = (offsets + (buffer_time * 1000 + end_time * 1000)).astype(int)
    return (
     starts, stops)


def chop_data_from_offsets(timeseries, offsets, start_time, end_time, buffer_time=0.0):
    if np.sign(start_time) == np.sign(end_time):
        start_time = -1 * start_time
    start, stop = _calc_start_stop_from_offset(offsets, start_time=start_time, end_time=end_time,
      buffer_time=buffer_time)
    time_axis = np.arange(stop[0] - start[0]) / timeseries['samplerate'].data
    if start_time * -1 == end_time:
        time_axis = time_axis - time_axis[(-1)] / 2
    dat = []
    for _start, _stop in zip(start[:-1], stop[:-1]):
        chopped = timeseries[(Ellipsis, slice(_start, _stop))]
        chopped['time'].data = time_axis
        dat.append(chopped)

    data = TimeSeriesLF.concat(dat, 'events')
    data['buffer_time'] = buffer_time
    return data


def minimum_time_from_frequency_ncycles(frequency, cycles=5):
    return cycles / frequency


def numbers_between(arr, low, high, values=False):
    if values:
        return arr[numbers_between(arr, low, high, False)]
    return np.logical_and(low <= arr, arr <= high)


def dataframe_from_connectivity_matrix(connectivity_matrix, frequency_bands, frequency_selection):
    dat = conectivity_matrix[:, :, numbers_between(frequency_bands, *frequency_selection)]
    return pd.DataFrame(np.mean(dat, -1))


def group_dataframe_from_rois(df, rois):
    """Given a dataframe N x N, returns mean M x M matrix of grouped mean rois

    INPUTS
    -------
    df: pd.DataFrame, shape = N x N
    rois: np.array like, shape N"""
    rois = pd.Series(rois)
    rois_df = df.groupby(by=rois, axis=0).mean().groupby(by=rois, axis=1).mean()
    return rois_df
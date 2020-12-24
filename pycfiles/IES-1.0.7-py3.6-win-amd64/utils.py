# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\loaders\utils.py
# Compiled at: 2018-01-16 21:50:37
# Size of source mod 2**32: 17606 bytes
import datetime, numpy as np, pandas as pd
from strategycontainer.exception import NoFurtherDataError
from strategycontainer.tsp.common import TS_FIELD_NAME, SID_FIELD_NAME
from strategycontainer.utils.numpy_utils import categorical_dtype
from strategycontainer.utils.pandas_utils import mask_between_time

def is_sorted_ascending(a):
    """Check if a numpy array is sorted."""
    return (np.fmax.accumulate(a) <= a).all()


def validate_event_metadata(event_dates, event_timestamps, event_sids):
    if not is_sorted_ascending(event_dates):
        raise AssertionError('event dates must be sorted')
    elif not len(event_sids) == len(event_dates) == len(event_timestamps):
        raise AssertionError('mismatched arrays: %d != %d != %d' % (
         len(event_sids),
         len(event_dates),
         len(event_timestamps)))


def next_event_indexer(all_dates, all_sids, event_dates, event_timestamps, event_sids):
    """
    Construct an index array that, when applied to an array of values, produces
    a 2D array containing the values associated with the next event for each
    sid at each moment in time.

    Locations where no next event was known will be filled with -1.

    Parameters
    ----------
    all_dates : ndarray[datetime64[ns], ndim=1]
        Row labels for the target output.
    all_sids : ndarray[int, ndim=1]
        Column labels for the target output.
    event_dates : ndarray[datetime64[ns], ndim=1]
        Dates on which each input events occurred/will occur.  ``event_dates``
        must be in sorted order, and may not contain any NaT values.
    event_timestamps : ndarray[datetime64[ns], ndim=1]
        Dates on which we learned about each input event.
    event_sids : ndarray[int, ndim=1]
        Sids assocated with each input event.

    Returns
    -------
    indexer : ndarray[int, ndim=2]
        An array of shape (len(all_dates), len(all_sids)) of indices into
        ``event_{dates,timestamps,sids}``.
    """
    validate_event_metadata(event_dates, event_timestamps, event_sids)
    out = np.full((len(all_dates), len(all_sids)), (-1), dtype=(np.int64))
    sid_ixs = all_sids.searchsorted(event_sids)
    dt_ixs = all_dates.searchsorted(event_dates, side='right')
    ts_ixs = all_dates.searchsorted(event_timestamps)
    for i in range(len(event_sids) - 1, -1, -1):
        start_ix = ts_ixs[i]
        end_ix = dt_ixs[i]
        out[start_ix:end_ix, sid_ixs[i]] = i

    return out


def previous_event_indexer(all_dates, all_sids, event_dates, event_timestamps, event_sids):
    """
    Construct an index array that, when applied to an array of values, produces
    a 2D array containing the values associated with the previous event for
    each sid at each moment in time.

    Locations where no previous event was known will be filled with -1.

    Parameters
    ----------
    all_dates : ndarray[datetime64[ns], ndim=1]
        Row labels for the target output.
    all_sids : ndarray[int, ndim=1]
        Column labels for the target output.
    event_dates : ndarray[datetime64[ns], ndim=1]
        Dates on which each input events occurred/will occur.  ``event_dates``
        must be in sorted order, and may not contain any NaT values.
    event_timestamps : ndarray[datetime64[ns], ndim=1]
        Dates on which we learned about each input event.
    event_sids : ndarray[int, ndim=1]
        Sids assocated with each input event.

    Returns
    -------
    indexer : ndarray[int, ndim=2]
        An array of shape (len(all_dates), len(all_sids)) of indices into
        ``event_{dates,timestamps,sids}``.
    """
    validate_event_metadata(event_dates, event_timestamps, event_sids)
    out = np.full((len(all_dates), len(all_sids)), (-1), dtype=(np.int64))
    eff_dts = np.maximum(event_dates, event_timestamps)
    sid_ixs = all_sids.searchsorted(event_sids)
    dt_ixs = all_dates.searchsorted(eff_dts)
    last_written = {}
    for i in range(len(event_dates) - 1, -1, -1):
        sid_ix = sid_ixs[i]
        dt_ix = dt_ixs[i]
        out[dt_ix:last_written.get(sid_ix, None), sid_ix] = i
        last_written[sid_ix] = dt_ix

    return out


def normalize_data_query_time(dt, time, tz):
    """Apply the correct time and timezone to a date.

    Parameters
    ----------
    dt : pd.Timestamp
        The original datetime that represents the date.
    time : datetime.time
        The time of day to use as the cutoff point for new data. Data points
        that you learn about after this time will become available to your
        algorithm on the next trading day.
    tz : tzinfo
        The timezone to normalize your dates to before comparing against
        `time`.

    Returns
    -------
    query_dt : pd.Timestamp
        The timestamp with the correct time and date in utc.
    """
    return pd.Timestamp((datetime.datetime.combine(dt.date(), time)),
      tz=tz).tz_convert('utc')


def normalize_data_query_bounds(lower, upper, time, tz):
    """Adjust the first and last dates in the requested datetime index based on
    the provided query time and tz.

    lower : pd.Timestamp
        The lower date requested.
    upper : pd.Timestamp
        The upper date requested.
    time : datetime.time
        The time of day to use as the cutoff point for new data. Data points
        that you learn about after this time will become available to your
        algorithm on the next trading day.
    tz : tzinfo
        The timezone to normalize your dates to before comparing against
        `time`.
    """
    lower -= datetime.timedelta(days=1)
    if time is not None:
        return (
         normalize_data_query_time(lower, time, tz),
         normalize_data_query_time(upper, time, tz))
    else:
        return (
         lower, upper)


_midnight = datetime.time(0, 0)

def normalize_timestamp_to_query_time(df, time, tz, inplace=False, ts_field='timestamp'):
    """Update the timestamp field of a dataframe to normalize dates around
    some data query time/timezone.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to update. This needs a column named ``ts_field``.
    time : datetime.time
        The time of day to use as the cutoff point for new data. Data points
        that you learn about after this time will become available to your
        algorithm on the next trading day.
    tz : tzinfo
        The timezone to normalize your dates to before comparing against
        `time`.
    inplace : bool, optional
        Update the dataframe in place.
    ts_field : str, optional
        The name of the timestamp field in ``df``.

    Returns
    -------
    df : pd.DataFrame
        The dataframe with the timestamp field normalized. If ``inplace`` is
        true, then this will be the same object as ``df`` otherwise this will
        be a copy.
    """
    if not inplace:
        df = df.copy()
    df.sort_values(ts_field, inplace=True)
    dtidx = pd.DatetimeIndex((df.loc[:, ts_field]), tz='utc')
    dtidx_local_time = dtidx.tz_convert(tz)
    to_roll_forward = mask_between_time(dtidx_local_time,
      time,
      _midnight,
      include_end=False)
    df.loc[(to_roll_forward, ts_field)] = (dtidx_local_time[to_roll_forward] + datetime.timedelta(days=1)).normalize().tz_localize(None).tz_localize('utc').normalize()
    df.loc[(~to_roll_forward, ts_field)] = dtidx[(~to_roll_forward)].normalize()
    return df


def check_data_query_args(data_query_time, data_query_tz):
    """Checks the data_query_time and data_query_tz arguments for loaders
    and raises a standard exception if one is None and the other is not.

    Parameters
    ----------
    data_query_time : datetime.time or None
    data_query_tz : tzinfo or None

    Raises
    ------
    ValueError
        Raised when only one of the arguments is None.
    """
    if (data_query_time is None) ^ (data_query_tz is None):
        raise ValueError("either 'data_query_time' and 'data_query_tz' must both be None or neither may be None (got %r, %r)" % (
         data_query_time,
         data_query_tz))


def last_in_date_group(df, dates, assets, reindex=True, have_sids=True, extra_groupers=None):
    """
    Determine the last piece of information known on each date in the date
    index for each group. Input df MUST be sorted such that the correct last
    item is chosen from each group.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be grouped. Must be sorted so that
        the correct last item is chosen from each group.
    dates : pd.DatetimeIndex
        The dates to use for grouping and reindexing.
    assets : pd.Int64Index
        The assets that should be included in the column multiindex.
    reindex : bool
        Whether or not the DataFrame should be reindexed against the date
        index. This will add back any dates to the index that were grouped
        away.
    have_sids : bool
        Whether or not the DataFrame has sids. If it does, they will be used
        in the groupby.
    extra_groupers : list of str
        Any extra field names that should be included in the groupby.

    Returns
    -------
    last_in_group : pd.DataFrame
        A DataFrame with dates as the index and fields used in the groupby as
        levels of a multiindex of columns.

    """
    idx = [
     dates[dates.searchsorted(df[TS_FIELD_NAME].values.astype('datetime64[D]'))]]
    if have_sids:
        idx += [SID_FIELD_NAME]
    if extra_groupers is None:
        extra_groupers = []
    idx += extra_groupers
    last_in_group = df.drop(TS_FIELD_NAME, axis=1).groupby(idx,
      sort=False).last()
    for _ in range(len(idx) - 1):
        last_in_group = last_in_group.unstack(-1)

    if reindex:
        if have_sids:
            cols = last_in_group.columns
            last_in_group = last_in_group.reindex(index=dates,
              columns=pd.MultiIndex.from_product((tuple(cols.levels[0:len(extra_groupers) + 1]) + (assets,)),
              names=(cols.names)))
        else:
            last_in_group = last_in_group.reindex(dates)
    return last_in_group


def ffill_across_cols(df, columns, name_map):
    """
    Forward fill values in a DataFrame with special logic to handle cases
    that pd.DataFrame.ffill cannot and cast columns to appropriate types.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to do forward-filling on.
    columns : list of BoundColumn
        The BoundColumns that correspond to columns in the DataFrame to which
        special filling and/or casting logic should be applied.
    name_map: map of string -> string
        Mapping from the name of each BoundColumn to the associated column
        name in `df`.
    """
    df.ffill(inplace=True)
    for column in columns:
        column_name = name_map[column.name]
        if column.dtype == categorical_dtype:
            df[column_name] = df[column.name].where(pd.notnull(df[column_name]), column.missing_value)
        else:
            df[column_name] = df[column_name].fillna(column.missing_value).astype(column.dtype)


def shift_dates(dates, start_date, end_date, shift):
    """
    Shift dates of a pipeline query back by `shift` days.

    load_adjusted_array is called with dates on which the user's algo
    will be shown data, which means we need to return the data that would
    be known at the start of each date.  This is often labeled with a
    previous date in the underlying data (e.g. at the start of today, we
    have the data as of yesterday). In this case, we can shift the query
    dates back to query the appropriate values.

    Parameters
    ----------
    dates : DatetimeIndex
        All known dates.
    start_date : pd.Timestamp
        Start date of the pipeline query.
    end_date : pd.Timestamp
        End date of the pipeline query.
    shift : int
        The number of days to shift back the query dates.
    """
    try:
        start = dates.get_loc(start_date)
    except KeyError:
        if start_date < dates[0]:
            raise NoFurtherDataError(msg='Pipeline Query requested data starting on {query_start}, but first known date is {calendar_start}'.format(query_start=(str(start_date)),
              calendar_start=(str(dates[0]))))
        else:
            raise ValueError('Query start %s not in calendar' % start_date)

    if start < shift:
        raise NoFurtherDataError(msg='Pipeline Query requested data from {shift} days before {query_start}, but first known date is only {start} days earlier.'.format(shift=shift,
          query_start=start_date,
          start=start))
    try:
        end = dates.get_loc(end_date)
    except KeyError:
        if end_date > dates[(-1)]:
            raise NoFurtherDataError(msg='Pipeline Query requesting data up to {query_end}, but last known date is {calendar_end}'.format(query_end=end_date,
              calendar_end=(dates[(-1)])))
        else:
            raise ValueError('Query end %s not in calendar' % end_date)

    return (
     dates[(start - shift)], dates[(end - shift)])
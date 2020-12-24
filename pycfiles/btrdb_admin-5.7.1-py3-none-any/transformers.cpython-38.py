# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/transformers.py
# Compiled at: 2020-05-13 17:11:01
# Size of source mod 2**32: 11275 bytes
__doc__ = '\nValue transformation utilities\n'
import csv, contextlib
from collections import OrderedDict
from warnings import warn
_STAT_PROPERTIES = ('min', 'mean', 'max', 'count', 'stddev')

def _get_time_from_row(row):
    for item in row:
        if item:
            return item.time
        raise Exception('Row contains no data')


def _stream_names(streamset, func):
    """
    private convenience function to come up with proper final stream names
    before sending a collection of streams (dataframe, etc.) back to the
    user.
    """
    return tuple((func(s) for s in streamset._streams))


def to_series(streamset, datetime64_index=True, agg='mean', name_callable=None):
    """
    Returns a list of Pandas Series objects indexed by time

    Parameters
    ----------
    datetime64_index: bool
        Directs function to convert Series index to np.datetime64[ns] or
        leave as np.int64.

    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to create the Series
        from. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Sprecify a callable that can be used to determine the series name given a
        Stream object.

    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError('Please install Pandas to use this transformation function.')
    else:
        if agg == 'all':
            raise AttributeError("cannot use 'all' as aggregate at this time")
        if not callable(name_callable):
            name_callable = lambda s: s.collection + '/' + s.name
        result = []
        stream_names = _stream_names(streamset, name_callable)
        for idx, output in enumerate(streamset.values()):
            times, values = [], []
            for point in output:
                times.append(point.time)
                if point.__class__.__name__ == 'RawPoint':
                    values.append(point.value)
                else:
                    values.append(getattr(point, agg))

            if datetime64_index:
                times = pd.Index(times, dtype='datetime64[ns]')
            result.append(pd.Series(data=values,
              index=times,
              name=(stream_names[idx])))

        return result


def to_dataframe(streamset, columns=None, agg='mean', name_callable=None):
    """
    Returns a Pandas DataFrame object indexed by time and using the values of a
    stream for each column.

    Parameters
    ----------
    columns: sequence
        column names to use for DataFrame.  Deprecated and not compatible with name_callable.

    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to create the Series
        from. Must be one of "min", "mean", "max", "count", "stddev", or "all". This
        argument is ignored if not using StatPoints.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Sprecify a callable that can be used to determine the series name given a
        Stream object.  This is not compatible with agg == "all" at this time

    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError('Please install Pandas to use this transformation function.')
    else:
        if columns:
            warn('the columns argument is deprecated and will be removed in a future release', DeprecationWarning, stacklevel=2)
        elif agg == 'all':
            if name_callable is not None:
                raise AttributeError("cannot provide name_callable when using 'all' as aggregate at this time")
            elif agg == 'all' and streamset.allow_window:
                agg = ''
            if not callable(name_callable):
                name_callable = lambda s: s.collection + '/' + s.name
            df = pd.DataFrame(to_dict(streamset, agg=agg))
            df = df.set_index('time')
            if agg == 'all':
                stream_names = streamset.allow_window or [[
                 s.collection, s.name, prop] for s in streamset._streams for prop in _STAT_PROPERTIES]
                df.columns = pd.MultiIndex.from_tuples(stream_names)
        else:
            df.columns = columns if columns else _stream_names(streamset, name_callable)
        return df


def to_array(streamset, agg='mean'):
    """
    Returns a multidimensional numpy array (similar to a list of lists) containing point
    classes.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to return for the
        arrays. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError('Please install Numpy to use this transformation function.')
    else:
        if agg == 'all':
            raise AttributeError("cannot use 'all' as aggregate at this time")
        results = []
        for points in streamset.values():
            segment = []
            for point in points:
                if point.__class__.__name__ == 'RawPoint':
                    segment.append(point.value)
                else:
                    segment.append(getattr(point, agg))

            results.append(segment)

        return np.array(results)


def to_dict(streamset, agg='mean', name_callable=None):
    """
    Returns a list of OrderedDict for each time code with the appropriate
    stream data attached.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to constrain dict
        keys. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Sprecify a callable that can be used to determine the series name given a
        Stream object.

    """
    if not callable(name_callable):
        name_callable = lambda s: s.collection + '/' + s.name
    data = []
    stream_names = _stream_names(streamset, name_callable)
    for row in streamset.rows():
        item = OrderedDict({'time': _get_time_from_row(row)})
        for idx, col in enumerate(stream_names):
            if row[idx].__class__.__name__ == 'RawPoint':
                item[col] = row[idx].value if row[idx] else None
            elif agg == 'all':
                for stat in _STAT_PROPERTIES:
                    item['{}-{}'.format(col, stat)] = getattr(row[idx], stat) if row[idx] else None

            else:
                item[col] = getattr(row[idx], agg) if row[idx] else None

        data.append(item)

    return data


def to_csv--- This code section failed: ---

 L. 261         0  LOAD_FAST                'agg'
                2  LOAD_STR                 'all'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 262         8  LOAD_GLOBAL              AttributeError
               10  LOAD_STR                 "cannot use 'all' as aggregate at this time"
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  ''
             16_0  COME_FROM             6  '6'

 L. 264        16  LOAD_GLOBAL              callable
               18  LOAD_FAST                'name_callable'
               20  CALL_FUNCTION_1       1  ''
               22  POP_JUMP_IF_TRUE     32  'to 32'

 L. 265        24  LOAD_LAMBDA              '<code_object <lambda>>'
               26  LOAD_STR                 'to_csv.<locals>.<lambda>'
               28  MAKE_FUNCTION_0          ''
               30  STORE_FAST               'name_callable'
             32_0  COME_FROM            22  '22'

 L. 267        32  LOAD_GLOBAL              contextlib
               34  LOAD_ATTR                contextmanager

 L. 268        36  LOAD_CODE                <code_object open_path_or_file>
               38  LOAD_STR                 'to_csv.<locals>.open_path_or_file'
               40  MAKE_FUNCTION_0          ''
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'open_path_or_file'

 L. 280        46  LOAD_FAST                'open_path_or_file'
               48  LOAD_FAST                'fobj'
               50  CALL_FUNCTION_1       1  ''
               52  SETUP_WITH          144  'to 144'
               54  STORE_FAST               'csvfile'

 L. 281        56  LOAD_GLOBAL              _stream_names
               58  LOAD_FAST                'streamset'
               60  LOAD_FAST                'name_callable'
               62  CALL_FUNCTION_2       2  ''
               64  STORE_FAST               'stream_names'

 L. 282        66  LOAD_FAST                'fieldnames'
               68  POP_JUMP_IF_FALSE    74  'to 74'
               70  LOAD_FAST                'fieldnames'
               72  JUMP_FORWARD         86  'to 86'
             74_0  COME_FROM            68  '68'
               74  LOAD_STR                 'time'
               76  BUILD_LIST_1          1 
               78  LOAD_GLOBAL              list
               80  LOAD_FAST                'stream_names'
               82  CALL_FUNCTION_1       1  ''
               84  BINARY_ADD       
             86_0  COME_FROM            72  '72'
               86  STORE_FAST               'fieldnames'

 L. 284        88  LOAD_GLOBAL              csv
               90  LOAD_ATTR                DictWriter
               92  LOAD_FAST                'csvfile'
               94  LOAD_FAST                'fieldnames'
               96  LOAD_FAST                'dialect'
               98  LOAD_CONST               ('fieldnames', 'dialect')
              100  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              102  STORE_FAST               'writer'

 L. 285       104  LOAD_FAST                'writer'
              106  LOAD_METHOD              writeheader
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          

 L. 287       112  LOAD_GLOBAL              to_dict
              114  LOAD_FAST                'streamset'
              116  LOAD_FAST                'agg'
              118  LOAD_CONST               ('agg',)
              120  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              122  GET_ITER         
              124  FOR_ITER            140  'to 140'
              126  STORE_FAST               'item'

 L. 288       128  LOAD_FAST                'writer'
              130  LOAD_METHOD              writerow
              132  LOAD_FAST                'item'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_BACK           124  'to 124'
              140  POP_BLOCK        
              142  BEGIN_FINALLY    
            144_0  COME_FROM_WITH       52  '52'
              144  WITH_CLEANUP_START
              146  WITH_CLEANUP_FINISH
              148  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 142


def to_table(streamset, agg='mean', name_callable=None):
    """
    Returns string representation of the data in tabular form using the tabulate
    library.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to create the Series
        from. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Sprecify a callable that can be used to determine the column name given a
        Stream object.

    """
    try:
        from tabulate import tabulate
    except ImportError:
        raise ImportError('Please install tabulate to use this transformation function.')
    else:
        if agg == 'all':
            raise AttributeError("cannot use 'all' as aggregate at this time")
        if not callable(name_callable):
            name_callable = lambda s: s.collection + '/' + s.name
        return tabulate(streamset.to_dict(agg=agg, name_callable=name_callable), headers='keys')


class StreamSetTransformer(object):
    """StreamSetTransformer"""
    to_dict = to_dict
    to_array = to_array
    to_series = to_series
    to_dataframe = to_dataframe
    to_csv = to_csv
    to_table = to_table
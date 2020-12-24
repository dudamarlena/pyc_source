# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <xlwings_pro-1.2.2>/xlwings/conversion/pandas_conv.py
# Compiled at: 2020-03-09 05:37:56
try:
    import pandas as pd
except ImportError:
    pd = None

if pd:
    import numpy as np
    from . import Converter, Options

    class PandasDataFrameConverter(Converter):
        writes_types = pd.DataFrame

        @classmethod
        def base_reader(cls, options):
            return super(PandasDataFrameConverter, cls).base_reader(Options(options).override(ndim=2))

        @classmethod
        def read_value(cls, value, options):
            index = options.get('index', 1)
            header = options.get('header', 1)
            dtype = options.get('dtype', None)
            copy = options.get('copy', False)
            if header == 1:
                columns = pd.Index(value[0])
            elif header > 1:
                columns = pd.MultiIndex.from_arrays(value[:header])
            else:
                columns = None
            df = pd.DataFrame(value[header:], columns=columns, dtype=dtype, copy=copy)
            if index > 0:
                df.columns = pd.Index(range(len(df.columns)))
                df.set_index(list(df.columns)[:index], inplace=True)
                df.index.names = pd.Index(value[(header - 1)][:index] if header else [None] * index)
                if header:
                    df.columns = columns[index:]
                else:
                    df.columns = pd.Index(range(len(df.columns)))
            return df

        @classmethod
        def write_value(cls, value, options):
            index = options.get('index', True)
            header = options.get('header', True)
            index_names = value.index.names
            index_names = [ '' if i is None else i for i in index_names ]
            index_levels = len(index_names)
            if index:
                if value.index.name in value.columns:
                    value.index.rename(None, inplace=True)
                value = value.reset_index()
            if header:
                if isinstance(value.columns, pd.MultiIndex):
                    columns = list(zip(*value.columns.tolist()))
                    columns = [ list(i) for i in columns ]
                    if index:
                        for c in columns[:-1]:
                            c[:index_levels] = [
                             ''] * index_levels

                        columns[(-1)][:index_levels] = index_names
                else:
                    columns = [
                     value.columns.tolist()]
                    if index:
                        columns[0][:index_levels] = index_names
                value = columns + value.values.tolist()
            else:
                value = value.values.tolist()
            return value


    PandasDataFrameConverter.register(pd.DataFrame)

    class PandasSeriesConverter(Converter):
        writes_types = pd.Series

        @classmethod
        def read_value(cls, value, options):
            index = options.get('index', 1)
            header = options.get('header', True)
            dtype = options.get('dtype', None)
            copy = options.get('copy', False)
            if header:
                columns = value[0]
                if not isinstance(columns, list):
                    columns = [
                     columns]
                data = value[1:]
            else:
                columns = None
                data = value
            df = pd.DataFrame(data, columns=columns, dtype=dtype, copy=copy)
            if index:
                df.columns = pd.Index(range(len(df.columns)))
                df.set_index(list(df.columns)[:index], inplace=True)
                df.index.names = pd.Index(value[(header - 1)][:index] if header else [None] * index)
            if header:
                df.columns = columns[index:]
            else:
                df.columns = pd.Index(range(len(df.columns)))
            series = df.squeeze()
            if not header:
                series.name = None
                series.index.name = None
            return series

        @classmethod
        def write_value(cls, value, options):
            index_names = value.index.names
            index_names = [ '' if i is None else i for i in index_names ]
            if all(v is None for v in value.index.names) and value.name is None:
                default_header = False
            else:
                default_header = True
            index = options.get('index', True)
            header = options.get('header', default_header)
            value_name = '(' + (', ').join(value.name) + ')' if isinstance(value.name, tuple) else value.name
            if index:
                rv = value.reset_index().values.tolist()
                header_row = [index_names + [value_name]]
            else:
                rv = value.values[:, np.newaxis].tolist()
                header_row = [[value_name]]
            if header:
                rv = header_row + rv
            return rv


    PandasSeriesConverter.register(pd.Series)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p3d3/util.py
# Compiled at: 2018-03-08 05:31:57
# Size of source mod 2**32: 1449 bytes
import numpy as np
from datetime import datetime, timedelta
import pandas as pd, json

def sanitize(df):
    df = df.copy()
    for col_name, dtype in df.dtypes.iteritems():
        if str(dtype) == 'category':
            df[col_name] = df[col_name].astype(str)
        else:
            if np.issubdtype(dtype, np.integer):
                df[col_name] = df[col_name].astype(object)
            else:
                if np.issubdtype(dtype, np.floating):
                    col = df[col_name].astype(object)
                    df[col_name] = col.where(col.notnull(), None)
                else:
                    if str(dtype).startswith('datetime'):
                        df[col_name] = df[col_name].astype(str).replace('NaT', '')

    return df


class P3JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            if isinstance(obj, timedelta):
                return obj.total_seconds()
            if isinstance(obj, pd.DataFrame):
                return obj.to_dict(orient='records')
            return json.JSONEncoder.default(self, obj)
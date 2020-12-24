# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/mlgear/utils.py
# Compiled at: 2019-12-28 18:27:38
# Size of source mod 2**32: 626 bytes
from datetime import datetime
import pandas as pd, numpy as np

def show(df, max_rows=10, max_cols=None, digits=6):
    with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_cols, 'display.float_format', lambda x: '%.{}f'.format(digits) % x):
        print(df)
    if isinstance(df, pd.DataFrame) or isinstance(df, np.ndarray):
        print(df.shape)


def print_step(step):
    print('[{}] {}'.format(datetime.now(), step))


def chunk(l, n):
    out = []
    for i in range(0, len(l), n):
        out.append(l[i:i + n])

    return out
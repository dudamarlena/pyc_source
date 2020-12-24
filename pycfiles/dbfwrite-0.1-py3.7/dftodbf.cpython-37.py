# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dbfwrite\dftodbf.py
# Compiled at: 2020-01-13 01:10:53
# Size of source mod 2**32: 3014 bytes
"""
Created on Mon Dec 23 15:45:22 2019

@author: vane
"""
import struct, datetime, pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_datetime64_dtype
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_float_dtype
from io import BytesIO

def dbfwrite(df, dbffile):
    f = open(dbffile, 'wb')
    file = BytesIO()
    rownum = df.shape[0]
    colnum = df.shape[1]
    fieldname = df.columns.values
    fieldspecs = []
    for name in df.columns.values:
        if is_numeric_dtype(df[name]):
            typ = 'N'
            siz = max(list(df[name].apply(str).apply(len)))
            if is_float_dtype(df[name]):
                d = df[name].apply(lambda x: len(str(x).split('.')[1]))
                deci = max(d)
            else:
                deci = 0
            df[name] = df[name].apply(lambda x: str(x).rjust(siz, ' '))
        else:
            if is_datetime64_dtype(df[name]):
                typ = 'D'
                siz = max(list(df[name].apply(str).apply(len)))
                deci = 0
                df[name] = df[name].apply(lambda x: x.strftime('%Y%m%d'))
            else:
                if is_bool_dtype(df[name]):
                    typ = 'L'
                    siz = max(list(df[name].apply(str).apply(len)))
                    deci = 0
                    df[name] = df[name].apply(lambda x: str(x)[0].upper())
                else:
                    siz = max(list(df[name].apply(str).apply(len)))
                    if siz > 255:
                        typ = 'M'
                    else:
                        typ = 'C'
                    deci = 0
                    df[name] = df[name].apply(lambda x: str(x)[:siz].ljust(siz, ' '))
        fieldinfo = (
         typ, siz, deci)
        fieldspecs.append(fieldinfo)

    version = 3
    now = datetime.datetime.now()
    year = now.year - 1900
    month = now.month
    day = now.day
    recordnum = rownum
    headerlen = colnum * 32 + 33
    recordlen = sum((field[1] for field in fieldspecs)) + 1
    hdr = struct.pack('<BBBBLHH20x', version, year, month, day, recordnum, headerlen, recordlen)
    file.write(hdr)
    for name, (typ, size, deci) in zip(fieldname, fieldspecs):
        name = name.ljust(11, '\x00')
        fld = struct.pack('<11sc4xBB14x', bytes(str(name).encode('utf-8')), bytes(typ.encode('utf-8')), size, deci)
        file.write(fld)

    n = '\r'
    file.write(bytes(str(n).encode('utf-8')))
    for i in range(0, rownum):
        n = ' '
        file.write(bytes(str(n).encode('utf-8')))
        for j in range(0, colnum):
            value = df.iloc[(i, j)]
            file.write(bytes(str(value).encode('utf-8')))

    n = '\x1a'
    file.write(bytes(str(n).encode('utf-8')))
    f.write(file.getvalue())
    f.flush()
    f.close()
    print('Success!')
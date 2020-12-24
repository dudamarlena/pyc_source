# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\lib\dataframe\dfio.py
# Compiled at: 2019-05-29 13:59:12
# Size of source mod 2**32: 1056 bytes
import pandas as pd
from scrapgo.utils.fileutils import get_file_extension
EXCEL_FILE_EXTENSIONS = [
 '.xlsx', '.xls', 'xls', 'xlsx', 'excel']
CSV_FILE_EXTENSIONS = ['.csv', 'csv']

def path2dataframe(path, **kwargs):
    ext = get_file_extension(path)
    if ext in EXCEL_FILE_EXTENSIONS:
        dataframe = pd.read_excel(path)
    else:
        if ext in CSV_FILE_EXTENSIONS:
            dataframe = pd.read_csv(path)
        else:
            raise ValueError(f"The File Extension {ext} is not Supported!")
    return dataframe


def dataframe2path(dataframe, filename, extension='csv', index=False, **kwargs):
    if extension in CSV_FILE_EXTENSIONS:
        path = filename + '.csv'
        (dataframe.to_csv)(path, index=index, **kwargs)
    else:
        if extension in EXCEL_FILE_EXTENSIONS:
            path = filename + '.xlsx'
            (dataframe.to_excel)(path, index=index, **kwargs)
        else:
            if extension is None:
                print(dataframe.head())
            else:
                msg = 'Output file extension must in xlsx, csv'
                raise ValueError(msg)
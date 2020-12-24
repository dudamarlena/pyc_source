# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ax/Workspace/norm/norm/utils.py
# Compiled at: 2019-03-17 19:51:24
# Size of source mod 2**32: 423 bytes
from pandas import DataFrame
from hashids import Hashids
from zlib import adler32
h = Hashids()

def hash_df(df):
    """
    Create a hash string out of a DataFrame data
    :param df: the DataFrame data
    :type df: DataFrame
    :return: the hash string
    :rtype: str
    """
    if df is None:
        return ''
    else:
        return h.encode(adler32(str(df.values).encode('utf-8')))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Mohammed Yusuf Khan\Google Drive\WorkArea\GitHub\toolstack-dev\toolstack\utils\utility_base.py
# Compiled at: 2019-06-29 19:31:30
# Size of source mod 2**32: 781 bytes
import pandas as pd

def available_datasets():
    """
    List of available datasets
    """
    return [
     'Salary',
     'Weather']


def load_dataset(data):
    """
    Load the data from available datasets
    Parameters
    ----------
    data : Dataset Name
        The list of datasets can be found calling the utils.available_datasets()
    Returns
    -------
    DataFrame
    """
    return pd.read_csv('https://raw.githubusercontent.com/getmykhan/toolstack/master/Datasets/' + data + '.csv')


def load_stopwords():
    """
    Default set of stopwords

    Returns
    -------
    Set
    """
    return set(pd.read_csv('https://algs4.cs.princeton.edu/35applications/stopwords.txt', header=(-1))[0].values.tolist())
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victor/Documents/Experiments/test-sphynx/v5/PROJECT/moduleD/matching/search.py
# Compiled at: 2018-02-20 08:47:55
# Size of source mod 2**32: 561 bytes
"""
Module pour chercher des trucs cools (package matching)
"""
import pandas as pd

def search(source, value):
    """Search for value in source database

    Args:
        source (str): database to look into
        value (str): value to look for

    Returns:
        list: occurances found
    """
    return [
     'found it']


def load(dataset):
    """load a dataset as dataframe from its name

    Args:
        dataset (str): path to the dataset

    Returns:
        pd.DataFrame: dataset
    """
    data_frame = pd.DataFrame()
    return data_frame
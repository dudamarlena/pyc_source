# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Alister/miniconda3/envs/obsea/lib/python3.7/site-packages/obsea/datasets.py
# Compiled at: 2019-07-10 06:05:58
# Size of source mod 2**32: 625 bytes
"""
Dataset module.

Used to retrieve the absolut path of toys datasets shiped with obsea.

Attributes
----------
data_path : string
    directory where datasets are stored.

"""
import os, obsea
data_path = os.path.join(os.path.dirname(obsea.__file__), 'data')

def get_dataset_path(dataset):
    """
    Give absolute path of toys datasets.

    Parameters
    ----------
    dataset : string
        Dataset name. Can be 'ais_cls', 'ais_marine_traffic', 'mmsi_list' or
        'station_list'.

    Returns
    -------
    string
        Absolute path.

    """
    return os.path.join(data_path, dataset + '.csv')
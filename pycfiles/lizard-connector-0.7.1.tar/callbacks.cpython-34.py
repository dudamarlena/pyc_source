# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roel.vandenberg/dev/lizard-connector/lizard_connector/callbacks.py
# Compiled at: 2018-04-17 02:55:53
# Size of source mod 2**32: 2538 bytes
"""
Callbacks to be used with lizard_connector.connector.Endpoint().get_async
"""
import json, time, pickle
FILE_BASE = 'api_result'

def no_op(*args, **kwargs):
    pass


def save_to_json(result):
    """
    Saves a result to json with a timestamp in milliseconds.

    Use with Endpoints initialized with the lizard_connector.json parser.

    Args:
        result (list|dict): a json dumpable object to save to file.
    """
    filename = '{}_{}.json'.format(FILE_BASE, str(int(time.time() * 1000)))
    with open(filename, 'w') as (json_filehandler):
        json.dump(result, json_filehandler)


def save_to_pickle(result):
    """
    Pickle a result to file with a timestamp in milliseconds.

    Use with Endpoints initialized with the lizard_connector.json parser.

    Args:
        result (list|dict): a python serializable object to save to file.
    """
    filename = '{}_{}.p'.format(FILE_BASE, str(int(time.time() * 1000)))
    with open(filename, 'w') as (pickle_filehandler):
        pickle.dump(result, pickle_filehandler)


def save_to_hdf5(result):
    """
    Saves a result to hdf5 file with a timestamp in milliseconds.

    Use with Endpoints initialized with the lizard_connector.scientific parser.

    Requires the h5py library for HDF5.

    Args:
        result (tuple[pandas.DataFrame|numpy.array]): a tuple with two elements
            which are either a pandas DataFrame or a numpy array.
    """
    filename = '{}_{}.h5'.format(FILE_BASE, str(int(time.time() * 1000)))
    try:
        import h5py, pandas as pd
    except ImportError:
        raise ImportError('When the save_to_hdf5 callback is used, make sureh5py, pandas and numpy are installed.')

    result.metadata.to_hdf(filename, 'metadata')
    for i, ds in enumerate(result.data):
        if ds:
            dataset_name = 'data_{}'.format(i)
            if isinstance(ds, pd.DataFrame):
                ds.to_hdf(filename, dataset_name)
            with h5py.File(filename, 'w', libver='latest') as (h5_file):
                if ds.dtype.kind == 'O':
                    print(ds)
                    dtype = str
                    ds = ds.astype(dtype)
                else:
                    dtype = ds.dtype
                dataset = h5_file.create_dataset(dataset_name, ds.shape, dtype=dtype)
                dataset[...] = ds
            continue
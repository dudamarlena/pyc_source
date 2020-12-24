# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/features/utils.py
# Compiled at: 2017-02-22 11:30:12
# Size of source mod 2**32: 2872 bytes
"""
Utility tools for the feature extraction.
"""
import os, logging, pickle, glob, numpy as np, pandas as pd
from gsitk import config
logger = logging.getLogger(__name__)
features_path = os.path.join(config.DATA_PATH, 'features/')
format_exts = {'numpy': '.npy', 
 'pickle': 'pck'}

def detect_saving_format(filename):
    ext = os.path.splitext(filename)[1]
    if ext == '.npy':
        return 'numpy'
    else:
        return 'pickle'


def _read_numpy_ndarray(name):
    path = os.path.join(features_path, name)
    with open(path, 'r') as (f):
        array = np.load(path)
    return array


def _read_pandas_dataframe(name):
    path = os.path.join(features_path, name)


def _read_pickle(name):
    path = os.path.join(features_path, name)
    with open(path, 'rb') as (f):
        from_pickle = pickle.loads(f)
    return from_pickle


def _save_numpy_ndarray(array, path):
    """Save a numpy ndarray"""
    np.save(path, array)


def _save_pandas_dataframe(dataframe, path):
    """Save a pandas dataframe"""
    dataframe.to_pickle(path)


def _save_as_pickle(to_pickle, path):
    """Save features as pickle"""
    with open(path, 'wb') as (f):
        pickle.dump(to_pickle, f)


def save_features(features, name):
    """Save the features in the <data_folder>/features directory."""
    if not os.path.exists(features_path):
        logger.debug('{} path does not exist. Creating...'.format(features_path))
        os.makedirs(features_path)
    path = os.path.join(config.DATA_PATH, 'features/', name)
    if isinstance(features, np.ndarray):
        _save_numpy_ndarray(features, path)
    else:
        if isinstance(features, pd.DataFrame):
            _save_pandas_dataframe(features, path)
        else:
            _save_as_pickle(features, path)


def read_features(name, format=None):
    """Read the features stored in path."""
    path = os.path.join(features_path, name)
    logger.debug('Reading features from {}'.format(name))
    paths = glob.glob(path + '*')
    if len(paths) > 1:
        if format is not None:
            if format in format_exts.keys():
                path = glob.glob(path + format_exts[format])
            else:
                raise ValueError('Format parameter is not valid. Choose between: {}'.format(format_exts.keys()))
        else:
            raise ValueError('I cannot decide which features you want. Try especifying a format.')
    else:
        path = paths[0]
    logger.debug('Features are in {}'.format(path))
    if not os.path.exists(path):
        raise ValueError('Given path does not exist.')
    format = detect_saving_format(path)
    if format == 'numpy':
        return _read_numpy_ndarray(path)
    else:
        return _read_pickle(path)


def _check_features(name, format):
    response = '- {} => format: {}'.format(name, format)
    return response
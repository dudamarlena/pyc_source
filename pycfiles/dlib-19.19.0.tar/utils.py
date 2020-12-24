# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davis/source/dlib/tools/python/test/utils.py
# Compiled at: 2019-03-10 12:46:09
import pkgutil, sys

def save_pickled_compatible(obj_to_pickle, file_name):
    """
        Save an object to the specified file in a backward compatible
        way for Pybind objects. See:
        http://pybind11.readthedocs.io/en/stable/advanced/classes.html#pickling-support
        and https://github.com/pybind/pybind11/issues/271
    """
    try:
        import cPickle as pickle
    except ImportError:
        import pickle

    data = pickle.dumps(obj_to_pickle, 2)
    with open(file_name, 'wb') as (handle):
        handle.write(data)


def load_pickled_compatible(file_name):
    """
        Loads a pickled object from the specified file
    """
    try:
        import cPickle as pickle
    except ImportError:
        import pickle

    with open(file_name, 'rb') as (handle):
        data = handle.read()
        if not is_python3():
            return pickle.loads(data)
        return pickle.loads(data, encoding='bytes')


def is_numpy_installed():
    """
        Returns True if Numpy is installed otherwise False
    """
    if pkgutil.find_loader('numpy'):
        return True
    else:
        return False


def is_python3():
    """
        Returns True if using Python 3 or above, otherwise False
    """
    return sys.version_info >= (3, 0)
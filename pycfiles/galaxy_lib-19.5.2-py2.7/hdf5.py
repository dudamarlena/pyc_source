# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/verify/asserts/hdf5.py
# Compiled at: 2019-04-28 04:54:30
import io
try:
    import h5py
except ImportError:
    h5py = None

IMPORT_MISSING_MESSAGE = 'h5 assertion requires unavailable optional dependency h5py'

def _assert_h5py():
    if h5py is None:
        raise Exception(IMPORT_MISSING_MESSAGE)
    return


def assert_has_h5_attribute(output_bytes, key, value):
    """Asserts the specified HDF5 output has a given key-value pair as HDF5
    attribute"""
    _assert_h5py()
    output_temp = io.BytesIO(output_bytes)
    local_attrs = h5py.File(output_temp, 'r').attrs
    assert key in local_attrs and str(local_attrs[key]) == value, 'Not a HDF5 file or H5 attributes do not match:\n\t%s\n\n\t(%s : %s)' % (local_attrs.items(), key, value)


def assert_has_h5_keys(output_bytes, keys):
    """ Asserts the specified HDF5 output has exactly the given keys."""
    _assert_h5py()
    keys = [ k.strip() for k in keys.strip().split(',') ]
    h5_keys = sorted(keys)
    output_temp = io.BytesIO(output_bytes)
    local_keys = sorted(list(h5py.File(output_temp, 'r').keys()))
    assert local_keys == h5_keys, 'Not a HDF5 file or H5 keys do not match:\n\t%s\n\t%s' % (local_keys, h5_keys)
# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hdf5_matlab_reader/matlab_reader.py
# Compiled at: 2016-03-22 17:43:40
# Size of source mod 2**32: 6021 bytes
from __future__ import division, print_function
import sys, h5py, numpy as np
from scipy import sparse
from functools import partial
from hdf5_matlab_reader.empty_matrix import EmptyMatrix

def loadmat(f):
    h5_file = h5py.File(f, 'r')
    return extract_file(h5_file)


def extract_file(f):

    def avoid_refs(kv):
        k, v = kv
        return not k.startswith('#refs#')

    return {k:extract_element(f, v) for k, v in filter(avoid_refs, f.items())}


def extract_element(f, element):
    if type(element) is h5py._hl.dataset.Dataset:
        return extract_dataset(f, element)
    if type(element) is h5py._hl.group.Group:
        return extract_group(f, element)
    raise NotImplementedError('Unimplemented HDF5 structure')


def extract_group(f, group):
    if 'MATLAB_sparse' in group.attrs:
        return extract_sparse(f, group)
    return {k:extract_element(f, v) for k, v in group.items()}


def extract_dataset(f, dataset):
    if 'MATLAB_class' not in dataset.attrs:
        return dataset.value
    else:
        data_class = dataset.attrs['MATLAB_class']
        if data_class == 'struct' and 'MATLAB_empty' in dataset.attrs:
            return {}
        if 'MATLAB_empty' in dataset.attrs and dataset.attrs['MATLAB_empty'] == 1:
            return EmptyMatrix(shape=dataset.value, dtype=data_class)
        if data_class in ('double', 'single', 'int8', 'uint8', 'int16', 'uint16', 'int32',
                          'uint32', 'int64', 'uint64'):
            return dataset.value
        else:
            if data_class == 'logical':
                return dataset.value.astype(bool)
            if data_class == 'cell':
                return extract_cell(f, dataset)
            if data_class == 'char':
                pass
            return extract_string(dataset)
        if data_class in ('categorical', 'datetime', 'containers.Map', 'table'):
            pass
        return dataset.value
    if data_class == 'FileWrapper__':
        return extract_cell(f, dataset)


def extract_sparse(f, group):
    data = group['data'].value
    rows = group['ir'].value
    cols = group['jc'].value
    mtype = group.attrs['MATLAB_class']
    nr = group.attrs['MATLAB_sparse']
    nc = len(cols) - 1
    ne = len(rows)
    compress_col = [np.where(cols == i)[0][(-1)] for i in np.arange(ne)]
    return sparse.coo_matrix((data, (rows, compress_col)), shape=(nr, nc), dtype=bool if mtype == 'logical' else None)


def indexarg(f, arg):
    """
    clearly it is more important to be pythonic than straightforward
    """
    return f[arg]


def extract_cell(f, dataset):
    """
    behold the elegance and simplicity of recursion
    """
    return np.squeeze(map_ndlist(partial(extract_element, f), map(partial(map_ndarray, partial(indexarg, f)), dataset.value)))


def bytearray_to_string(z):
    return ''.join(map(unichr, z))


def is_ndim_list(ndlist):
    return list in map(type, ndlist)


def extract_string(dataset):
    string_k = partial(map_ndarrays, bytearray_to_string)
    str_array = string_k(np.transpose(dataset.value))
    if len(str_array) == 1:
        return str_array[0]
    else:
        return str_array


def map_ndlist(k, ndlist):
    """
    like map, but operates on every element of n-dimensional python list
    """
    if type(ndlist) == list:
        return map(partial(map_ndlist, k), ndlist)
    else:
        return k(ndlist)


def map_ndarray(k, ndarray):
    """
    like map, but operates on every element of n-dimensional np.ndarray
    """
    if ndarray.ndim > 1:
        return map(partial(map_ndarray, k), ndarray)
    else:
        return map(k, ndarray)


def map_ndlists(k, ndlists):
    """
    like map, but operates on every lowest-dim list of n-dimensional list
    """
    if is_ndim_list(ndlists):
        return map(partial(map_ndlist, k), ndlist)
    else:
        return k(ndlist)


def map_ndarrays(k, ndarray):
    """
    like map, but operates on every lowest-dim list of n-dimensional np.ndarray
    """
    if ndarray.ndim > 1:
        return map(partial(map_ndarrays, k), ndarray)
    else:
        return k(ndarray)


if __name__ == '__main__':
    matfile = sys.argv[1]
    try:
        h5_file = h5py.File(matfile, 'r')
        mat_out = extract_file(h5_file)
        print(mat_out)
        for k, v in mat_out.items():
            print(k, np.shape(v))

        import pdb
        pdb.set_trace()
    except Exception as e:
        print('{0}: {1}'.format(type(e), e))
        import pdb
        pdb.set_trace()
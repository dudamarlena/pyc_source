# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bigmpi4py/bigmpi4py.py
# Compiled at: 2019-01-19 14:12:43
# Size of source mod 2**32: 63759 bytes
"""
================================
Toolbox
================================

This file contains many functions that will be shared through several files.
"""
import pandas as pd, numpy as np, time, sys, os, itertools, gc, sys, inspect
from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass

import pandas as pd, itertools
from mpi4py import MPI
from psutil import virtual_memory
dict_emptythings = {pd.DataFrame: pd.DataFrame(), np.ndarray: np.array([]), list: [], str: '', 
 int: 0, float: 0.0, dict: {}, set: (), pd.Series: pd.Series(), type(None): None}

def _get_size_object(this):
    if isinstance(this, np.ndarray):
        return this.nbytes
    else:
        if isinstance(this, list):
            sum = 0
            for i in this:
                if isinstance(i, np.ndarray):
                    sum += i.nbytes
                else:
                    sum += sys.getsizeof(i)

            return sum
        else:
            if isinstance(this, pd.DataFrame):
                return this.values.nbytes + this.index.values.nbytes + this.columns.values.nbytes
            if isinstance(this, pd.Series):
                return this.values.nbytes + this.index.values.nbytes
        return sys.getsizeof(this)


def _is_istring_cols(scatter_object, by_col):
    string_cols = False
    if isinstance(scatter_object, (pd.DataFrame, pd.Series)):
        string_cols = True
        cols = scatter_object.columns.tolist()
        for i in by_col:
            if i not in cols:
                string_cols = False
                break

    return string_cols


def _return_set_type(set_object):
    """
    Given a set with object types, return if it is "simple" (0), "complex" (1) or "mixed" (2)
    """
    issimple, iscomplex = (False, False)
    simple_types = [int, float, str, bool]
    complex_types = [list, np.ndarray, pd.Series, pd.DataFrame, set]
    for i in set_object:
        if type(i) in simple_types:
            issimple = True
            break
        else:
            if type(i) in complex_types:
                iscomplex = True
                break
            else:
                try:
                    doesdiswork = 0 == i * 0
                    issimple = True
                except:
                    raise TypeError('{} is not recognized so far.'.format(i))

    if issimple:
        if not iscomplex:
            return 0
    if iscomplex:
        if not issimple:
            return 1
    return 2


def _return_values_df(scatter_object):
    if isinstance(scatter_object, (pd.DataFrame, pd.Series)):
        return scatter_object.values
    else:
        return scatter_object


def _generate_index_list(scatter_object, by_col):
    """
    This function generates a list with index combination of all elements within
    each category (column) of by_col variable.

    :return: Nested list with index combination.
    """
    string_cols = _is_istring_cols(scatter_object, by_col)
    if string_cols:
        dict_categories = {i:list(dict.fromkeys(_return_slice(scatter_object, col_0=i, string_cols=True).values.tolist())) for i in by_col}
    else:
        if isinstance(scatter_object, pd.DataFrame):
            cols = scatter_object.columns.tolist()
            dict_categories = {i:list(dict.fromkeys(_return_slice(scatter_object, col_0=i, col_f=(i + 1))[cols[i]].values.tolist())) for i in by_col}
        else:
            dict_categories = {i:list(dict.fromkeys(_return_slice(scatter_object, col_0=i, col_f=(i + 1)).flatten().tolist())) for i in by_col}
    dict_categories_lens = {i:len(dict_categories[i]) for i in dict_categories.keys()}
    list_dict_categories_idx = [i - 1 for i in list(dict_categories_lens.values())]
    list_dict_categories_keys = list(dict_categories.keys())
    nested_list_idx = []
    while list_dict_categories_idx[0] >= 0:
        loop_combination_idx_list = []
        for i in range(len(list_dict_categories_idx)):
            loop_combination_idx_list.append(dict_categories[list_dict_categories_keys[i]][list_dict_categories_idx[i]])

        nested_list_idx.append(loop_combination_idx_list)
        list_dict_categories_idx[(-1)] -= 1
        for idx in range(len(list_dict_categories_idx) - 1, 0, -1):
            if -1 in list_dict_categories_idx:
                list_dict_categories_idx[idx] = dict_categories_lens[list_dict_categories_keys[idx]] - 1
                list_dict_categories_idx[(idx - 1)] -= 1
            else:
                break

    return (
     nested_list_idx, list_dict_categories_keys)


def _is_vable(optimize, scatter_object):
    numpy = False
    if isinstance(scatter_object, np.ndarray):
        if scatter_object.dtype.kind in ('u', 'i', 'f', 'b'):
            numpy = True
    return optimize & numpy | (type(scatter_object) == type(None))


def _merge_objects(list_objects, delete=False):
    """
    Given a list with objects, merges them into one single object, provided all elements of the list
    are of the same type.

    :param list_objects: List with objects to merge.
    :param delete: If `True`, deletes list_objects
    :return: merged object
    """
    if list_objects == None:
        return
    else:
        if type(list_objects[0]) in [pd.DataFrame, pd.Series]:
            table_return = pd.concat(list_objects, copy=False)
        else:
            if isinstance(list_objects[0], np.ndarray):
                n_rows = sum([len(i) for i in list_objects])
                i_row = 0
                if list_objects[0].ndim >= 2:
                    table_return = np.empty(((n_rows,) + np.shape(list_objects[0])[1:]), dtype=(list_objects[0].dtype))
                else:
                    table_return = np.empty(n_rows, dtype=(list_objects[0].dtype))
                for i in list_objects:
                    if len(i) > 0:
                        if list_objects[0].ndim > 1:
                            table_return[i_row:i_row + len(i), :] = i
                        else:
                            table_return[i_row:i_row + len(i)] = i
                        i_row += len(i)

            else:
                if isinstance(list_objects[0], list):
                    table_return = list(itertools.chain.from_iterable(list_objects))
                    for i in reversed(table_return):
                        if _return_set_type((i,)) == 0:
                            pass
                        elif len(i) == 0:
                            table_return.remove(i)

        if delete:
            del list_objects
        return table_return


def _return_slice(object_slice, row_0=0, row_f=None, col_0=0, col_f=None, string_cols=False):
    if isinstance(object_slice, (pd.DataFrame, pd.Series, np.ndarray)):
        if row_f == None:
            row_f = object_slice.shape[0]
        elif col_f == None:
            col_f = object_slice.shape[1]
    if isinstance(object_slice, pd.DataFrame):
        if string_cols & (col_0 in object_slice.columns.tolist()):
            return object_slice[col_0].iloc[row_0:row_f]
        else:
            return object_slice.iloc[row_0:row_f, col_0:col_f]
    else:
        if isinstance(object_slice, np.ndarray):
            if object_slice.ndim > 1:
                return object_slice[row_0:row_f, col_0:col_f]
            else:
                return object_slice[row_0:row_f]
        else:
            if isinstance(object_slice, pd.Series):
                return object_slice.iloc[row_0:row_f]
    if isinstance(object_slice, list):
        return object_slice[row_0:row_f]


def _return_idx_list_k1(idx_list, scatter_object, size, size_limit):
    """
    Given a scatter object and a idx list of locations to cut that object, return
    the maximum k value of all the objects in the division list, as well as the new division of
    the object in a list.

    :param idx_list: List with indexes of object cutting.
    :type idx_list: list
    :param scatter_object: Object to be cut.
    :type scatter_object: Defined in `scatter()`function.
    :param size: comm.size, number of processors.
    :type size: int
    :param size_limit: limit of memory allocated to each element.
    :type size_limit: int
    :return: k value.
    :type return: int
    :return: idx list.
    :type return: list
    """
    idx_list_sizes = [_get_size_object(_return_slice(scatter_object, idx_list[i], idx_list[(i + 1)])) for i in range(len(idx_list) - 1)]
    k = int(max([i / size_limit for i in idx_list_sizes])) + 1
    idx_list_k = []
    for i in range(len(idx_list) - 1):
        idx_list_k += [int(z) for z in np.linspace(idx_list[i], idx_list[(i + 1)], k + 1)][:-1]

    idx_list_k += [len(scatter_object)]
    return (
     k, idx_list_k)


def _return_k2(scatter_object, size_limit):
    """
    Returns the k2 value of an object; concretely, a list with objects.

    :param scatter_object: list from which k2 must be obtained.
    :type scatter_object: list

    :param size_limit: limit of memory for each processor.
    :type size_limit: int

    :return: k2 value
    :type return: int
    """
    list_object_sizes = [_get_size_object(i) for i in scatter_object]
    k2 = int(max([i / size_limit for i in list_object_sizes])) + 1
    return k2


def _cut_in_k_parts(scatter_object, k, size, idx_list_k1=[]):
    """
    Given a scatter object and a k value, cuts the object into k parts, trying to keep the same
    length for all the objects.

    :param scatter_object: Object to be cut.
    :type scatter_object: Defined in `scatter()`function.
    :param k: k value.
    :type k: list
    :param size: number of processors
    :type size: int
    :param idx_list_k1: list with custom cutting indexes
    :type idx_list_k1: list
    :return: cut object.
    :type return: list
    """
    k1, k2 = k[0], k[1]
    if len(idx_list_k1) == 0:
        idx_list_k1 = [int(i) for i in np.linspace(0, len(scatter_object), size * k1 + 1)]
    else:
        scatter_list_objects_k1 = [_return_slice(scatter_object, idx_list_k1[i], idx_list_k1[(i + 1)]) for i in range(len(idx_list_k1) - 1)]
        if k[1] <= 1:
            scatter_list_objects = scatter_list_objects_k1
        else:
            scatter_list_objects = [[
             [dict_emptythings[type(scatter_object[0])] for y in range(k2)]] for x in range(k1 * size)]
            k_i = 0
            while scatter_list_objects_k1:
                obj_k2 = []
                for obj in scatter_list_objects_k1[0]:
                    idx_list_k2 = [int(i) for i in np.linspace(0, len(obj), k2 + 1)]
                    obj_k2.append([_return_slice(obj, idx_list_k2[i], idx_list_k2[(i + 1)]) for i in range(len(idx_list_k2) - 1)])

                if len(obj_k2) > 0:
                    scatter_list_objects[k_i] = obj_k2
                del scatter_list_objects_k1[0]
                k_i += 1

    return scatter_list_objects


def _scatterv(object, comm, root=0):
    """
    Generalized function that automatically uses `comm.Scatterv()` or `comm.scatter()` depending
    on the data type. If the array is numeric, it does so. If the array is not numeric, or it
    is not an array of the class `numpy.ndarray`, it redirects the scattering to do `comm.scatter()`.

    :param object: object to be scattered.
    :type object: `scatter()` object type.
    :param comm: MPI.COMM_WORLD object
    :type comm: MPI.COMM_WORLD object
    :param root: root process
    :type root: int
    :param optimize_scatter: If True, uses `comm.Scaterv()` command with numerical arrays.
    :type optimize_scatter: bool
    :return: Scattered object
    """
    if comm.rank == root:
        if isinstance(object, list):
            counts = [i.size for i in object]
            displs = [0] + list(np.cumsum(counts))
            lens = [len(i) for i in object]
            object = _merge_objects(object)
        else:
            if object.ndim > 1:
                displs = [int(i) * int(object.size / object.shape[0]) for i in np.linspace(0, object.shape[0], comm.size + 1)]
            else:
                displs = [int(i) for i in np.linspace(0, object.shape[0], comm.size + 1)]
            counts = [displs[(i + 1)] - displs[i] for i in range(len(displs) - 1)]
            if object.ndim > 1:
                lens = [int((displs[(i + 1)] - displs[i]) / object.shape[1]) for i in range(len(displs) - 1)]
            else:
                lens = [displs[(i + 1)] - displs[i] for i in range(len(displs) - 1)]
        displs = displs[:-1]
        shape = object.shape
        object_type = object.dtype
        if object.ndim > 1:
            object = object.ravel().astype((np.float64), copy=False)
    else:
        object, counts, displs, shape, lens, object_type = (None, None, None, None,
                                                            None, None)
    counts = comm.bcast(counts, root=root)
    displs = comm.bcast(displs, root=root)
    lens = comm.bcast(lens, root=root)
    shape = list(comm.bcast(shape, root=root))
    object_type = comm.bcast(object_type, root=root)
    shape[0] = lens[comm.rank]
    shape = tuple(shape)
    x = np.zeros(counts[comm.rank])
    comm.Scatterv([object, counts, displs, MPI.DOUBLE], x, root=root)
    del object
    if len(shape) > 1:
        return np.reshape(x, (-1, ) + shape[1:]).astype(object_type, copy=False)
    else:
        return x.view(object_type)


def _gatherv(object, comm, root, optimize, k1_val):
    """
       Generalized function that automatically uses `comm.Gatherv()` or `comm.gather()` depending
       on the data type. If the array is numeric, it does so. If the array is not numeric, or it
       is not an array of the class `numpy.ndarray`, it redirects the scattering to do `comm.gather()`.

       :param object: object to be scattered.
       :type object: `gather()` object type.
       :param comm: MPI.COMM_WORLD object
       :type comm: MPI.COMM_WORLD object
       :param root: root process
       type root: int
       :return: Scattered object
       """
    optimize_scatter, object_type = (0, None)
    if comm.rank == root:
        if isinstance(object, np.ndarray) & optimize:
            if object.dtype in [np.float64, np.float32, np.float16, np.float,
             np.int, np.int8, np.int16, np.int32, np.int64, int, float,
             bool]:
                optimize_scatter = 1
                object_type = object.dtype
        else:
            optimize_scatter = comm.bcast(optimize_scatter, root=root)
            object_type = comm.bcast(object_type, root=root)
            if optimize_scatter == 1:
                counts = object.size
                lens = object.shape[0]
                shape = list(object.shape)
                if object.ndim > 1:
                    object = object.ravel().astype((np.float64), copy=False)
                counts = comm.allgather(counts)
                lens = comm.gather(lens, root=root)
                displs = None
                if comm.rank == root:
                    displs = [sum(counts[:i]) for i in range(len(counts))]
                    shape[0] = sum(lens)
                    shape = tuple(shape)
                if comm.rank == root:
                    x = np.zeros((sum(counts)), dtype=(np.float64))
                else:
                    x = None
                comm.Gatherv([object, counts[comm.rank]], [x, counts, displs, MPI.DOUBLE], root=root)
                if comm.rank == root:
                    if len(shape) > 1:
                        return_obj = np.reshape(x, (-1, ) + shape[1:]).astype(object_type, copy=False)
                        if k1_val == 1:
                            return return_obj
                        else:
                            lens = [
                             0] + list(np.cumsum(lens))
                            return [return_obj[lens[i]:lens[(i + 1)]] for i in range(len(lens) - 1)]
                    else:
                        return_obj = x.view(object_type)
                        if k1_val == 1:
                            return return_obj
                else:
                    lens = [
                     0] + list(np.cumsum(lens))
                    return [return_obj[lens[i]:lens[(i + 1)]] for i in range(len(lens) - 1)]
            else:
                return x
    else:
        return comm.gather(object, root=root)


def _gather_or_allgather(object, comm, root, type_gather='gather', optimize=True, k1_val=1):
    if type_gather == 'gather':
        return _gatherv(object, comm, root, optimize, k1_val)
    if type_gather == 'allgather':
        return comm.allgather(object)


def _general_scatter(scatter_object, comm, by, dest, size_limit, root, optimize, scatter_method):
    """
    This function is a more generalised form of the comm.scatter() function, prepared for arrays
    of any size.

    :param scatter_object: Object to be divided.
    :type scatter_object: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                          `pd.DataFrame` or `np.ndarray` objects. If a list of objects is passed
                          objects must all of them be [int, float, str] or [pd.DataFrame, np.array].
                          Lists with elements of mixed classes are yet not supported.

    :param comm: MPI4PY's MPI.COMM_WORLD object.

    :param by: If the table cannot be directly divided by rows and, instead, there are some
               categorical variables that are stored within a column/s in the
               `pd.DataFrame`/`np.ndarray` object, `scatter` can perform the subdivision based
               on this variable.  For instance, it the column has 1000 genes (several rows per
               gene), and the # of processors is 10, each processor will have 100 genes. So far,
               only one `by` variable can be attributed. The table must be sorted by this
    :type by: int (`np.ndarray`) or str (`pd.Dataframe`).

    :param size_limit: maximum byte size allowed for each divisible object. If the size exceeds the
                       size limit, the chunk will be divided in `k`subchunks.
    :type size_limit: int

    :param root: processor from which the object has been created.
    :type root: int

    :param scatter_method: ['scatter' | 'bcast']. If 'scatter', divides de object and distributes it
                            into the processors. If 'bcast', sends a copy of the object to all
                            processors.

    :return: i-th subtable for processor i, already parallelized.
    :type return: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                  `pd.DataFrame` or `np.ndarray` objects.
    """
    rank = comm.rank
    size = comm.size
    scatter_object_type = type(scatter_object)
    tag = 4568121
    if type(by) != list:
        by = [
         by]
    size_limit = size_limit / size
    if size == 1:
        return scatter_object
    else:
        if rank == root:
            if scatter_method in ('sendrecv', ):
                size = 1
                by = []
            if type(scatter_object) in [pd.DataFrame, np.ndarray, pd.Series]:
                by_col = by if by != [] else []
                scatter_object_nrows = scatter_object.shape[0]
                if len(by_col) > 0:
                    idx_list = []
                    nested_list_values, list_categories_keys = _generate_index_list(scatter_object, by_col)
                    string_cols = _is_istring_cols(scatter_object, by_col)
                    for value_comb in nested_list_values:
                        for i in range(len(value_comb)):
                            if string_cols:
                                col_f = by_col[i]
                            else:
                                col_f = by_col[i] + 1
                            bool_array_i = _return_slice(scatter_object, col_0=(by_col[i]), col_f=col_f,
                              string_cols=string_cols) == value_comb[i]
                            if i == 0:
                                if isinstance(bool_array_i, (pd.DataFrame, pd.Series)):
                                    bool_array = bool_array_i.values
                                else:
                                    bool_array = bool_array_i
                            else:
                                if isinstance(bool_array_i, (pd.DataFrame, pd.Series)):
                                    bool_array = bool_array & bool_array_i.values
                                else:
                                    bool_array = bool_array & bool_array_i

                        bool_to_idx = np.argwhere(bool_array.flatten()).flatten()
                        if len(bool_to_idx) > 0:
                            idx_list.append(int(min(bool_to_idx)))

                    idx_list.append(len(scatter_object))
                    idx_list = sorted(idx_list)
                    lsp = np.linspace(0, len(idx_list) - 1, size + 1)
                    idx_list = [idx_list[int(i)] for i in lsp]
                    k, idx_list_k = _return_idx_list_k1(idx_list, scatter_object, size, size_limit)
                else:
                    lsp = np.linspace(0, scatter_object_nrows, size + 1)
                    idx_list = [int(i) for i in lsp]
                    k, idx_list_k = _return_idx_list_k1(idx_list, scatter_object, size, size_limit)
            else:
                if _is_vable(optimize, scatter_object) & (k == 1):
                    scatter_list_objects = scatter_object
                else:
                    scatter_list_objects = [_return_slice(scatter_object, idx_list_k[i], idx_list_k[(i + 1)]) for i in range(len(idx_list_k) - 1)]
        else:
            if type(scatter_object) == list:
                set_type = _return_set_type(scatter_object)
                if set_type == 2:
                    raise TypeError('The list to be scattered cannot contain simple types (int, float, str) and complex types (pd.DataFrame, np.ndarray, list) mixed together.')
                else:
                    if set_type == 0:
                        idx_list = [int(i) for i in np.linspace(0, len(scatter_object), size + 1)]
                        k, idx_list_k = _return_idx_list_k1(idx_list, scatter_object, size, size_limit)
                        scatter_list_objects = [scatter_object[idx_list_k[i]:idx_list_k[(i + 1)]] for i in range(len(idx_list_k) - 1)]
                    else:
                        if set_type == 1:
                            idx_list = [int(i) for i in np.linspace(0, len(scatter_object), size + 1)]
                            k2 = _return_k2(scatter_object, size_limit)
                            if k2 == 1:
                                k1, idx_list_k1 = _return_idx_list_k1(idx_list, scatter_object, size, size_limit)
                            else:
                                k1, idx_list_k1 = 1, idx_list
                            k = [k1, k2]
                            scatter_list_objects = _cut_in_k_parts(scatter_object, k, size, idx_list_k1)
                        else:
                            raise TypeError('The object types ({}) are not allowed so far.'.format(set_types))
            else:
                if type(k) != list:
                    k = [
                     k, 1]
                else:
                    k, scatter_list_objects, idx_list = (None, None, None)
                k = comm.scatter(([k] * comm.size), root=root)
                k1, k2 = k[0], k[1]
                is_vable = _is_vable(optimize, scatter_object)
                is_vable = np.all(comm.allgather(is_vable))
                if k2 > 1:
                    if rank == root:
                        if is_vable:
                            pass
                        else:
                            table_list_k_i = [scatter_list_objects[i] for i in range(0, k1 * size, k1)]
                    else:
                        table_list_k_i = None
                    merge_table_k_i_j = []
                    for k_2 in range(k2):
                        if rank == root:
                            table_k_i_j = []
                            for z in table_list_k_i:
                                i_j_z = []
                                for l in range(len(z)):
                                    i_j_z.append(z[l][k_2])

                                table_k_i_j.append(i_j_z)

                        else:
                            table_k_i_j = None
                        if scatter_method == 'scatter':
                            table_k_i_j = comm.scatter(table_k_i_j, root=root)
                        else:
                            if scatter_method == 'sendrecv':
                                if rank == root:
                                    comm.send((table_k_i_j[0]), dest=dest, tag=tag)
                                if rank == dest:
                                    table_k_i_j = comm.recv(source=root, tag=tag)
                        merge_table_k_i_j.append(table_k_i_j)

                    if scatter_method == 'sendrecv':
                        object_return = [] if comm.rank == dest else None
                        if rank == dest:
                            for l in range(len(merge_table_k_i_j[0])):
                                object_return.append(_merge_objects([merge_table_k_i_j[k][l] for k in range(len(merge_table_k_i_j))]))

                            return object_return
                        else:
                            return
                    else:
                        if scatter_method == 'scatter':
                            object_return_not_merged = [[[] for y in range(0)] for x in range(len(merge_table_k_i_j[0]))]
                            for l in range(len(merge_table_k_i_j[0])):
                                object_return_not_merged[l] = [
                                 _merge_objects([merge_table_k_i_j[k_2][l] for k_2 in range(len(merge_table_k_i_j))])]

                else:
                    if scatter_method == 'scatter':
                        object_return_not_merged = [[[] for y in range(0)] for x in range(k1)]
                    else:
                        if scatter_method == 'sendrecv':
                            object_return_not_merged = [[[] for y in range(0)] for x in range(k1)] if rank == dest else None
                        for k_i in range(k1):
                            if rank == root:
                                if is_vable & (k[0] == 1):
                                    pass
                                else:
                                    table_list_k_i = [scatter_list_objects[i] for i in range(0, k1 * size, k1)]
                            else:
                                table_list_k_i = None
                            if scatter_method == 'scatter':
                                if is_vable:
                                    if k[0] == 1:
                                        object_return_not_merged[k_i] = _scatterv(scatter_object, comm, root=root)
                                    else:
                                        object_return_not_merged[k_i] = _scatterv(table_list_k_i, comm, root=root)
                                else:
                                    object_return_not_merged[k_i] = comm.scatter(table_list_k_i, root=root)
                            else:
                                if scatter_method == 'sendrecv':
                                    if rank == root:
                                        comm.send((table_list_k_i[0]), dest=dest, tag=tag)
                                    if rank == dest:
                                        object_return_not_merged[k_i] = comm.recv(source=root, tag=tag)
                                if rank == root:
                                    try:
                                        for k_del in reversed(sorted(list(range(0, k1 * size, k1)))):
                                            del scatter_list_objects[k_del]

                                    except:
                                        del scatter_list_objects

                                k1 -= 1

            if is_vable & (k1 == 1):
                object_return = object_return_not_merged[0]
            else:
                object_return = _merge_objects(object_return_not_merged, delete=True)
        return object_return


def _general_gather(gather_object, comm, size_limit, root, optimize, gather_method):
    """
    This function is a more generalised form of the comm.gather() function, prepared for arrays
    of any size.

    :param gather_object: Object to be gathered.
    :type gather_object: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                          `pd.DataFrame` or `np.ndarray` objects. If a list of objects is passed
                          objects must all of them be [int, float, str] or [pd.DataFrame, np.array].
                          Lists with elements of mixed classes are yet not supported.

    :param comm: MPI4PY's MPI.COMM_WORLD object.

    :param size_limit: maximum byte size allowed for each divisible object. If the size exceeds the
                       size limit, the chunk will be divided in `k`subchunks.
    :type size_limit: int

    :gather_method: ['gather' | 'allgather']. If `gather`, returns the object to the "root"
                    processor. If `allgather`, all processors receive a copy of the gathered object.
    :type gather_method: str

    :param root: if `gather`, processor that will receive the gathered object.
    :type root: int

    :return: object from gathered subobjects.
    :type return: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                  `pd.DataFrame` or `np.ndarray` objects.
    """
    rank, size = comm.rank, comm.size
    size_limit = size_limit / size
    if size == 1:
        return gather_object
    else:
        if (type(gather_object) == list) & (_return_set_type(gather_object) == 1):
            k2 = _return_k2(gather_object, size_limit)
        else:
            k2 = 1
        if k2 == 1:
            k1, idx_list_k1 = _return_idx_list_k1([0, len(gather_object)], gather_object, size, size_limit)
        else:
            k1 = 1
        k1 = max(comm.allgather(k1))
        k2 = max(comm.allgather(k2))
        if k2 > 1:
            k1 = 1
        else:
            idx_list_k1 = [int(z) for z in np.linspace(0, len(gather_object), k1 + 1)]
        if (k1 == 1) & (k2 == 1):
            object_return = _gather_or_allgather(gather_object, comm, root, gather_method, optimize=optimize)
        else:
            if k1 > 1:
                object_return = [None] * (k1 * size) if rank == root else None
                for k_i in range(k1):
                    object_return_k_i = _gather_or_allgather((gather_object[idx_list_k1[k_i]:idx_list_k1[(k_i + 1)]]), comm,
                      root, gather_method, k1_val=k1, optimize=optimize)
                    if rank == root:
                        for i in range(size):
                            object_return[k_i + i * k1] = object_return_k_i[i]

            else:
                if k2 > 1:
                    max_size_list = max(comm.allgather(len(gather_object)))
                    if len(gather_object) == 0:
                        gather_object += [[]] * (max_size_list - len(gather_object))
                    else:
                        gather_object += [dict_emptythings[type(gather_object[0])]] * (max_size_list - len(gather_object))
                    object_return = [None] * (max_size_list * size) if rank == root else None
                    for size_i in range(max_size_list):
                        list_return_object_i = [] if rank == root else None
                        object_cut_k2 = [int(x) for x in np.linspace(0, len(gather_object[size_i]), k2 + 1)]
                        for k_i in range(k2):
                            object_return_k_i = _gather_or_allgather((gather_object[size_i][object_cut_k2[k_i]:object_cut_k2[(k_i + 1)]]),
                              comm,
                              root, gather_method, optimize=False)
                            if rank == root:
                                list_return_object_i.append(object_return_k_i)

                        if rank == root:
                            for n_i in range(size):
                                merged_i_k = _merge_objects([list_return_object_i[k_i][n_i] for k_i in range(k2)])
                                if len(merged_i_k) > 0:
                                    object_return[size_i + n_i * max_size_list] = merged_i_k

                        del list_return_object_i

                    if rank == root:
                        object_return = list(filter((None).__ne__, object_return))
                    return object_return
        if isinstance(object_return, list):
            object_return = list(filter((None).__ne__, object_return))
            if len(object_return) > 0:
                object_return = _merge_objects(object_return)
            else:
                object_return = None
        return object_return


def bcast(bcast_object, comm, size_limit=50000000, root=0):
    """
    This function communicates an object to the rest of cores, but this time it communicates the
    whole object to all cores. Thus, at the end of the broadcasting, each core will have an
    exact copy of the object.

    :param bcast_object: Object to be communicated.
    :type bcast_object: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                          `pd.DataFrame` or `np.ndarray` objects. If a list of objects is passed
                          objects must all of them be [int, float, str] or [pd.DataFrame, np.array].
                          Lists with elements of mixed classes are yet not supported.

    :param comm: MPI4PY's MPI.COMM_WORLD object.

    :param size_limit: maximum byte size allowed for each divisible object. If the size exceeds the
                       size limit, the chunk will be divided in `k`subchunks.
    :type size_limit: int

    :param root: processor from which the object has been created.
    :type root: int

    :return: i-th subtable for processor i, already parallelized.
    :type return: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                  `pd.DataFrame` or `np.ndarray` objects.
    """
    if comm.rank == root:
        mem = virtual_memory().available
        size_scatter_object = _get_size_object(bcast_object)
    else:
        mem, size_scatter_object = (None, None)
    mem = comm.scatter([mem] * comm.size)
    size_scatter_object = comm.scatter([size_scatter_object] * comm.size)
    scatter_object_type = comm.scatter([type(bcast_object)] * comm.size)
    if size_scatter_object * comm.size > mem:
        raise MemoryError('The size of the object is too big to be broadcasted for this numberof processors.')
    return_object = None
    for CPU in range(comm.size):
        if root == CPU:
            return_object = bcast_object
        else:
            if comm.rank == root:
                scatter_list = [
                 dict_emptythings[type(bcast_object)]] * comm.size
                scatter_list[CPU] = bcast_object
            else:
                scatter_list = None
            scatter_list_object = _general_scatter(scatter_list, comm, size_limit=size_limit, root=root,
              by=[],
              dest=0,
              optimize=False,
              scatter_method='scatter')
            if comm.rank == CPU:
                return_object = scatter_list_object[0]

    return return_object


def scatter(scatter_object, comm, by=[], size_limit=500000000, root=0, optimize=True):
    """
    This function divides an object into `n` parts, and distributes it into all the cores.

    :param scatter_object: Object to be communicated.
    :type scatter_object: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                          `pd.DataFrame` or `np.ndarray` objects. If a list of objects is passed
                          objects must all of them be [int, float, str] or [pd.DataFrame, np.array].
                          Lists with elements of mixed classes are yet not supported.

    :param comm: MPI4PY's MPI.COMM_WORLD object.

    :param by: If the table cannot be directly divided by rows and, instead, there are some
               categorical variables that are stored within a column/s in the
               `pd.DataFrame`/`np.ndarray` object, `scatter` can perform the subdivision based
               on this variable.  For instance, it the column has 1000 genes (several rows per
               gene), and the # of processors is 10, each processor will have 100 genes. So far,
               only one `by` variable can be attributed. The table must be sorted by this
    :type by: int (`np.ndarray`) or str (`pd.Dataframe`).

    :param size_limit: maximum byte size allowed for each divisible object. If the size exceeds the
                       size limit, the chunk will be divided in `k`subchunks.
    :type size_limit: int

    :param root: processor from which the object has been created.
    :type root: int

    :param optimize: If `True`, applies a vectorized parallelization of the object, given the object
                     supports that parallelization.
    :type optimize: bool

    :return: i-th subtable for processor i, already parallelized.
    :type return: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                  `pd.DataFrame` or `np.ndarray` objects.
    """
    return _general_scatter(scatter_object, comm, by, dest=0, size_limit=size_limit, root=root, optimize=optimize,
      scatter_method='scatter')


def gather(gather_object, comm, optimize=True, size_limit=1500000000, root=0):
    """
    This function communicates individual objects, each one in a different core, to a
    destination core.

    :param gather_object: Object to be communicated.
    :type gather_object: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                          `pd.DataFrame` or `np.ndarray` objects. If a list of objects is passed
                          objects must all of them be [int, float, str] or [pd.DataFrame, np.array].
                          Lists with elements of mixed classes are yet not supported.

    :param comm: MPI4PY's MPI.COMM_WORLD object.

    :param size_limit: maximum byte size allowed for each divisible object. If the size exceeds the
                       size limit, the chunk will be divided in `k`subchunks.
    :type size_limit: int

    :param root: processor from which the object has been created.
    :type root: int

    :param optimize: If `True`, applies a vectorized parallelization of the object, given the object
                     supports that parallelization.
    :type optimize: bool

    :return: i-th subtable for processor i, already parallelized.
    :type return: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                  `pd.DataFrame` or `np.ndarray` objects.
    """
    return _general_gather(gather_object, comm, size_limit, root, optimize=optimize, gather_method='gather')


def allgather(allgather_object, comm, size_limit=1500000000, root=0):
    """
    This function combines the objects from all the cores and distributes copies of the
    combined object to all the cores.

    :param gather_object: Object to be communicated.
    :type gather_object: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                          `pd.DataFrame` or `np.ndarray` objects. If a list of objects is passed
                          objects must all of them be [int, float, str] or [pd.DataFrame, np.array].
                          Lists with elements of mixed classes are yet not supported.

    :param comm: MPI4PY's MPI.COMM_WORLD object.

    :param size_limit: maximum byte size allowed for each divisible object. If the size exceeds the
                       size limit, the chunk will be divided in `k`subchunks.
    :type size_limit: int

    :param root: processor from which the object has been created.
    :type root: int

    :return: i-th subtable for processor i, already parallelized.
    :type return: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                  `pd.DataFrame` or `np.ndarray` objects.
    """
    return _general_gather(allgather_object, comm, size_limit, root, optimize=False, gather_method='allgather')


def sendrecv(send_object, comm, dest, size_limit=1500000000, root=0):
    """
    This function sends an object from a source core to a destination node.

        :param send_object: Object to be communicated.
    :type send_object: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                          `pd.DataFrame` or `np.ndarray` objects. If a list of objects is passed
                          objects must all of them be [int, float, str] or [pd.DataFrame, np.array].
                          Lists with elements of mixed classes are yet not supported.

    :param comm: MPI4PY's MPI.COMM_WORLD object.

    :param dest: Destination node where the object will be communicated.
    :type dest: int

    :param size_limit: maximum byte size allowed for each divisible object. If the size exceeds the
                       size limit, the chunk will be divided in `k`subchunks.
    :type size_limit: int

    :param root: processor from which the object has been created.
    :type root: int

    :return: i-th subtable for processor i, already parallelized.
    :type return: `pd.DataFrame`, `np.ndarray`, and list of string, ints, floats, or
                  `pd.DataFrame` or `np.ndarray` objects.
    """
    return _general_scatter(send_object, comm, by=[], dest=dest, size_limit=size_limit, root=root, optimize=False, scatter_method='sendrecv')
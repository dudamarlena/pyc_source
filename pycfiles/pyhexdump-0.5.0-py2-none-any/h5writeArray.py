# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5writeArray.py
# Compiled at: 2014-12-08 16:27:09
import logging, h5py, numpy as np
from pyxll import xl_func
from h5_helpers import is_h5_location_handle, path_is_available_for_obj, resolvable
from shape_helpers import can_reshape, normalize_first, normalize_last, normalize_step
logger = logging.getLogger(__name__)

def create_array(loc, path, data):
    """
    Creates and writes data to an HDF5 array, and returns a
    message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path of the HDF5 array.
    data: var[]
        The data to be written.
    """
    ret = path
    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')
    if not isinstance(path, str):
        raise TypeError('String expected.')
    if not path_is_available_for_obj(loc, path, h5py.Dataset):
        return "Unable to create an HDF5 array at '%s'." % path
    try:
        x = np.asarray(data)
        file_type = x.dtype
        if file_type.char in ('S', 'U'):
            file_type = h5py.special_dtype(vlen=unicode)
        loc.create_dataset(path, x.shape, dtype=file_type, data=x.astype(file_type))
    except Exception as e:
        logger.info(e)
        ret = 'Array creation faild.'

    return ret


def write_array(loc, path, data, slice_tuple):
    """
    Creates (as needed) and writes data to an HDF5 array, and returns a
    message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path of the HDF5 array.
    data: var[]
        The data to be written.
    slice_tuple: tuple of slices
        The destination indices to be written.

    Comments
    --------
    The destination can be of a different rank than the data range.
    """
    ret = path
    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')
    if not isinstance(path, str):
        raise TypeError('String expected.')
    if not resolvable(loc, path):
        return "HDF5 array at '%s' not found." % path
    else:
        if loc.get(path, getclass=True) != h5py.Dataset:
            return "The object at '%s' is not an HDF5 array." % path
        dset = loc[path]
        file_type = dset.dtype
        x = None
        try:
            x = np.asarray(data).astype(file_type)
        except Exception as e:
            logger.info(e)
            return "Can't convert data to element type in the file."

        try:
            rk = len(dset.shape)
            rshape = tuple([ (slice_tuple[i].stop - slice_tuple[i].start) / slice_tuple[i].step for i in range(rk)
                           ])
            if not np.greater(rshape, 0).all():
                return 'Degenerate hyperslab found.'
            if not np.prod(rshape) == np.prod(x.shape):
                return 'Count mismatch between source and destination ranges.'
            rmaxshape = tuple([ slice_tuple[i].stop for i in range(rk) ])
            if np.greater(rmaxshape, dset.shape).any():
                if can_reshape(rmaxshape, dset.maxshape):
                    dset.resize(np.maximum(rmaxshape, dset.shape))
                else:
                    return "Can't extend the dataset to accomodate the data range."
            dset[slice_tuple] = x.reshape(rshape)
        except Exception as e:
            print e
            logger.info(e)
            ret = 'Write failed.'

        return ret


@xl_func('string filename, string arrayname, var[] data, var first, var last, var step : string', category='HDF5', thread_safe=False, disable_function_wizard_calc=True)
def h5writeArray(filename, arrayname, data, first, last, step):
    """
    Writes data to an HDF5 dataset

    :param filename: the name of an HDF5 file
    :param arrayname: the path name of an HDF5 array
    :param data: an Excel range of data to be written
    :param first: the (1-based) index of the first element to be written (optional)
    :param last: the (1-based) index of the last element to be written (optional)
    :param step: the write stride in each dimension (optional)
    :returns: A string
    """
    ret = arrayname
    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")
    if not isinstance(arrayname, str):
        raise TypeError("'arrayname' must be a string.")
    if not isinstance(data, list):
        raise TypeError("'data' must be a list.")
    try:
        with h5py.File(filename, 'a') as (f):
            create = False
            if not resolvable(f, arrayname):
                if not path_is_available_for_obj(f, arrayname, h5py.Dataset):
                    return "Unable to create an HDF5 array at '%s'." % arrayname
                create = True
            elif f.get(arrayname, getclass=True) != h5py.Dataset:
                return "The object at '%s' is not an HDF5 array." % arrayname
            if create:
                ret = create_array(f, arrayname, data)
            else:
                dset = f[arrayname]
                start = normalize_first(first, dset.shape)
                stop = normalize_last(last, dset.shape)
                stride = normalize_step(step, dset.shape)
                slc = [ slice(start[i], stop[i], stride[i]) for i in range(len(start))
                      ]
                ret = write_array(f, arrayname, data, tuple(slc))
    except IOError as e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % filename
    except Exception as e:
        logger.info(e)
        return 'Internal error.'

    return ret
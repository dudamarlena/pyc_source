# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5appendRows.py
# Compiled at: 2014-12-08 16:26:04
import logging, h5py, numpy as np
from pyxll import xl_func
from h5_helpers import is_h5_location_handle, resolvable
logger = logging.getLogger(__name__)

def append_rows(loc, path, rows):
    """
    Append rows to an existing table and returns the number of appended rows. 

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path of the HDF5 table.
    rows: var[]
        The rows to be appended.

    """
    ret = path
    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')
    if not isinstance(path, str):
        raise TypeError('String expected.')
    if not isinstance(rows, list):
        raise TypeError('List expected.')
    if not resolvable(loc, path):
        return "HDF5 table at '%s' not found." % path
    if loc.get(path, getclass=True) != h5py.Dataset:
        return "The object at '%s' is not an HDF5 table." % path
    dset = loc[path]
    file_type = dset.dtype
    a = np.zeros((len(rows),), dtype=file_type)
    try:
        x = np.asarray(rows)
        for i in range(len(rows)):
            field_count = 0
            for fld in file_type.names:
                a[i][fld] = x[i][field_count]
                field_count += 1

    except Exception as e:
        logger.info(e)
        return "Can't convert rows to the element type in the file."

    try:
        curr_rows = dset.shape[0]
        new_rows = len(rows)
        dset.resize((curr_rows + new_rows,))
        dset[curr_rows:] = a
        ret = '%d rows appended.' % new_rows
    except Exception as e:
        print e
        logger.info(e)
        ret = 'Write failed.'

    return ret


@xl_func('string filename, string tablename, var[] rows: var', category='HDF5', thread_safe=False, disable_function_wizard_calc=True)
def h5appendRows(filename, tablename, rows):
    """
    Appends rows to an exisiting HDF5 table.

    :param filename: the name of an HDF5 file
    :param tablename: the path name of an HDF5 table
    :param rows: an Excel range of rows
    :returns: A string, the number of rows appended
    """
    ret = '\x00'
    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")
    if not isinstance(tablename, str):
        raise TypeError("'tablename' must be a string.")
    try:
        with h5py.File(filename, 'a') as (f):
            if not resolvable(f, tablename):
                return 'Table not found.'
            if f.get(tablename, getclass=True) != h5py.Dataset:
                return "The object at '%s' is not an HDF5 table." % tablename
            dset = f[tablename]
            if len(dset.shape) != 1 or dset.maxshape != (None, ):
                return "The object at '%s' is not an HDF5 table." % tablename
            if dset.dtype.names is None:
                return "The object at '%s' is not an HDF5 table." % tablename
            ret = append_rows(f, tablename, rows)
    except IOError as e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % filename
    except Exception as e:
        logger.info(e)
        return 'Internal error.'

    return ret
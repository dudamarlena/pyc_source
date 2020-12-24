# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5readAttribute.py
# Compiled at: 2014-12-08 16:26:36
import h5py
from pyxll import xl_func
from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc

@xl_func('string filename, string location, string attr: string', category='HDF5', thread_safe=False, disable_function_wizard_calc=True)
def h5readAttribute(filename, location, attr):
    """
    Reads and returns a string repesentation of the value of an HDF5 attribute.

    :param filename: the name of an HDF5 file
    :param location: the location of a HDF5 object
    :param attr:     the name of an HDF5 attribute
    :returns: A string
    """
    if not isinstance(filename, str):
        raise TypeError('String expected.')
    if not isinstance(location, str):
        raise TypeError('String expected.')
    if not isinstance(attr, str):
        raise TypeError('String expected.')
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." % filename
    else:
        with h5py.File(filename, 'r') as (f):
            path = location
            if path != '':
                if path not in f:
                    return "Invalid location '%s'." % path
            else:
                path = '/'
            is_valid, species = path_is_valid_wrt_loc(f, path)
            if not is_valid:
                return 'Invalid location specified.'
            obj = f.get(path)
            if obj is not None:
                if attr in obj.attrs:
                    return str(obj.attrs[attr])
                else:
                    return "No attribute named '%s' found." % attr

            else:
                return "No object at location '%s'." % location
        return
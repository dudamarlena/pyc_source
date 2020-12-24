# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5getInfo.py
# Compiled at: 2015-03-06 08:25:28
import logging, h5py, numpy as np
from pyxll import xl_func
from config import Limits
from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc
import renderer
from type_helpers import dtype_to_hexad
from shape_helpers import tuple_to_excel
logger = logging.getLogger(__name__)

def render_info(loc, path):
    """
    Returns a list of key/value pairs (more or less)

    Parameters
    ----------
    loc: h5py.File
        An open file handler where to search.
    path: str
        the path into the file that we are interested in.
    """
    is_valid, species = path_is_valid_wrt_loc(loc, path)
    if not is_valid:
        raise ValueError('The specified path is invalid with respect to the location provided.')
    result = []
    if species is None or isinstance(species, h5py.HardLink):
        hnd = loc if path == '/' else loc[path]
        num_attr = len(hnd.attrs)
        if num_attr > 0:
            result.append(('Number of attributes:', num_attr))
            keys = hnd.attrs.keys()
            vals = hnd.attrs.values()
            for key, val in zip(keys, vals):
                result.append((key, str(val)))

        if isinstance(hnd, (h5py.File, h5py.Group)):
            num_links = len(hnd.keys())
            result.append(('Number of links:', num_links))
            if num_links > 0:
                result.append(('Link names:', '\x00'))
                keys = hnd.keys()
                for key in keys:
                    result.append(('\x00', key))

        elif isinstance(hnd, h5py.Dataset):
            result.append(('Number of elements:', hnd.size))
            result.append(('Shape:', tuple_to_excel(hnd.shape)))
            result.append(('Type:', dtype_to_hexad(hnd.dtype)))
        elif isinstance(hnd, h5py.Datatype):
            result.append(('Type:', dtype_to_hexad(hnd.dtype)))
        else:
            raise ValueError('What kind of hardlink is this???')
    elif isinstance(species, h5py.SoftLink):
        result.append(('Link:', 'SoftLink'))
        result.append(('Destination:', species.path))
    elif isinstance(species, h5py.ExternalLink):
        result.append(('Link:', 'ExternalLink'))
        result.append(('Destination:',
         ('file://{}/{}').format(species.filename, species.path)))
    else:
        result.append(('Link:', 'Unknown link type.'))
    return result


@xl_func('string filename, string location : string', category='HDF5', thread_safe=False, macro=True, disable_function_wizard_calc=True)
def h5getInfo(filename, location):
    """
    Display detailed information about a specific location in an HDF5 file.

    :param filename: the name of an HDF5 file
    :param location: an HDF5 path name (optional)
    :returns: A string
    """
    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")
    if not isinstance(location, str):
        raise TypeError("'location' must be a string.")
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." % filename
    ret = '\x00'
    with h5py.File(filename, 'r') as (f):
        path = location
        if path != '':
            if path not in f:
                return 'Invalid location.'
        else:
            path = '/'
        is_valid, _ = path_is_valid_wrt_loc(f, path)
        if not is_valid:
            return 'Invalid location specified.'
        ret = path
        lines = render_info(f, path)
        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines) + 1, 2), dtype=dty)
        row = 0
        for l in lines:
            a[row] = l
            row += 1
            if row >= Limits.EXCEL_MAX_ROWS:
                break

        renderer.draw(a)
        return ret
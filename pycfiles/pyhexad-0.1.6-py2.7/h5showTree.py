# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5showTree.py
# Compiled at: 2015-03-12 09:39:38
"""
We use H5Ovisit to traverse the hierarchy starting from a given location.
H5Ovisit introduces a traversal order that is akin to XML document order.
A worksheet can be viewed as a 2D grid of rows and columns.
The cell position where to render the link name of an object is as follows:

row    - the current position in "document order"
column - the "level" = the number of group ancestors
"""
from functools import partial
import posixpath, logging, h5py, numpy as np
from pyxll import xl_func
from config import Limits
from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc
import renderer
logger = logging.getLogger(__name__)

def render_tree(loc, path):
    """
    Create a list of tuples (col, name), where 'col' is the
    column index and 'name' is a link or HDF5 path name.
    The row index is the position in the list.

    Returns the list and the maximum column index.
    """
    is_valid, species = path_is_valid_wrt_loc(loc, path)
    if not is_valid:
        raise Exception('The specified path is invalid with respect to the location provided.')
    result = []
    if species is None or isinstance(species, h5py.HardLink):
        hnd = loc if path == '/' else loc[path]
        if isinstance(hnd, (h5py.File, h5py.Group)):
            result.append((1, hnd.name))

            def print_obj(grp, name):
                path = posixpath.join(grp.name, name)
                col = path.count('/')
                result.append((col, path.split('/')[(-1)]))

            hnd.visit(partial(print_obj, hnd))
        elif isinstance(hnd, (h5py.Dataset, h5py.Datatype)):
            result.append((1, hnd.name))
        else:
            raise Exception('What kind of hardlink is this???')
    else:
        if isinstance(species, (h5py.SoftLink, h5py.ExternalLink)):
            result.append((1, loc.name + '/' + path))
        else:
            result.append((1, 'Unknown link type found.'))
        max_col = 0
        for line in result:
            if line[0] > max_col:
                max_col = line[0]

    return (
     result, max_col)


@xl_func('string filename, string location : string', category='HDF5', thread_safe=False, macro=True, disable_function_wizard_calc=True)
def h5showTree(filename, location):
    """
    Display contents of an HDF5 file in hierarchical form

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
        ret = f.filename
        path = location
        if path != '':
            if path not in f:
                return 'Invalid location.'
        else:
            path = '/'
        is_valid, dummy = path_is_valid_wrt_loc(f, path)
        if not is_valid:
            return 'Invalid location specified.'
        lines = []
        max_col = 0
        lines, max_col = render_tree(f, path)
        if len(lines) >= Limits.EXCEL_MAX_ROWS or max_col >= Limits.EXCEL_MAX_COLS:
            return 'The number objects in the file or the depth of thehierarchy exceeds the maximum number of rows or columnsof an Excel worksheet.'
        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines) + 1, max_col + 1), dtype=dty)
        row = 0
        for l in lines:
            a[(row, 0)] = row
            a[(row, l[0])] = l[1]
            row += 1

        renderer.draw(a)
        return ret
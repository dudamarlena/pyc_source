# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5newArray.py
# Compiled at: 2014-12-08 16:26:12
import logging, h5py, numpy as np
from pyxll import xl_func
from h5_helpers import is_h5_location_handle, path_is_available_for_obj
from shape_helpers import get_chunk_dimensions, get_dimensions
from type_helpers import parse_dtype
logger = logging.getLogger(__name__)

def new_array(loc, path, size, plist=''):
    """
    Creates a new HDF5 array and returns a message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path where to create the new array.
    size: list of lists
        The dimensions of the new array.
    plist: string
        A list of dataset creation properties.
    """
    ret = path
    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')
    if not path_is_available_for_obj(loc, path, h5py.Dataset):
        return "Can't create array at '%s'." % path
    else:
        plist_ht = {}
        if plist.strip() != '':
            if len(plist.split(',')) % 2 != 0:
                return 'Invalid property list.'
            a = plist.split(',')
            for i in range(0, len(a), 2):
                plist_ht[a[i].strip().upper()] = a[(i + 1)].strip()

        try:
            kwargs = {}
            dims, maxdims = get_dimensions(size)
            if dims is None:
                return 'Invalid dimensions specified.'
            kwargs['shape'] = tuple(dims)
            kwargs['maxshape'] = tuple(maxdims)
            file_type = np.dtype('double')
            if 'DATATYPE' in plist_ht.keys():
                try:
                    file_type = parse_dtype(plist_ht['DATATYPE'].upper())
                except:
                    return "Unsupported datatype '%s'." % plist_ht['DATATYPE'].upper()

            kwargs['dtype'] = file_type
            if 'CHUNKSIZE' in plist_ht.keys():
                chunk = plist_ht['CHUNKSIZE']
                chunkdims = get_chunk_dimensions(chunk)
                if chunkdims is None:
                    return 'Invalid chunk dimensions specified.'
                if len(chunkdims) != len(dims):
                    return 'Chunk rank must equal array rank.'
                kwargs['chunks'] = chunkdims
            if 'DEFLATE' in plist_ht.keys():
                lvl = plist_ht['DEFLATE']
                try:
                    lvl = int(lvl)
                    if lvl < 0 or lvl > 9:
                        return 'Compression level out of range [0-9].'
                    kwargs['compression'] = lvl
                except:
                    return 'Invalid compression level ([0-9]).'

            if 'FILLVALUE' in plist_ht.keys():
                fv = plist_ht['FILLVALUE']
                try:
                    if file_type in np.sctypes['float']:
                        fv = float(fv)
                    elif file_type in np.sctypes['int'] or file_type in np.sctypes['uint']:
                        fv = int(fv)
                    kwargs['fillvalue'] = fv
                except:
                    return 'Invalid fill value.'

            if 'FLETCHER32' in plist_ht.keys():
                bool = plist_ht['FLETCHER32']
                if bool.strip().lower() == 'true':
                    kwargs['fletcher32'] = True
            if 'SHUFFLE' in plist_ht.keys():
                bool = plist_ht['SHUFFLE']
                if bool.strip().lower == 'true':
                    kwargs['shuffle'] = True
            loc.create_dataset(path, **kwargs)
        except Exception as e:
            logger.info(e)
            ret = 'Internal error.'

        return ret


@xl_func('string filename, string datasetname, int[] size, string plist : string', category='HDF5', thread_safe=False, disable_function_wizard_calc=True)
def h5newArray(filename, arrayname, size, properties):
    """
    Creates a new multi-diensional HDF5 dataset of a scalar datatype.

    :param filename: the name of an HDF5 file
    :param arrayname: the name of the HDF5 array to be created
    :param size: the dimensions of the dataset to be created
    :param properties: a list of dataset creation properties (optional)
    :returns: A string
    """
    if not isinstance(filename, str):
        return "'filename' must be a string."
    if not isinstance(arrayname, str):
        return "'arrayname' must be a string."
    if not isinstance(size, list):
        return "'size' must be a list of lists."
    if not isinstance(properties, str):
        return "'properties' must be a string."
    ret = '\x00'
    if filename.strip() == '':
        return 'Missing file name.'
    try:
        with h5py.File(filename, 'a') as (f):
            ret = new_array(f, arrayname, size, properties)
    except IOError as e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % filename
    except Exception as e:
        logger.info(e)
        return 'Internal error.'

    return ret
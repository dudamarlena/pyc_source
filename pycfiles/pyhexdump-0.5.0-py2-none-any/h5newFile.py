# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5newFile.py
# Compiled at: 2014-12-08 16:26:17
import logging, tempfile, h5py
from pyxll import xl_func
logger = logging.getLogger(__name__)

@xl_func('string filename: string', category='HDF5', thread_safe=False, disable_function_wizard_calc=False)
def h5newFile(filename):
    """
    Creates a new HDF5 file. If no file name is specified a temporary file
    name will be generated at random.

    Existing files will not be overwritten.

    :param filename: the name of the HDF5 file to be created (optional)
    :returns: A string
    """
    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")
    ret = '\x00'
    if filename == '':
        filename = tempfile.mktemp('.h5')
    try:
        with h5py.File(filename, 'w-', libver='latest') as (f):
            ret = filename
    except IOError as e:
        ret = "Can't create file '%s'." % filename
    except Exception as e:
        logger.info(e)
        return 'Internal error.'

    return ret
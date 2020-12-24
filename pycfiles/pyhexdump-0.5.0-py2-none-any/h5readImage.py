# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhexad\h5readImage.py
# Compiled at: 2014-12-08 16:26:41
import logging, os
from tempfile import mktemp
import h5py
from pyxll import xl_func
from renderer import xl_app
from config import Places
from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc
logger = logging.getLogger(__name__)

def get_image(loc, image_path, palette_path=None):
    """
    Returns the absolute path of a GIF image rendering of the
    HDF5 image at image_path
    """
    is_valid, species = path_is_valid_wrt_loc(loc, image_path)
    if not is_valid:
        return (None, 'Invalid image path specified.')
    else:
        if loc.get(image_path) is None or loc.get(image_path, getclass=True) != h5py.Dataset:
            return (None, "Can't open HDF5 image '%s'." % image_path)
        exe = '%s\\bin\\%s' % (Places.HDF5_HOME, Places.H52GIF)
        if not os.path.exists(exe):
            return (None, "Can't locate the h52gif executable. Check config.py!")
        img = None
        try:
            gif = mktemp('.gif')
            cmd = '%s %s %s -i "%s"' % (exe, loc.file.filename, gif, image_path)
            os.system(cmd)
            img = gif
        except Exception as e:
            logger.info(e)
            return (
             None, str(e))

        return (
         img, '\x00')


@xl_func('string filename, string imagename, string palettename: string', category='HDF5')
def h5readImage(filename, imagename, palettename=None):
    """
    Reads an HDF5 image

    :param filename: the name of an HDF5 file
    :param imagename: the name of an HDF5 image
    :param palettename: the name of an HDF5 palette (optional)
    """
    ret = '\x00'
    if not isinstance(filename, str):
        return "'filename' must be a string."
    else:
        if not file_exists(filename):
            return "Can't open file '%s' or the file is not an HDF5 file." % filename
        if not isinstance(imagename, str):
            return "'imagename' must be a string."
        if palettename is not None:
            if not isinstance(palettename, str):
                return "'palettename' must be a string."
        try:
            with h5py.File(filename) as (f):
                img, ret = get_image(f, imagename, palettename)
                if img is None:
                    return ret
                if not os.path.exists(img):
                    return 'Failed to create image file.'
                xl_app().ActiveSheet.Pictures().Insert(img)
        except Exception as e:
            logger.info(e)
            ret = 'Internal error. Contact support!'

        return ret
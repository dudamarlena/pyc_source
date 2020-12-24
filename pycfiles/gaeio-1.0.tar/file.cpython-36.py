# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\gaeio\src\basic\file.py
# Compiled at: 2020-04-25 14:33:31
# Size of source mod 2**32: 1503 bytes
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.messager import messager as vis_msg
__all__ = [
 'file']

def readAsciiFile(asciifile, comment='#', delimiter=None):
    """
    Read an ASCII file (by numpy.loadtxt)

    Args:
        asciifile:  An ASCII file for reading
        comment:    Comments. Default is '#'
        delimiter:  Delimiter. Default is None

    Return:
        2D array of the data from the ASCII file
    """
    if os.path.exists(asciifile) is False:
        vis_msg.print('ERROR in readAsciiFile: Ascii file not found', type='error')
        sys.exit()
    try:
        return np.loadtxt(asciifile, comments=comment, delimiter=delimiter)
    except ValueError:
        return


class file:
    readAsciiFile = readAsciiFile
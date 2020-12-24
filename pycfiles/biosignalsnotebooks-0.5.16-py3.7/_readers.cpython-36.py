# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\gui_s\AppData\Local\Temp\pip-build-vljg4uzq\pyedflib\pyedflib\data\_readers.py
# Compiled at: 2018-06-15 05:54:11
# Size of source mod 2**32: 546 bytes
import os, numpy as np, pyedflib

def test_generator():
    """
    Get an sample EDF-file

    Parameters
    ----------
    None

    Returns
    -------
    f : EdfReader object
       object containing the handle to the file

    Examples
    --------
    >>> import pyedflib.data
    >>> f = pyedflib.data.test_generator()
    >>> f.signals_in_file == 11
    True
    >>> f._close()
    >>> del f

    """
    fname = os.path.join(os.path.dirname(__file__), 'test_generator.edf')
    f = pyedflib.EdfReader(fname)
    return f
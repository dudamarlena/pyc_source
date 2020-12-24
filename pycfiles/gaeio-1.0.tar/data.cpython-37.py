# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\basic\data.py
# Compiled at: 2019-12-15 16:23:09
# Size of source mod 2**32: 1622 bytes
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.vis.messager as vis_msg
__all__ = [
 'data']

def str2int(str):
    """
    Covert a string to integer

    Args:
        str:    A string for conversion

    Return:
        The corresponding integer if it is convertable. Otherwise, False is returned.
    """
    try:
        return int(str)
    except ValueError:
        return False


def str2float(str):
    """
    Covert a string to float

    Args:
        str:    A string for conversion

    Return:
        The corresponding float if it is convertable. Otherwise, False is returned.
    """
    try:
        return float(str)
    except ValueError:
        return False


class data:
    str2int = str2int
    str2float = str2float
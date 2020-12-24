# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pymcaspec/utils.py
# Compiled at: 2019-02-16 17:54:00
# Size of source mod 2**32: 653 bytes
import numpy as np

def get_T_ISR(scan_inst):
    """ISR specific function to read the temperature.

    Parameters
    ----------
    scan_inst : instance of scan class
        a particular scan created in pymcaspec

    Returns
    -------
    TB : float
        The B temperature sensor
    TA : float
        The A temperature sensor
    """
    TB, TA = [], []
    for dataobject in scan_inst.dataobjects:
        header = dataobject.info['Header']
        lineX = [line for line in header if '#X' in line][0]
        tb, ta = lineX.split(' ')[1:4:2]
        TB.append(float(tb))
        TA.append(float(ta))

    return (np.array(TB), np.array(TA))
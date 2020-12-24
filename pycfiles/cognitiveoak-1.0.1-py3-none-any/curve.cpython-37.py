# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\basic\curve.py
# Compiled at: 2019-12-15 16:23:09
# Size of source mod 2**32: 2181 bytes
import numpy as np
from scipy import interpolate
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.vis.messager as vis_msg
__all__ = [
 'curve']

def changeCurveSize(curve, length_new, kind='cubic'):
    """
    Change curve size through 1D interpolation (from scipy)

    Args:
        curve:      2D array of curves, with each row representing one curve
        length_new: Length of the new curve.
        kind:       Interpolation type as a string ('linear', 'nearest', 'quadratic', 'cubic'). Default is 'cubic'

    Return:
        2D array of curves after interpolation, with each row representing one curve
    """
    if np.ndim(curve) != 2:
        vis_msg.print('ERROR in changeCurveSize: 2D array expected', type='error')
        sys.exit()
    if length_new <= 1:
        vis_msg.print('ERROR in changeCurveSize: New curve length > 1', type='error')
        sys.exit()
    ncurve = np.shape(curve)[0]
    length = np.shape(curve)[1]
    line = np.linspace(0.0, 1.0, length)
    line_new = np.linspace(0.0, 1.0, length_new)
    curve_new = np.zeros([ncurve, length_new])
    for i in range(ncurve):
        curve_i = curve[i, :]
        f = interpolate.interp1d(line, curve_i, kind=kind)
        curve_new[i, :] = f(line_new)

    return curve_new


class curve:
    changeCurveSize = changeCurveSize
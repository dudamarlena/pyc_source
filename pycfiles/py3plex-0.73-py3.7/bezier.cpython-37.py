# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/bezier.py
# Compiled at: 2019-02-26 09:54:34
# Size of source mod 2**32: 2785 bytes
import numpy as np
from scipy.interpolate import CubicSpline

def bezier_calculate_dfy(mp_y, path_height, x0, midpoint_x, x1, y0, y1, dfx, mode='upper'):
    if mode == 'upper':
        midpoint_y = mp_y * path_height
    else:
        if mode == 'bottom':
            midpoint_y = mp_y * (2 - path_height)
        else:
            raise ValueError("Unknown mode in dfy calculation (value must be one of 'upper', 'bottom'")
    x_t = [
     x0, midpoint_x, x1]
    y_t = [y0, midpoint_y, y1]
    cs = CubicSpline(x_t, y_t)
    return cs(dfx)


def draw_bezier(total_size, p1, p2, mode='quadratic', inversion=False, path_height=2, linemode='both', resolution=0.1):
    if mode == 'quadratic':
        if p1[0] < p1[1]:
            x0, x1 = p1
            y0, y1 = p2
        else:
            x1, x0 = p1
            y1, y0 = p2
        dfx = np.arange(x0, x1, resolution)
        midpoint_x = (x0 + x1) / 2
        mp_y = (y0 + y1) / 2
        if linemode == 'both':
            r1 = np.round(y0, 0)
            r2 = np.round(y1, 0)
            try:
                if r1 > y0 and r2 > y1:
                    dfy = bezier_calculate_dfy(mp_y, path_height, x0, midpoint_x, x1, y0, y1, dfx, mode='upper')
                else:
                    dfy = bezier_calculate_dfy(mp_y, path_height, x0, midpoint_x, x1, y0, y1, dfx, mode='bottom')
            except Exception:
                raise Exception('Unable to calculate coordinate for points ' + str((x0, y0)) + ', ' + str((x1, y1)))

        else:
            if linemode == 'upper':
                try:
                    dfy = bezier_calculate_dfy(mp_y, path_height, x0, midpoint_x, x1, y0, y1, dfx, mode='upper')
                except Exception:
                    raise Exception('Unable to calculate coordinate for points ' + str((x0, y0)) + ', ' + str((x1, y1)))

            else:
                if linemode == 'bottom':
                    try:
                        dfy = bezier_calculate_dfy(mp_y, path_height, x0, midpoint_x, x1, y0, y1, dfx, mode='bottom')
                    except Exception:
                        raise Exception('Unable to calculate coordinate for points ' + str((x0, y0)) + ', ' + str((x1, y1)))

                else:
                    msg = "Unknown linemode '{linemode}' in curve calculation (value must be one of 'upper', 'bottom', 'both'"
                    raise ValueError(msg.format(lm=linemode))
        return (
         dfx, dfy)
    if mode == 'cubic':
        pass
    else:
        msg = "Unknown mode '{mode}' in curve calculation (value must be one of 'quadratic', 'cubic', 'quad'"
        raise ValueError(msg.format(mode=mode))
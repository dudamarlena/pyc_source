# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/part3d.py
# Compiled at: 2020-02-25 16:40:42
# Size of source mod 2**32: 705 bytes
"""part3d generator

module to generat part3d 
"""
__all__ = [
 'Part3D']

class Part3D:
    __doc__ = 'create a part3d object'

    def __init__(self):
        """startup class"""
        self.points = list()
        self.conn = list()

    def add_line(self, pos0, pos1, npts):
        """Add a line frop pos0 to pos1"""
        p_t = list(pos0)
        self.points.append(list(p_t))
        for i in range(0, npts - 1):
            next_ptid = len(self.points)
            alpha = 1.0 * (i + 1) / (npts - 1)
            for j in range(3):
                p_t[j] = pos0[j] + (pos1[j] - pos0[j]) * alpha

            self.points.append(list(p_t))
            self.conn.append([next_ptid - 1, next_ptid])
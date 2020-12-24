# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/PyChemia/tests/test_code_vasp_03.py
# Compiled at: 2019-05-14 13:43:02
# Size of source mod 2**32: 486 bytes
import sys, numpy, pychemia
if pychemia.HAS_MAYAVI:
    from mayavi.mlab import quiver
    if not pychemia.HAS_MAYAVI:
        sys.exit(1)

    def test_quiver3d():
        x, y, z = numpy.mgrid[-2:3, -2:3, -2:3]
        r = numpy.sqrt(x ** 2 + y ** 2 + z ** 4)
        u = y * numpy.sin(r) / (r + 0.001)
        v = -x * numpy.sin(r) / (r + 0.001)
        w = numpy.zeros_like(z)
        obj = quiver3d(x, y, z, u, v, w, line_width=3, scale_factor=1)
        return obj
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/examples/diffusion2Dtest.py
# Compiled at: 2014-09-23 12:37:24
import numpy as np
from landlab import RasterModelGrid
import pylab
from pylab import plot, draw, show, contour

def main():
    nr = 130
    nc = 3
    dx = 0.25
    s = 0.001
    k = 0.01
    dt = 0.25 * dx ** 2.0 / k
    print 'dt=', dt
    nt = 40000
    mg = RasterModelGrid(nr, nc, dx)
    u = mg.zeros(centering='cell')
    interior_cells = mg.get_interior_cells()
    dudt = mg.zeros(centering='cell')
    mg.set_noflux_boundaries(False, True, False, True)
    for i in range(0, nt):
        print i
        g = mg.calculate_face_gradients(u)
        q = -k * g
        dqds = mg.calculate_flux_divergences(q)
        for c in interior_cells:
            dudt[c] = s - dqds[c]

        u = u + dudt * dt
        u = mg.update_noflux_boundaries(u)

    ur = mg.cell_vector_to_raster(u)
    print 'Max u = ', max(u)
    contour(ur)
    show()


if __name__ == '__main__':
    main()
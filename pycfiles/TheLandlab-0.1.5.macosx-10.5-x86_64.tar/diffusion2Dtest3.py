# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/examples/diffusion2Dtest3.py
# Compiled at: 2014-09-23 12:37:24
"""
diffusion2Dtest.py: Tests ModelGrid() class by implementing a 2D
diffusion code.

version 3 same as 2 but uses source as a dvector

GT, July 2010
"""
from landlab import RasterModelGrid
from pylab import plot, draw, show, contour

def set_flux_coefficients(mg, dx):
    """
    Sets the spatial pattern of "K" (diffusion coefficient at cell
    faces)
    """
    Kmax = 1.0
    Kexp = 1.0
    yf = mg.get_face_y_coords()
    xf = mg.get_face_x_coords()
    decay_scale = 0.5
    xf = xf - dx / 2.0
    yf = yf - dx / 2.0
    x0 = 0.5 * (mg.number_of_node_columns - 2) * dx
    y0 = (mg.number_of_node_columns - 2) * dx
    dist = sqrt((xf - x0) ** 2.0 + (yf - y0) ** 2.0)
    K = Kmax * exp(-dist / decay_scale)
    return K


def main():
    nr = 12
    nc = 12
    dx = 0.5
    s0 = 0.001
    mg = RasterModelGrid(nr, nc, dx)
    u = mg.zeros(centering='cell')
    interior_cells = mg.get_interior_cells()
    dudt = mg.zeros(centering='cell')
    s = mg.zeros(centering='cell')
    s[interior_cells] = s0
    opt_plot = True
    k = set_flux_coefficients(mg, dx)
    dt = 0.25 * dx ** 2.0 / max(k)
    run_time = 100.0
    nt = int(round(run_time / dt))
    mg.set_noflux_boundaries(True, True, False, True)
    for i in range(0, nt):
        print i
        g = mg.calculate_face_gradients(u)
        q = -k * g
        dqds = mg.calculate_flux_divergences(q)
        dudt = s - dqds
        u = u + dudt * dt
        u = mg.update_noflux_boundaries(u)

    if opt_plot:
        ur = mg.cell_vector_to_raster(u)
        contour(ur)
        show()


if __name__ == '__main__':
    main()
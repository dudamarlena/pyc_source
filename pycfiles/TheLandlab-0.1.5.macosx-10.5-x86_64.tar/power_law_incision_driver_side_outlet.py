# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/simple_power_law_incision/power_law_incision_driver_side_outlet.py
# Compiled at: 2014-09-23 12:37:24
import numpy as np, pylab
from landlab import RasterModelGrid
from random import uniform
from landlab.components.simple_power_law_incision.power_law_fluvial_eroder import PowerLawIncision
from landlab.components.flow_routing.flow_routing_D8 import RouteFlowD8
from landlab.components.flow_accum.flow_accumulation2 import AccumFlow
import matplotlib.pyplot as plt

def main():
    nr = 50
    nc = 60
    nnodes = nr * nc
    dx = 10
    rg = RasterModelGrid(nr, nc, dx)
    rg.set_inactive_boundaries(False, True, True, True)
    z = np.zeros(nnodes)
    for i in range(0, nnodes):
        if rg.is_interior(i):
            z[i] = 2 + uniform(-0.5, 0.5)

    total_run_time = 10000
    one_twentieth_time = total_run_time / 20
    uplift_rate = 0.001
    rain_rate = 1
    storm_duration = 50
    elapsed_time = 0
    incisor = PowerLawIncision('input_file.txt', rg)
    interior_nodes = rg.get_active_cell_node_ids()
    while elapsed_time < total_run_time:
        z = incisor.run_one_storm(rg, z, rain_rate, storm_duration)
        z[interior_nodes] = z[interior_nodes] + uplift_rate * storm_duration
        elapsed_time = elapsed_time + storm_duration
        if elapsed_time % one_twentieth_time == 0:
            print 'elapsed time', elapsed_time
            elev_raster = rg.node_vector_to_raster(z, True)
            pylab.figure(22)
            im = pylab.imshow(elev_raster, cmap=pylab.cm.RdBu, extent=[0, nc * rg.dx, 0, nr * rg.dx])
            cb = pylab.colorbar(im)
            cb.set_label('Elevation (m)', fontsize=12)
            pylab.title('Topography')
            pylab.show()

    flow_router = RouteFlowD8(len(z))
    flowdirs, max_slopes = flow_router.calc_flowdirs(rg, z)
    accumulator = AccumFlow(rg)
    drain_area = accumulator.calc_flowacc(rg, z, flowdirs)
    plt.loglog(np.array(drain_area), np.array(max_slopes), 'ro')
    plt.xlabel('drainage area, m')
    plt.ylabel('surface slope')
    plt.show()
    elev_raster = rg.node_vector_to_raster(z, True)
    pylab.figure(22)
    im = pylab.imshow(elev_raster, cmap=pylab.cm.RdBu, extent=[0, nc * rg.dx, 0, nr * rg.dx])
    cb = pylab.colorbar(im)
    cb.set_label('Elevation (m)', fontsize=12)
    pylab.title('Topography')
    pylab.show()


if __name__ == '__main__':
    main()
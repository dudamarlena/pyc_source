# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/simple_power_law_incision/power_law_incision_driver.py
# Compiled at: 2014-09-23 12:37:24
import numpy as np
from pylab import *
from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_grid
from landlab.components.dem_support.dem_boundary_conditions import WatershedBoundaryConditions
from random import uniform
from landlab.components.simple_power_law_incision.power_law_fluvial_eroder import PowerLawIncision
from landlab.components.flow_routing.flow_routing_D8 import RouteFlowD8
from landlab.components.flow_accum.flow_accumulation2 import AccumFlow
import matplotlib.pyplot as plt

def main():
    nr = 5
    nc = 6
    nnodes = nr * nc
    dx = 1
    rg = RasterModelGrid(nr, nc, dx)
    nodata_val = -1
    z = nodata_val * np.ones(nnodes)
    helper = [
     7, 8, 9, 10, 13, 14, 15, 16]
    for i in xrange(0, len(helper)):
        z[helper[i]] = 2 + uniform(-0.5, 0.5)

    helper = [
     19, 20, 21, 22]
    for i in xrange(0, len(helper)):
        z[helper[i]] = 3 + uniform(-0.5, 0.5)

    z[7] = 1
    bc = WatershedBoundaryConditions()
    outlet_loc = bc.set_bc_find_outlet(rg, z, nodata_val)
    zoutlet = z[outlet_loc]
    total_run_time = 500000
    uplift_rate = 0.001
    rain_rate = 1
    storm_duration = 50
    elapsed_time = 0
    incisor = PowerLawIncision('input_file.txt', rg)
    interior_nodes = rg.get_active_cell_node_ids()
    while elapsed_time < total_run_time:
        z[interior_nodes] = z[interior_nodes] + uplift_rate * storm_duration
        z[outlet_loc] = zoutlet
        z = incisor.run_one_storm(rg, z, rain_rate, storm_duration)
        elapsed_time = elapsed_time + storm_duration

    flow_router = RouteFlowD8(len(z))
    flowdirs, max_slopes = flow_router.calc_flowdirs(rg, z)
    accumulator = AccumFlow(rg)
    drain_area = accumulator.calc_flowacc(rg, z, flowdirs)
    z[interior_nodes] = z[interior_nodes] + uplift_rate * storm_duration
    z[outlet_loc] = zoutlet
    plt.loglog(np.array(drain_area), np.array(max_slopes), 'ro')
    plt.show()
    imshow_grid(rg, z, values_at='node')


if __name__ == '__main__':
    main()
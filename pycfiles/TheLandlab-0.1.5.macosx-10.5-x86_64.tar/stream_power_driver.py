# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/examples/stream_power_driver.py
# Compiled at: 2015-02-11 19:25:27
from landlab.components.flow_routing.route_flow_dn import FlowRouter
from landlab.components.stream_power.fastscape_stream_power import SPEroder
from landlab import ModelParameterDictionary
from landlab.plot import channel_profile as prf
from landlab.plot.imshow import imshow_node_grid
from landlab import RasterModelGrid
import numpy as np, pylab
from time import time
input_file = './stream_power_params.txt'
inputs = ModelParameterDictionary(input_file)
nrows = inputs.read_int('nrows')
ncols = inputs.read_int('ncols')
dx = inputs.read_float('dx')
leftmost_elev = inputs.read_float('leftmost_elevation')
initial_slope = inputs.read_float('initial_slope')
uplift_rate = inputs.read_float('uplift_rate')
runtime = inputs.read_float('total_time')
dt = inputs.read_float('dt')
nt = int(runtime // dt)
uplift_per_step = uplift_rate * dt
mg = RasterModelGrid(nrows, ncols, dx)
mg.create_node_array_zeros('topographic_elevation')
z = mg.create_node_array_zeros() + leftmost_elev
z += initial_slope * np.amax(mg.node_y) - initial_slope * mg.node_y
mg['node']['topographic_elevation'] = z + np.random.rand(len(z)) / 100000.0
mg.set_closed_boundaries_at_grid_edges(False, True, False, True)
print 'Running ...'
fr = FlowRouter(mg)
sp = SPEroder(mg, input_file)
time_on = time()
for i in xrange(nt):
    mg['node']['topographic_elevation'][mg.core_nodes] += uplift_per_step
    mg = fr.route_flow(grid=mg)
    mg = sp.erode(mg)
    pylab.figure(6)
    profile_IDs = prf.channel_nodes(mg, mg.at_node['steepest_slope'], mg.at_node['drainage_area'], mg.at_node['upstream_ID_order'], mg.at_node['flow_receiver'])
    dists_upstr = prf.get_distances_upstream(mg, len(mg.at_node['steepest_slope']), profile_IDs, mg.at_node['links_to_flow_receiver'])
    prf.plot_profiles(dists_upstr, profile_IDs, mg.at_node['topographic_elevation'])
    print 'Completed loop ', i

print 'Completed the simulation. Plotting...'
time_off = time()
pylab.figure(1)
pylab.close()
pylab.figure(1)
im = imshow_node_grid(mg, 'water_discharges', cmap='Blues')
pylab.figure(2)
im = imshow_node_grid(mg, 'topographic_elevation')
elev = mg['node']['topographic_elevation']
elev_r = mg.node_vector_to_raster(elev)
pylab.figure(3)
im = pylab.plot(mg.dx * np.arange(nrows), elev_r[:, int(ncols // 2)])
pylab.title('N-S cross_section')
pylab.figure(4)
im = pylab.plot(mg.dx * np.arange(ncols), elev_r[int(nrows // 4), :])
pylab.title('E-W cross_section')
drainage_areas = mg['node']['drainage_area'][mg.get_interior_nodes()]
steepest_slopes = mg['node']['steepest_slope'][mg.get_interior_nodes()]
pylab.figure(5)
pylab.loglog(drainage_areas, steepest_slopes, 'x')
pylab.xlabel('Upstream drainage area, m^2')
pylab.ylabel('Maximum slope')
print 'Done.'
print 'Time: ', time_off - time_on
pylab.show()
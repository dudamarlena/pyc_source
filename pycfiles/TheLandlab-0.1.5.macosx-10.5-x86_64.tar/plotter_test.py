# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/examples/plotter_test.py
# Compiled at: 2015-02-11 19:25:27
from landlab.components.flow_routing.route_flow_dn import FlowRouter
from landlab.components.stream_power.fastscape_stream_power import SPEroder
from landlab import ModelParameterDictionary
from landlab.plot import imshow
from landlab.plot.video_out import VideoPlotter
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
runtime = 40.0
dt = 1.0
nt = int(runtime // dt)
uplift_per_step = uplift_rate * dt
mg = RasterModelGrid(nrows, ncols, dx)
mg.set_inactive_boundaries(False, True, False, True)
mg.create_node_array_zeros('topographic_elevation')
z = mg.create_node_array_zeros() + leftmost_elev
z += initial_slope * np.amax(mg.node_y) - initial_slope * mg.node_y
mg['node']['topographic_elevation'] = z + np.random.rand(len(z)) / 100000.0
print 'Running ...'
fr = FlowRouter(mg)
sp = SPEroder(mg, input_file)
vid = VideoPlotter(mg, data_centering='node')
time_on = time()
for i in xrange(nt):
    print 'loop ', i
    mg['node']['topographic_elevation'][mg.core_nodes] += uplift_per_step
    mg = fr.route_flow(grid=mg)
    mg = sp.erode(mg)
    vid.add_frame(mg, mg.hillshade(alt=15.0), cmap='gray')

print 'Completed the simulation. Plotting...'
time_off = time()
elev = mg['node']['topographic_elevation']
print 'Done.'
print 'Time: ', time_off - time_on
vid.produce_video(override_min_max=(0, 1))
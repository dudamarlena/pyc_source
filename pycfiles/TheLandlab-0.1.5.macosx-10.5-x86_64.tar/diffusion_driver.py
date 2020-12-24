# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/examples/diffusion_driver.py
# Compiled at: 2015-02-11 19:25:27
from landlab.components.nonlinear_diffusion.Perron_nl_diffuse import PerronNLDiffuse
from landlab.components.diffusion.diffusion import DiffusionComponent
from landlab import ModelParameterDictionary
from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_node_grid
import numpy as np, pylab
input_file = './diffusion_test_params.txt'
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
mg['node']['topographic_elevation'] = z + np.random.rand(len(z)) / 100000.0
mg.set_fixed_value_boundaries_at_grid_edges(True, True, True, True)
print 'Running ...'
diffuse = PerronNLDiffuse(mg, input_file)
lin_diffuse = DiffusionComponent(grid=mg, input_stream=input_file)
uplifted_nodes = mg.get_core_nodes()
for i in xrange(nt):
    mg = diffuse.diffuse(mg, i * dt)
    pylab.figure(1)
    elev_r = mg.node_vector_to_raster(mg['node']['topographic_elevation'])
    im = pylab.plot(mg.dx * np.arange(nrows), elev_r[:, int(ncols // 2)])
    print 'Completed loop ', i

print 'Completed the simulation. Plotting...'
pylab.figure(1)
pylab.title('N-S cross_section, nonlinear diffusion')
pylab.xlabel('Distance')
pylab.ylabel('Elevation')
pylab.figure(2)
im_nl = imshow_node_grid(mg, 'topographic_elevation')
pylab.figure(3)
elev_r = mg.node_vector_to_raster(mg['node']['topographic_elevation'])
im = pylab.plot(mg.dx * np.arange(nrows), elev_r[:, int(ncols // 2)])
print 'Done.'
mg['node']['topographic_elevation'] = z + np.random.rand(len(z)) / 100000.0
print 'Running ...'
for i in xrange(nt):
    mg['node']['topographic_elevation'][uplifted_nodes] += uplift_per_step
    mg = lin_diffuse.diffuse(mg, internal_uplift=False)
    pylab.figure(4)
    elev_r = mg.node_vector_to_raster(mg['node']['topographic_elevation'])
    im = pylab.plot(mg.dx * np.arange(nrows), elev_r[:, int(ncols // 2)])
    print 'Completed loop ', i

print 'Completed the simulation. Plotting...'
pylab.figure(4)
pylab.title('N-S cross_section, linear diffusion')
pylab.xlabel('Distance')
pylab.ylabel('Elevation')
pylab.figure(5)
im = imshow_node_grid(mg, 'topographic_elevation')
pylab.figure(3)
elev_r = mg.node_vector_to_raster(mg['node']['topographic_elevation'])
im = pylab.plot(mg.dx * np.arange(nrows), elev_r[:, int(ncols // 2)])
pylab.xlabel('Distance')
pylab.ylabel('Elevation')
pylab.show()
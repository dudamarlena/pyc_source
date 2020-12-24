# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/examples/slope_aspect_routines_comparison.py
# Compiled at: 2015-02-11 19:25:27
from landlab import RasterModelGrid
import matplotlib.pyplot as plt, numpy as np
from landlab.plot.imshow import imshow_field, imshow_grid
grid = RasterModelGrid(53, 67, 10.0)
elev = np.load('elevation_NS.npy')
grid['node']['Elevation'] = elev
ids = grid.node_index_at_cells
slope_Burrough, aspect_Burrough = grid.calculate_slope_aspect_at_nodes_Burrough(ids, vals='Elevation')
slope_horn, aspect_horn = grid.calculate_slope_aspect_at_nodes_horn(ids, vals='Elevation')
slope_BFP, aspect_BFP = grid.calculate_slope_aspect_at_nodes_bestFitPlane(ids, elev)
slope_NSP = grid.node_slopes_using_patches(elevs='Elevation', unit='degrees')
pic = 0
plt.figure(pic)
imshow_field(grid, 'Elevation', values_at='node', grid_units=('m', 'm'))
plt.title('Elevation in m')
pic += 1
plt.figure(pic)
imshow_grid(grid, np.degrees(slope_Burrough), values_at='cell', grid_units=('m', 'm'))
plt.title('Slope in degrees - Burrough 1998')
pic += 1
plt.figure(pic)
imshow_grid(grid, np.degrees(aspect_Burrough), values_at='cell', grid_units=('m', 'm'))
plt.title('Aspect in degrees - Burrough 1998')
pic += 1
plt.figure(pic)
imshow_grid(grid, np.degrees(slope_horn), values_at='cell', grid_units=('m', 'm'))
plt.title('Slope in degrees - Horn')
pic += 1
plt.figure(pic)
imshow_grid(grid, np.degrees(aspect_horn), values_at='cell', grid_units=('m', 'm'))
plt.title('Aspect in degrees - Horn')
pic += 1
plt.figure(pic)
imshow_grid(grid, np.degrees(slope_BFP), values_at='cell', grid_units=('m', 'm'))
plt.title('Slope in degrees - bestFitPlane')
pic += 1
plt.figure(pic)
imshow_grid(grid, np.degrees(aspect_BFP), values_at='cell', grid_units=('m', 'm'))
plt.title('Aspect in degrees - bestFitPlane')
pic += 1
plt.figure(pic)
imshow_grid(grid, slope_NSP, values_at='node', grid_units=('m', 'm'))
plt.title('Slope in degrees - Node Slopes using Patches')
plt.show()
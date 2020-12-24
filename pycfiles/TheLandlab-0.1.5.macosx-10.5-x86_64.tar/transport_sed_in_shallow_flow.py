# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/sed_trp_shallow_flow/transport_sed_in_shallow_flow.py
# Compiled at: 2015-02-11 19:25:27
"""

2D numerical model of shallow-water flow over topography read from a DEM, using
the Bates et al. (2010) algorithm for storage-cell inundation modeling.

1st stab at componentizing this routine, following GT, by DEJH, Oct 2013.

"""
from landlab import ModelParameterDictionary
import numpy as np

class SurfaceFlowTransport(object):

    def __init__(self, grid, input_stream):
        self.grid = grid
        inputs = ModelParameterDictionary(input_stream)
        self.n = inputs.read_float('n')
        self.g = inputs.read_float('g')
        self.alpha = inputs.read_float('alpha')
        self.tau_crit = inputs.read_float('tau_crit')
        self.mpm = inputs.read_float('mpm')
        self.erode_start_time = inputs.read_float('erode_start_time')
        try:
            self.z = grid.at_node['topographic_elevation']
        except:
            print 'elevations not found in grid!'

        try:
            self.h = grid.at_node['planet_surface__water_depth']
        except:
            print 'initial water depths not found in grid!'

        self.rhog = 9810.0
        self.q = grid.create_active_link_array_zeros()
        self.dhdt = grid.create_node_array_zeros()
        self.tau = grid.create_active_link_array_zeros()
        self.qs = grid.create_active_link_array_zeros()
        self.dqsds = grid.create_node_array_zeros()
        self.dzdt = self.dhdt
        self.dzaccum = grid.create_node_array_zeros()
        self.zm = grid.create_node_array_zeros()
        self.zm[:] = self.z[:]

    def set_and_return_dynamic_timestep(self):
        self.dtmax = self.alpha * self.grid.dx / np.sqrt(self.g * np.amax(self.h))
        return self.dtmax

    def set_timestep(self, timestep_in):
        """
        This fn allows overriding of the inbuilt dynamic timestepping, if, e.g.,
        another component requires a shorter timestep.
        Function assumes you have already called self.
        set_and_return_dynamic_timestep() to establish what the min should be.
        """
        if timestep_in <= self.dtmax:
            self.dtmax = timestep_in
        else:
            raise RuntimeError('Attempting to manually set an unstable timestep! Abort! Abort!')

    def transport_sed(self, elapsed_time):
        grid = self.grid
        z = self.z
        h = self.h
        g = self.g
        n = self.n
        tau_crit = self.tau_crit
        q = self.q
        qs = self.qs
        tau = self.tau
        rhog = self.rhog
        alpha = self.alpha
        mpm = self.mpm
        zm = self.zm
        dtmax = self.dtmax
        erode_start_time = self.erode_start_time
        ten_thirds = 10.0 / 3.0
        interior_cells = grid.get_active_cell_node_ids()
        zmax = grid.max_of_link_end_node_values(z)
        w = h + z
        wmax = grid.max_of_link_end_node_values(w)
        hflow = wmax - zmax
        water_surface_slope = grid.calculate_gradients_at_active_links(w)
        q = (q - g * hflow * dtmax * water_surface_slope) / (1.0 + g * hflow * dtmax * n * n * abs(q) / hflow ** ten_thirds)
        tau = -rhog * hflow * water_surface_slope
        tauex = abs(tau) - tau_crit
        tauex[np.where(tauex < 0.0)] = 0.0
        qs = np.sign(tau) * mpm * pow(tauex, 1.5)
        dqds = grid.calculate_flux_divergence_at_nodes(q)
        dqsds = grid.calculate_flux_divergence_at_nodes(qs)
        dhdt = -dqds
        dzdt = -dqsds
        excess_time = 0.0
        if np.amin(dhdt) < 0.0:
            shallowing_locations = np.where(dhdt < 0.0)
            time_to_drain = -h[shallowing_locations] / dhdt[shallowing_locations]
            dtmax2 = alpha * np.amin(time_to_drain)
            min_timestep_ratio = int(dtmax // dtmax2)
            if min_timestep_ratio:
                excess_time = dtmax / dtmax2 - min_timestep_ratio
                dt = dtmax2
            else:
                dt = dtmax
        else:
            min_timestep_ratio = 0
            dt = dtmax
        for i in xrange(min_timestep_ratio + 1):
            h[interior_cells] += dhdt[interior_cells] * dt
            if elapsed_time >= erode_start_time:
                zm[interior_cells] += dzdt[interior_cells] * dt

        if excess_time:
            h[interior_cells] += dhdt[interior_cells] * dt * excess_time
            if elapsed_time >= erode_start_time:
                zm[interior_cells] += dzdt[interior_cells] * dt * excess_time
        self.z = z
        self.h = h
        self.q = q
        self.qs = qs
        self.tau = tau
        self.zm = zm
        self.grid['node']['topographic_elevation'] = zm
        self.grid['node']['planet_surface__water_depth'] = h
        return self.grid
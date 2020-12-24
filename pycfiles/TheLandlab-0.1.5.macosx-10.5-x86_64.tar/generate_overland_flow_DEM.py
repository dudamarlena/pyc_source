# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/overland_flow/generate_overland_flow_DEM.py
# Compiled at: 2015-02-11 19:25:27
""" generate_overland_flow.py 

 This component simulates overland flow using
 the 2-D numerical model of shallow-water flow
 over topography using the Bates et al. (2010)
 algorithm for storage-cell inundation modeling.

Written by Greg Tucker, Nicole Gasparini and Jordan Adams

"""
from landlab import Component, ModelParameterDictionary
from landlab.components.detachment_ltd_sed_trp.generate_detachment_ltd_transport import DetachmentLtdErosion
import pylab, numpy as np
from matplotlib import pyplot as plt
from math import atan, degrees
import os, csv
f = open('C:\\Users\\Jordan\\Dropbox\\z.csv', 'w')
_DEFAULT_INPUT_FILE = os.path.join(os.path.dirname(__file__), 'overland_flow_input.txt')

class OverlandFlow(Component):
    """  Landlab component that simulates overland flow using the Bates et al., (2010) approximations
of the 1D shallow water equations to be used for 2D flood inundation modeling. 
    
This component calculates discharge, depth and shear stress after some precipitation event across
any raster grid. Default input file is named "overland_flow_input.txt' and is contained in the
landlab.components.overland_flow folder.
        
    Inputs
    ------
    grid : Requires a RasterGridModel instance
        
    input_file : Contains necessary and optional inputs. If not given, default input file is used.
        - Manning's n is REQUIRED.
        - Storm duration is needed IF rainfall_duration is not passed in the initialization
        - Rainfall intensity is needed IF rainfall_intensity is not passed in the initialization
        - Model run time can be provided in initialization. If not it is set to the storm duration
        
    Constants
    ---------
    h_init : float
        Some initial depth in the channels. Default = 0.001 m
    g : float
        Gravitational acceleration, \x0crac{m}{s^2}
    alpha : float
        Non-dimensional time step factor from Bates et al., (2010)
    rho : integer
        Density of water, \x0crac{kg}{m^3}
    ten_thirds : float
        Precalculated value of \x0crac{10}{3} which is used in the implicit shallow water equation.
            
            
    >>> DEM_name = 'DEM_name.asc'
    >>> (rg, z) = read_esri_ascii(DEM_name) # doctest: +SKIP
    >>> of = OverlandFlow(rg) # doctest: +SKIP
       
"""
    _name = 'OverlandFlow'
    _input_var_names = set([
     'water_depth',
     'rainfall_intensity',
     'rainfall_duration',
     'elevation'])
    _output_var_names = set([
     'water_depth',
     'water_discharge',
     'shear_stress',
     'water_discharge_at_nodes',
     'slope_at_nodes'])
    _var_units = {'water_depth': 'm', 
       'rainfall_intensity': 'm/s', 
       'rainfall_duration': 's', 
       'water_discharge': 'm3/s', 
       'shear_stress': 'Pa', 
       'water_discharge_at_nodes': 'm3/s', 
       'slope_at_nodes': 'm/m', 
       'elevation': 'm'}

    def __init__(self, grid, input_file=None, detach_ltd=True, **kwds):
        self.h_init = kwds.pop('h_init', 0.001)
        self.alpha = kwds.pop('alpha', 0.2)
        self.rho = kwds.pop('rho', 1000)
        self.m_n = kwds.pop('Mannings_n', 0.04)
        self.rainfall_intensity = kwds.pop('rainfall_intensity', None)
        self.rainfall_duration = kwds.pop('rainfall_duration', None)
        self.model_duration = kwds.pop('model_duration', None)
        super(OverlandFlow, self).__init__(grid, **kwds)
        for name in self._input_var_names:
            if name not in self.grid.at_node:
                self.grid.add_zeros('node', name, units=self._var_units[name])

        for name in self._output_var_names:
            if name not in self.grid.at_node:
                self.grid.add_zeros('node', name, units=self._var_units[name])

        self._nodal_values = self.grid['node']
        self._link_values = self.grid['active_link']
        self._water_discharge = grid.add_zeros('active_link', 'water_discharge', units=self._var_units['water_discharge'])
        self.g = 9.8
        self.ten_thirds = 10.0 / 3.0
        self.current_time = 0.0
        self.m_n_sq = self.m_n * self.m_n
        self.elapsed_time = 0
        self.q_at_node = []
        self.time = []
        self.detach_ltd = detach_ltd
        MPD = ModelParameterDictionary()
        if input_file is None:
            input_file = _DEFAULT_INPUT_FILE
        MPD.read_from_file(input_file)
        if self.rainfall_duration == None:
            self.rainfall_duration = MPD.read_float('RAINFALL_DURATION')
        if self.rainfall_intensity == None:
            self.rainfall_intensity = MPD.read_float('RAINFALL_INTENSITY')
        if self.model_duration == None:
            self.total_time = self.rainfall_duration
        if self.detach_ltd == True:
            self.dl = DetachmentLtdErosion(self.grid)
        self.hstart = grid.zeros(centering='node') + self.h_init
        self.h = grid.zeros(centering='node') + self.h_init
        self.dhdt = grid.zeros(centering='cell')
        self.dqds = grid.zeros(centering='node')
        self.q = grid.zeros(centering='active_link')
        self.tau = grid.zeros(centering='node')
        self.total_dzdt = grid.zeros(centering='node')
        self.h = self.hstart
        return

    def flow_at_one_node(self, grid, z, study_node, **kwds):
        """
        Outputs water depth, discharge and shear stress values through time at
        a user-selected point, defined as the "study_node" in function arguments.

        
        Inputs
        ------
        grid : Requires a RasterGridModel instance
        
        z : elevations drawn from the grid
        
        study_node : node ID for the the node at which discharge, depth and shear stress are calculated
        
        total_t : total model run time. If not provided as an argument or in the input_file, it is set to the storm_duration
        
        rainfall_intensity : rainfall intensity in m/s. If not provided as an argument, it must come from the input file.
        
        self.rainfall_duration : storm duration in seconds. If not provided as an argument, it must come from the input file.
        
        >>> study_row = 10
        >>> study_column = 10
        >>> rg.node_coords_to_id(study_row, study_column) # doctest: +SKIP
        >>> of.flow_at_one_node(rg, z, study_node, model_duration, storm_intensity, storm_duration) # doctest: +SKIP
        
        The study_node should NOT be a boundary node.
        """
        self.q_node = grid.zeros(centering='node')
        self.interior_nodes = grid.get_active_cell_node_ids()
        self.active_links = grid.active_links
        self._water_depth = self._nodal_values['water_depth']
        self._slope_at_nodes = self._nodal_values['slope_at_nodes']
        self._shear_stress = self._nodal_values['shear_stress']
        self._water_discharge = self._link_values['water_discharge']
        self.rainfall_duration = kwds.pop('rainfall_duration', self.rainfall_duration)
        self.rainfall_intensity = kwds.pop('rainfall_intensity', self.rainfall_intensity)
        self.interstorm_duration = kwds.pop('interstorm_duration', 0)
        self.model_duration = kwds.pop('model_duration', self.rainfall_duration)
        self.z = z
        self.elapsed_time = kwds.pop('elapsed_time', 0)
        self.model_duration += self.interstorm_duration
        self.h_thresh = 1 * 1e-06
        self.study_node = study_node
        self.interior_nodes = grid.get_active_cell_node_ids()
        self.active_links = grid.active_links
        self.time = [
         0]
        self.q_study = [
         0]
        self.tau_study = [
         0]
        self.depth_study = [
         0]
        self.q_node = grid.zeros(centering='node')
        self.tau_node = grid.zeros(centering='node')
        self.dqds = grid.zeros(centering='node')
        while self.elapsed_time < self.model_duration:
            dtmax = self.alpha * grid.dx / np.sqrt(self.g * np.amax(self.h))
            dt = min(dtmax, self.model_duration)
            zmax = grid.max_of_link_end_node_values(z)
            w = self.h + self.z
            wmax = grid.max_of_link_end_node_values(w)
            hflow = wmax - zmax
            water_surface_slope = grid.calculate_gradients_at_active_links(w)
            above_thresh = np.where(hflow > self.h_thresh)
            below_thresh = np.where(hflow < self.h_thresh)
            self.q[above_thresh] = (self.q[above_thresh] - self.g * hflow[above_thresh] * dtmax * water_surface_slope[above_thresh]) / (1.0 + self.g * hflow[above_thresh] * dtmax * 0.06 * 0.06 * (abs(self.q[above_thresh]) / hflow[above_thresh] ** self.ten_thirds))
            self.q[below_thresh] = 0.0
            self.dqds = grid.calculate_flux_divergence_at_nodes(self.q)
            if self.elapsed_time > self.rainfall_duration:
                self.rainfall_intensity = 0.0
            self.dhdt = self.rainfall_intensity - self.dqds
            if np.amin(self.dhdt) < 0.0:
                shallowing_locations = np.where(self.dhdt < 0.0)
                time_to_drain = -self.h[shallowing_locations] / self.dhdt[shallowing_locations]
                dtmax2 = self.alpha * np.amin(time_to_drain)
                dt = np.min([dtmax, dtmax2, self.model_duration])
            else:
                dt = dtmax
            self.h[self.interior_nodes] = self.h[self.interior_nodes] + self.dhdt[self.interior_nodes] * dt
            self.slopes_at_node, garbage = grid.calculate_steepest_descent_on_nodes(w, water_surface_slope)
            self._water_discharge_at_nodes = self.get_summed_out_discharge_at_nodes()
            tau_temp = self.rho * self.g * self.slopes_at_node[study_node] * self.h[study_node]
            self.tau_study.append(tau_temp)
            self.depth_study.append(self.h[study_node])
            self.q_study.append(self._water_discharge_at_nodes[study_node])
            self.time.append(self.elapsed_time)
            self.elapsed_time += dt
            print 'elapsed time', self.elapsed_time

        self._water_depth[self.interior_nodes] = self.h[self.interior_nodes]
        self._water_discharge = self.q
        self._slope_at_nodes[self.interior_nodes] = self.slopes_at_node[self.interior_nodes]

    def update_at_one_point(self, grid, rainfall_duration, model_duration, rainfall_intensity, **kwds):
        """
        The update_at_one_point() method, for now, requires our grid (which has fields associated with it),
        a new rainfall_duration, model_durationa and rainfall_intensity until I figure out some clever way to update using
        the MPD. 
        
        This function updates the overall elapsed time and passes it as an optional argument to flow_at_one_node().
        hstart is updated to be the depths from the field (_water_depth), model duration is updated to include past calls to
        flow_at_one_node() and/or update_at_one_node() depending on the past model run.
    
        Rainfall_duration is also updated so that model time will continue sequentially.
        """
        elapsed = self.elapsed_time
        self.hstart = self._water_depth
        model_dur = model_duration + self.elapsed_time
        rain_dur = rainfall_duration + self.elapsed_time
        intens = rainfall_intensity
        self.flow_at_one_node(grid, self.z, self.study_node, rainfall_duration=rain_dur, rainfall_intensity=intens, model_duration=model_dur, elapsed_time=elapsed)
        print '\n', '\n'

    def flow_across_grid(self, grid, z, detach_ltd=True, **kwds):
        """
        Outputs water depth, discharge and shear stress values through time at
        every point in the input grid.

        
        Inputs
        ------
        grid : Requires a RasterGridModel instance
        
        z : elevations drawn from the grid
     
        total_t : total model run time. If not provided as an argument or in the input_file, it is set to the storm_duration
        
        rainfall_intensity : rainfall intensity in m/s. If not provided as an argument, it must come from the input file.
        
        rainduration : storm duration in seconds. If not provided as an argument, it must come from the input file.
        
        """
        self.interior_nodes = grid.get_active_cell_node_ids()
        self.active_links = grid.active_links
        self._shear_stress = self._nodal_values['shear_stress']
        self._water_discharge = self._link_values['water_discharge']
        self._slope_at_nodes = self._nodal_values['slope_at_nodes']
        self.elevation = self._nodal_values['elevation']
        self.rainfall_duration = kwds.pop('rainfall_duration', self.rainfall_duration)
        self.rainfall_intensity = kwds.pop('rainfall_intensity', self.rainfall_intensity)
        self.interstorm_duration = kwds.pop('interstorm_duration', 0)
        self.model_duration = kwds.pop('model_duration', self.rainfall_duration)
        self._water_depth = self._nodal_values['water_depth']
        self.z = z
        self.elapsed_time = kwds.pop('elapsed_time', 0)
        self.model_duration += self.interstorm_duration
        self.h_thresh = 1 * 1e-06
        while self.elapsed_time < self.model_duration:
            dtmax = self.alpha * grid.dx / np.sqrt(self.g * np.amax(self.h))
            dt = min(dtmax, self.model_duration)
            zmax = grid.max_of_link_end_node_values(z)
            w = self.h + self.z
            wmax = grid.max_of_link_end_node_values(w)
            hflow = wmax - zmax
            water_surface_slope = grid.calculate_gradients_at_active_links(w)
            above_thresh = np.where(hflow > self.h_thresh)
            below_thresh = np.where(hflow < self.h_thresh)
            self.q[above_thresh] = (self.q[above_thresh] - self.g * hflow[above_thresh] * dtmax * water_surface_slope[above_thresh]) / (1.0 + self.g * hflow[above_thresh] * dtmax * 0.06 * 0.06 * (abs(self.q[above_thresh]) / hflow[above_thresh] ** self.ten_thirds))
            self.q[below_thresh] = 0.0
            self.dqds = grid.calculate_flux_divergence_at_nodes(self.q, self.dqds)
            if self.elapsed_time > self.rainfall_duration:
                self.rainfall_intensity = 0
            self.dhdt = self.rainfall_intensity - self.dqds
            if np.amin(self.dhdt) < 0.0:
                shallowing_locations = np.where(self.dhdt < 0.0)
                time_to_drain = -self.h[shallowing_locations] / self.dhdt[shallowing_locations]
                dtmax2 = self.alpha * np.amin(time_to_drain)
                dt = np.min([dtmax, dtmax2, self.model_duration])
            else:
                dt = dtmax
            self.h[self.interior_nodes] = self.h[self.interior_nodes] + self.dhdt[self.interior_nodes] * dt
            w = self.h + self.z
            self.slopes_at_node, dwnstr_nodes = grid.calculate_steepest_descent_on_nodes(w, water_surface_slope)
            self.tau = self.rho * self.g * self.slopes_at_node * self.h
            self._water_discharge_at_nodes = self.get_summed_out_discharge_at_nodes()
            self.slopes_at_node[np.where(self.slopes_at_node < 0)] = 0.0
            if self.detach_ltd == True:
                new_z, dzdt = self.dl.change_elev(self.z, self.slopes_at_node, self._water_discharge_at_nodes)
            self.z_f = new_z
            self.total_dzdt += dzdt
            self.elapsed_time += dt
            print 'elapsed time', self.elapsed_time

        self._water_depth[self.interior_nodes] = self.h.take(self.interior_nodes)
        self._shear_stress[self.interior_nodes] = self.tau.take(self.interior_nodes)
        self._water_discharge = self.q
        self._slope_at_nodes[self.interior_nodes] = self.slopes_at_node.take(self.interior_nodes)

    def update_across_grid(self, grid, rainfall_duration, model_duration, rainfall_intensity, **kwds):
        """
        The update_across_grid() method, for now, requires our grid (which has fields associated with it),
        a new rainfall_duration, model_durationa and rainfall_intensity until I figure out some clever way to update using
        the MPD. 
        
        This function updates the overall elapsed time and passes it as an optional argument to flow_across_grid().
        hstart is updated to be the depths from the field (_water_depth), model duration is updated to include past calls to
        flow_across_grid() and/or update_across_grid() depending on the past model run.
    
        Rainfall_duration is also updated so that model time will continue sequentially.
        """
        elapsed = self.elapsed_time
        self.hstart = self._water_depth
        model_dur = model_duration + self.elapsed_time
        rain_dur = rainfall_duration + self.elapsed_time
        intens = rainfall_intensity
        self.flow_across_grid(grid, self.z, rainfall_duration=rain_dur, rainfall_intensity=intens, model_duration=model_dur, elapsed_time=elapsed)

    def get_summed_out_discharge_at_nodes(self):
        """ 
        For each interior node, this method finds the links where discharge is flowing out and maps
        the sum of these "q_out" links to the respective interior node
        """
        discharge_array = self.q[self.grid.node_activelinks(self.interior_nodes)]
        south = discharge_array[0]
        west = discharge_array[1]
        north = discharge_array[2]
        east = discharge_array[3]
        south[np.where(south > 0)] = 0.0
        west[np.where(west > 0)] = 0.0
        south[np.where(south < 0)] = south[np.where(south < 0)] * -1
        west[np.where(west < 0)] = west[np.where(west < 0)] * -1
        north[np.where(north < 0)] = 0.0
        east[np.where(east < 0)] = 0.0
        q_node = south + west + north + east
        self.q_interior_nodes = self.grid.zeros(centering='node')
        self.q_interior_nodes[self.interior_nodes] = q_node
        self._water_discharge_at_nodes = self.q_interior_nodes
        return self._water_discharge_at_nodes

    def plot_at_one_node(self):
        """This method must follow a call to the flow_at_one_node() method.
        
        It plots depth, discharge and shear stress through time at the study
        node that was called in the flow_at_one_node() method.
        
           Three windows will appear after this method is called:
               1. Discharge through time is plotted as a solid blue line.
               2. Shear stress through time is plotted as a solid red line.
               3. Water depth through time is plotted as a solid cyan line.
        """
        plt.figure('Discharge at Study Node')
        plt.plot(self.time, self.q_study, 'b-')
        plt.legend(loc=1)
        plt.ylabel('Discharge, m^3/s')
        plt.xlabel('Time, s')
        plt.figure('Shear Stress at Study Node')
        plt.plot(self.time, self.tau_study, 'r-')
        plt.ylabel('Shear Stress, Pa')
        plt.xlabel('Time, s')
        plt.legend(loc=1)
        plt.figure('Water Depth at Study Node')
        plt.plot(self.time, self.depth_study, 'c-')
        plt.ylabel('Water Depth, m')
        plt.xlabel('Time, s')
        plt.legend(loc=1)
        plt.show()
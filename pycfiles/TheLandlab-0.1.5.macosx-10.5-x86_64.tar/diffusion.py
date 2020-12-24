# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/diffusion/diffusion.py
# Compiled at: 2015-02-11 19:25:27
"""

Component that models 2D diffusion using an explicit finite-volume method.

Created July 2013 GT
Last updated August 2013 GT

"""
from landlab import ModelParameterDictionary
from landlab import create_and_initialize_grid
_ALPHA = 0.1
_VERSION = 'pass_grid'

class DiffusionComponent:
    """
    This component implements linear diffusion of a field in the supplied
    ModelGrid.
    
    This components requires the following parameters be set in the input file,
    *input_stream*, set in the component initialization:
        
        'DIFMOD_UPLIFT_RATE' or 'uplift_rate', both equivalent to the uplift rate
        'DIFMOD_KD', the diffusivity to use
    
    Optional inputs are:
        
        'dt', the model timestep (assumed constant)
        'values_to_diffuse', a string giving the name of the grid field
        containing the data to diffuse.
    
    If 'dt' is not supplied, you must call the method :func:`set_timestep` as
    part of your run loop. This allows you to set a dynamic timestep for this
    class.
    If 'values_to_diffuse' is not provided, defaults to 
    'topographic_elevation'.
    
    No particular units are necessary where they are not specified, as long as
    all units are internally consistent.
    
    The component takes *grid*, the ModelGrid object, and (optionally)
    *current_time* and *input_stream*. If *current_time* is not set, it defaults
    to 0.0. If *input_stream* is not set in instantiation of the class,
    :func:`initialize` with *input_stream* as in input must be called instead.
    *Input_stream* is the filename of (& optionally, path to) the parameter 
    file.
    
    The primary method of this class is :func:`diffuse`.
    """

    def __init__(self, grid, input_stream=None, current_time=0.0):
        self.grid = grid
        self.current_time = current_time
        if input_stream:
            self.initialize(input_stream)
        else:
            print 'Ensure you call the initialize(input_stream) method before running the model!'

    def initialize(self, input_stream):
        if type(input_stream) == ModelParameterDictionary:
            inputs = input_stream
        else:
            inputs = ModelParameterDictionary(input_stream)
        self.kd = inputs.read_float('DIFMOD_KD')
        try:
            self.uplift_rate = inputs.read_float('DIFMOD_UPLIFT_RATE')
        except:
            self.uplift_rate = inputs.read_float('uplift_rate')

        try:
            self.values_to_diffuse = inputs.read_str('values_to_diffuse')
        except:
            self.values_to_diffuse = 'topographic_elevation'

        try:
            self.timestep_in = inputs.read_float('dt')
        except:
            print 'No fixed timestep supplied, it must be set dynamically somewhere else. Be sure to call input_timestep(timestep_in) as part of your run loop.'

        if self.grid == None:
            self.grid = create_and_initialize_grid(input_stream)
        dx = self.grid.min_active_link_length()
        self.dt = _ALPHA * dx * dx / self.kd
        try:
            self.tstep_ratio = self.timestep_in / self.dt
        except:
            pass

        self.interior_cells = self.grid.get_core_cell_node_ids()
        if _VERSION == 'make_all_data':
            self.z = self.grid.add_zeros('node', 'landscape_surface__elevation')
            self.g = self.grid.add_zeros('active_link', 'landscape_surface__gradient')
            self.qs = self.grid.add_zeros('active_link', 'unit_sediment_flux')
            self.dqds = self.grid.add_zeros('node', 'sediment_flux_divergence')
        elif _VERSION == 'explicit':
            pass
        else:
            self.g = self.grid.create_active_link_array_zeros()
            self.qs = self.grid.create_active_link_array_zeros()
            self.dqds = self.grid.create_node_array_zeros()
        return

    def input_timestep(self, timestep_in):
        """
        Allows the user to set a dynamic (evolving) timestep manually as part of
        a run loop.
        """
        self.timestep_in = timestep_in
        self.tstep_ratio = timestep_in / self.dt

    def run_one_step_explicit(self, mg, z, g, qs, dqsds, dzdt, delt):
        dt = min(self.dt, delt)
        g = mg.calculate_gradients_at_active_links(z)
        qs = -self.kd * g
        dqsds = mg.calculate_flux_divergence_at_nodes(qs)
        dzdt = self.uplift_rate - dqsds
        z[self.interior_cells] = z[self.interior_cells] + dzdt[self.interior_cells] * dt
        self.current_time += dt
        return (
         z, g, qs, dqsds, dzdt)

    def run_one_step_internal(self, delt):
        dt = min(self.dt, delt)
        self.g = self.grid.calculate_gradients_at_active_links(self.z)
        self.qs = -self.kd * self.g
        self.dqsds = self.grid.calculate_flux_divergence_at_nodes(self.qs)
        dzdt = self.uplift_rate - self.dqsds
        self.z[self.interior_cells] += dzdt[self.interior_cells] * dt
        self.current_time += dt
        return self.current_time

    def diffuse(self, grid, internal_uplift=True, num_uplift_implicit_comps=1):
        """
        This is the primary method of the class. Call it to perform an iteration
        of the model. Takes *grid*, the model grid.
        
        *grid* must contain the field to diffuse, which defaults to
        'topographic_elevation'. This can be overridden with the 
        values_to_diffuse property in the input file.
        
        See the class docstring for a list of the other properties necessary
        in the input file for this component to run.
        
        By default, this component requires it to incorporate uplift into its 
        execution. If you only have one module that requires this, do not add
        uplift manually in your loop; this method will include uplift 
        automatically. If more than one of your components has this requirement,
        set *num_uplift_implicit_comps* to the total number of components that
        do.
        
        You can suppress this behaviour by setting *internal_uplift* to False.

        """
        repeats = int(self.tstep_ratio // 1.0)
        extra_time = self.tstep_ratio - repeats
        z = grid.at_node[self.values_to_diffuse]
        core_nodes = grid.get_core_cell_node_ids()
        for i in xrange(repeats + 1):
            self.qs = -self.kd * grid.calculate_gradients_at_active_links(z)
            self.dqsds = grid.calculate_flux_divergence_at_nodes(self.qs)
            dzdt = -self.dqsds
            if i == repeats:
                timestep = extra_time
            else:
                timestep = self.dt
            if internal_uplift:
                add_uplift = self.uplift_rate / num_uplift_implicit_comps
            else:
                add_uplift = 0.0
            grid.at_node[self.values_to_diffuse][core_nodes] += add_uplift + dzdt[core_nodes] * timestep
            if grid.fixed_gradient_boundary_nodes:
                grid.at_node[self.values_to_diffuse][grid.fixed_gradient_node_properties['boundary_node_IDs']] = grid.at_node[self.values_to_diffuse][grid.fixed_gradient_node_properties['anchor_node_IDs']] + grid.fixed_gradient_node_properties['values_to_add']

        return grid

    def run_until_explicit(self, mg, t, z, g, qs, dqsds, dzdt):
        while self.current_time < t:
            remaining_time = t - self.current_time
            z, g, qs, dqsds, dzdt = self.run_one_step_explicit(mg, z, g, qs, dqsds, dzdt, remaining_time)

        return (z, g, qs, dqsds, dzdt)

    def run_until_internal(self, t):
        while self.current_time < t:
            remaining_time = t - self.current_time
            self.run_one_step_internal(remaining_time)

    def run_until(self, t):
        while self.current_time < t:
            remaining_time = t - self.current_time
            self.run_one_step_internal(remaining_time)

    def get_time_step(self):
        """
        Returns time-step size.
        """
        return self.dt

    @property
    def time_step(self):
        """
        Returns time-step size (as a property).
        """
        return self.dt
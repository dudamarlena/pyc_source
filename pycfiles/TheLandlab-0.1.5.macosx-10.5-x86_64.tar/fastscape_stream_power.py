# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/stream_power/fastscape_stream_power.py
# Compiled at: 2015-02-11 19:25:27
"""
This module attempts to "component-ify" GT's Fastscape stream power erosion.
Created DEJH, March 2014.
"""
import numpy
from landlab import ModelParameterDictionary
from landlab.core.model_parameter_dictionary import MissingKeyError, ParameterValueError
from landlab.field.scalar_data_fields import FieldError
from scipy import weave
from scipy.optimize import newton, fsolve
UNDEFINED_INDEX = numpy.iinfo(numpy.int32).max

class SPEroder(object):
    """
    This class uses the Braun-Willett Fastscape approach to calculate the amount
    of erosion at each node in a grid, following a stream power framework.
    
    On initialization, it takes *grid*, a reference to a ModelGrid, and
    *input_stream*, a string giving the filename (and optionally, path) of the
    required input file.
    
    It needs to be supplied with the key variables:
    
        *K_sp*
        
        *m_sp*
    
    ...which it will draw from the supplied input file. *n_sp*  can be any 
    value ~ 0.5<n_sp<4., but note that performance will be EXTREMELY degraded
    if n<1.
    
    If you want to supply a spatial variation in K, set K_sp to the string
    'array', and pass a field name or array to the erode method's K_if_used
    argument.
    
    *dt*, *rainfall_intensity*, and *value_field* are optional variables.
    
    *dt* is a fixed timestep, and *rainfall_intensity* is a parameter which 
    modulates K_sp (by a product, r_i**m_sp) to reflect the direct influence of
    rainfall intensity on erosivity. *value_field* is a string giving the name
    of the field containing the elevation data in the grid. It defaults to
    'topographic_elevation' if not supplied.
    
    This module assumes you have already run 
    :func:`landlab.components.flow_routing.route_flow_dn.FlowRouter.route_flow`
    in the same timestep. It looks for 'upstream_ID_order', 
    'links_to_flow_receiver', 'drainage_area', 'flow_receiver', and
    'topographic_elevation' at the nodes in the grid. 'drainage_area' should
    be in area upstream, not volume (i.e., set runoff_rate=1.0 when calling
    FlowRouter.route_flow).
    
    If dt is not supplied, you must call gear_timestep(dt_in, rain_intensity_in)
    each iteration to set these variables on-the-fly (rainfall_intensity will be
    overridden if supplied in the input file).
    If dt is supplied but rainfall_intensity is not, the module will assume you
    mean r_i = 1.
    
    The primary method of this class is :func:`erode`.
    """

    def __init__(self, grid, input_stream):
        self.grid = grid
        inputs = ModelParameterDictionary(input_stream)
        try:
            self.K = inputs.read_float('K_sp')
        except ParameterValueError:
            self.use_K = True
        else:
            self.use_K = False

        self.m = inputs.read_float('m_sp')
        try:
            self.n = inputs.read_float('n_sp')
        except:
            self.n = 1.0

        try:
            self.dt = inputs.read_float('dt')
        except:
            print 'Set dynamic timestep from the grid. You must call gear_timestep() to set dt each iteration.'

        try:
            self.r_i = inputs.read_float('rainfall_intensity')
        except:
            self.r_i = 1.0

        try:
            self.value_field = inputs.read_str('value_field')
        except:
            self.value_field = 'topographic_elevation'

        self.A_to_the_m = grid.create_node_array_zeros()
        self.alpha = grid.empty(centering='node')
        self.alpha_by_flow_link_lengthtothenless1 = numpy.empty_like(self.alpha)
        self.grid.node_diagonal_links()
        if self.n != 1.0:
            self.nonlinear_flag = True
            if self.n < 1.0:
                print '***WARNING: With n<1 performance of the Fastscape algorithm is slow!***'
        else:
            self.nonlinear_flag = False
        self.weave_flag = grid.weave_flag

        def func_for_newton(x, last_step_elev, receiver_elev, alpha_by_flow_link_lengthtothenless1, n):
            y = x - last_step_elev + alpha_by_flow_link_lengthtothenless1 * (x - receiver_elev) ** n
            return y

        def func_for_newton_diff(x, last_step_elev, receiver_elev, alpha_by_flow_link_lengthtothenless1, n):
            y = 1.0 + n * alpha_by_flow_link_lengthtothenless1 * (x - receiver_elev) ** (n - 1.0)
            return y

        self.func_for_newton = func_for_newton
        self.func_for_newton_diff = func_for_newton_diff

    def gear_timestep(self, dt_in, rainfall_intensity_in=None):
        self.dt = dt_in
        if rainfall_intensity_in is not None:
            self.r_i = rainfall_intensity_in
        return (
         self.dt, self.r_i)

    def erode(self, grid_in, K_if_used=None):
        """
        This method implements the stream power erosion, following the Braun-
        Willett (2013) implicit Fastscape algorithm. This should allow it to
        be stable against larger timesteps than an explicit stream power scheme.
        
        The method takes *grid*, a reference to the model grid.
        Set 'K_if_used' as a field name or nnodes-long array if you set K_sp as
        'array' during initialization.
        
        It returns the grid, in which it will have modified the value of 
        *value_field*, as specified in component initialization.
        """
        upstream_order_IDs = self.grid['node']['upstream_ID_order']
        z = self.grid['node'][self.value_field]
        defined_flow_receivers = numpy.not_equal(self.grid['node']['links_to_flow_receiver'], UNDEFINED_INDEX)
        flow_link_lengths = self.grid.link_length[self.grid['node']['links_to_flow_receiver'][defined_flow_receivers]]
        if K_if_used != None:
            assert self.use_K, "An array of erodabilities was provided, but you didn't set K_sp to 'array' in your input file! Aborting..."
            try:
                self.K = self.grid.at_node[K_if_used][defined_flow_receivers]
            except TypeError:
                self.K = K_if_used[defined_flow_receivers]

        numpy.power(self.grid['node']['drainage_area'], self.m, out=self.A_to_the_m)
        self.alpha[defined_flow_receivers] = self.r_i ** self.m * self.K * self.dt * self.A_to_the_m[defined_flow_receivers] / flow_link_lengths
        flow_receivers = self.grid['node']['flow_receiver']
        n_nodes = upstream_order_IDs.size
        alpha = self.alpha
        if self.nonlinear_flag == False:
            if self.weave_flag:
                code = '\n                    int current_node;\n                    int j;\n                    for (int i = 0; i < n_nodes; i++) {\n                        current_node = upstream_order_IDs[i];\n                        j = flow_receivers[current_node];\n                        if (current_node != j) {\n                            z[current_node] = (z[current_node] + alpha[current_node]*z[j])/(1.0+alpha[current_node]);\n                        }\n                    }\n                '
                weave.inline(code, ['n_nodes', 'upstream_order_IDs', 'flow_receivers', 'z', 'alpha'])
            else:
                for i in upstream_order_IDs:
                    j = flow_receivers[i]
                    if i != j:
                        z[i] = (z[i] + alpha[i] * z[j]) / (1.0 + alpha[i])

        else:
            self.alpha_by_flow_link_lengthtothenless1[defined_flow_receivers] = alpha[defined_flow_receivers] / flow_link_lengths ** (self.n - 1.0)
            alpha_by_flow_link_lengthtothenless1 = self.alpha_by_flow_link_lengthtothenless1
            n = float(self.n)
            if self.weave_flag:
                if n < 1.0:
                    for i in upstream_order_IDs:
                        j = flow_receivers[i]
                        func_for_newton = self.func_for_newton
                        func_for_newton_diff = self.func_for_newton_diff
                        if i != j:
                            z[i] = fsolve(func_for_newton, z[i], args=(z[i], z[j], alpha_by_flow_link_lengthtothenless1[i], n))

                else:
                    code = "\n                        int current_node;\n                        int j;\n                        double current_z;\n                        double previous_z;\n                        double elev_diff;\n                        double elev_diff_tothenless1;\n                        for (int i = 0; i < n_nodes; i++) {\n                            current_node = upstream_order_IDs[i];\n                            j = flow_receivers[current_node];\n                            previous_z = z[current_node];\n                            if (current_node != j) {\n                                while (1) {\n                                    elev_diff = previous_z-z[j];\n                                    elev_diff_tothenless1 = pow(elev_diff, n-1.); //this isn't defined if in some iterations the elev_diff goes -ve\n                                    current_z = previous_z - (previous_z - z[current_node] + alpha_by_flow_link_lengthtothenless1[current_node]*elev_diff_tothenless1*elev_diff)/(1.+n*alpha_by_flow_link_lengthtothenless1[current_node]*elev_diff_tothenless1);\n                                    if (abs((current_z - previous_z)/current_z) < 1.48e-08) break;\n                                    previous_z = current_z;\n                                }\n                                z[current_node] = current_z;\n                            }\n                        }\n                    "
                    weave.inline(code, ['n_nodes', 'upstream_order_IDs', 'flow_receivers', 'z', 'alpha_by_flow_link_lengthtothenless1', 'n'], headers=['<math.h>'])
            else:
                for i in upstream_order_IDs:
                    j = flow_receivers[i]
                    func_for_newton = self.func_for_newton
                    func_for_newton_diff = self.func_for_newton_diff
                    if i != j:
                        if n >= 1.0:
                            z[i] = newton(func_for_newton, z[i], fprime=func_for_newton_diff, args=(z[i], z[j], alpha_by_flow_link_lengthtothenless1[i], n), maxiter=10)
                        else:
                            z[i] = fsolve(func_for_newton, z[i], args=(z[i], z[j], alpha_by_flow_link_lengthtothenless1[i], n))

        return self.grid
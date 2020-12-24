# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/simple_power_law_incision/power_law_fluvial_eroder.py
# Compiled at: 2015-02-11 19:25:27
"""
Component for detachment-limited fluvial incision using a simple power-law model.

I = K Q^m S^n

I=incision rate (M Y^(-1) )
K=bedrock erodibility (M^(1-3m) Y^(m-1) ) #read in from input file
Q= fluvial discharge (M^3 Y^-1 )
S=slope of landscape (negative of the gradient in topography, dimensionless, 
and only applies on positive slopes)
m, n =exponents, read in from input file

NOTE, in units above M=meters.  This component assumes that variables are given
in units of meters and years, including rainfall!

NOTE, Only incision happens in this class.  NO DEPOSITION.  
NO TRACKING OF SEDIMENT FLUX.

This assumes that a grid has already been instantiated.

To run this, first instantiate the class member, then run one storm
    incisor = PowerLawIncision('input_file_name',grid)
    z = incisior.run_one_storm(grid, z, rainrate=optional, storm_duration=optional)
    
Note that the component knows the default rainfall rate (m/yr) and storm duration (yr)
so these values need not be passed in.  Elevationare eroded and sent back.
    
 
"""
from landlab import ModelParameterDictionary
from landlab.components.flow_routing.flow_routing_D8 import RouteFlowD8
from landlab.components.flow_accum.flow_accumulation2 import AccumFlow
import numpy as np

class PowerLawIncision(object):

    def __init__(self, input_stream, grid, current_time=0.0):
        self.grid = grid
        self.current_time = current_time
        self.initialize(grid, input_stream)

    def initialize(self, grid, input_stream):
        if type(input_stream) == ModelParameterDictionary:
            inputs = input_stream
        else:
            inputs = ModelParameterDictionary(input_stream)
        self.m = inputs.get('M_EXPONENT', ptype=float)
        self.n = inputs.get('N_EXPONENT', ptype=float)
        self.K = inputs.get('K_COEFFICIENT', ptype=float)
        self.rainfall_myr = inputs.get('RAINFALL_RATE_M_PER_YEAR', ptype=float)
        self.rain_duration_yr = inputs.get('RAIN_DURATION_YEARS', ptype=float)
        self.frac = 0.9
        self.I = grid.zeros(centering='node')

    def run_one_storm(self, grid, z, rainrate=None, storm_dur=None):
        if rainrate == None:
            rainrate = self.rainfall_myr
        if storm_dur == None:
            storm_dur = self.rain_duration_yr
        m = self.m
        n = self.n
        K = self.K
        frac = self.frac
        interior_nodes = grid.get_active_cell_node_ids()
        flow_router = RouteFlowD8(len(z))
        flowdirs, max_slopes = flow_router.calc_flowdirs(grid, z)
        accumulator = AccumFlow(grid)
        drain_area = accumulator.calc_flowacc(grid, z, flowdirs)
        time = 0
        dt = storm_dur
        while time < storm_dur:
            max_slopes.clip(0)
            I = -K * np.power(rainrate * drain_area, m) * np.power(max_slopes, n)
            for i in interior_nodes:
                dzdtdif = I[flowdirs[i]] - I[i]
                if dzdtdif > 0:
                    dtmin = frac * (z[i] - z[flowdirs[i]]) / dzdtdif
                    if dtmin < dt:
                        if dtmin > 0.001 * dt:
                            dt = dtmin
                        else:
                            dt = 0.001 * dt

            z = I * dt + z
            time = dt + time
            if time > 0.9999 * storm_dur:
                time = storm_dur
            else:
                dt = storm_dur - time
                flowdirs, max_slopes = flow_router.calc_flowdirs(grid, z)
                drain_area = accumulator.calc_flowacc(grid, z, flowdirs)

        return z
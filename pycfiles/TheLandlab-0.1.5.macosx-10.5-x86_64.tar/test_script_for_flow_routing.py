# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/examples/test_script_for_flow_routing.py
# Compiled at: 2014-09-23 12:37:24
"""
just a little script for testing the d8 flow routing class 
and drainage area calculation 
"""
from landlab import RasterModelGrid
from landlab.examples.flowRoutingD8 import RouteFlowD8
from landlab.examples.drainageArea import CalcDrainageArea
from numpy import *

def main():
    nr = 5
    nc = 6
    ncells = nr * nc
    dx = 1
    rg = RasterModelGrid(nr, nc, dx)
    elevations = zeros(ncells)
    helper = [
     7, 13, 19, 10, 16, 22]
    for i in range(0, 6):
        elevations[helper[i]] = 2

    helper = [
     8, 14, 20, 21, 15, 9]
    for i in range(0, 6):
        elevations[helper[i]] = 3

    print 'elevation vector'
    print elevations
    flow = RouteFlowD8(ncells)
    flow_directions = flow.calc_flowdirs(rg, elevations)
    print 'flow direction vector'
    print flow_directions
    da_calculator = CalcDrainageArea(ncells)
    drain_area = da_calculator.calc_DA(rg, flow_directions)
    print 'drainage area vector'
    print drain_area


if __name__ == '__main__':
    main()
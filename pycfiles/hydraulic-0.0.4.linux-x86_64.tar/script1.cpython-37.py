# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/hydraulic/script1.py
# Compiled at: 2020-01-31 09:10:08
# Size of source mod 2**32: 10740 bytes
"""
Created on Tue Nov 13 17:24:47 2018

@author: jezequel
"""
import thermal as th
from hydraulic.fluids import water
import math, volmdlr as vm
cp_thickness = 0.001
thermal_conductivity = 237
hnodes = [th.Node('h' + str(i)) for i in range(22)]
tnodes = [th.Node('t' + str(i)) for i in range(15)]
b1 = th.TemperatureBound([hnodes[0]], 313, 'b1')
p1 = th.ThermalPipe([hnodes[0], hnodes[1], tnodes[0]], 3e-06, water, 'p1')
j1 = th.Junction([hnodes[1]], [hnodes[2], hnodes[3]], [3e-06], water, 'j1')
p2 = th.ThermalPipe([hnodes[2], hnodes[4], tnodes[1]], 1e-06, water, 'p2')
p3 = th.ThermalPipe([hnodes[4], hnodes[6], tnodes[2]], 2e-06, water, 'p3')
p4 = th.ThermalPipe([hnodes[6], hnodes[8], tnodes[3]], 1e-06, water, 'p4')
p5 = th.ThermalPipe([hnodes[3], hnodes[5], tnodes[4]], 2e-06, water, 'p5')
p6 = th.ThermalPipe([hnodes[5], hnodes[7], tnodes[5]], 1e-06, water, 'p6')
p7 = th.ThermalPipe([hnodes[7], hnodes[9], tnodes[6]], 2e-06, water, 'p7')
j2 = th.Junction([hnodes[8], hnodes[9]], [hnodes[10], hnodes[11], hnodes[12]], [
 1.5e-06, 1.5e-06], water, 'j2')
p8 = th.ThermalPipe([hnodes[10], hnodes[13], tnodes[7]], 1e-06, water, 'p8')
p9 = th.ThermalPipe([hnodes[13], hnodes[15], tnodes[8]], 1e-06, water, 'p9')
p10 = th.ThermalPipe([hnodes[15], hnodes[17], tnodes[9]], 1e-06, water, 'p10')
p11 = th.ThermalPipe([hnodes[11], hnodes[18], tnodes[10]], 1e-06, water, 'p11')
p12 = th.ThermalPipe([hnodes[12], hnodes[14], tnodes[11]], 1e-06, water, 'p12')
p13 = th.ThermalPipe([hnodes[14], hnodes[16], tnodes[12]], 1e-06, water, 'p13')
p14 = th.ThermalPipe([hnodes[16], hnodes[19], tnodes[13]], 1e-06, water, 'p14')
j3 = th.Junction([hnodes[17], hnodes[18], hnodes[19]], [hnodes[20]], [
 1e-06, 1e-06, 1e-06], water, 'j2')
p15 = th.ThermalPipe([hnodes[20], hnodes[21], tnodes[14]], 3e-06, water, 'p15')
b2 = th.HeatFlowOutBound([hnodes[21]], 'b2')
bounds = [
 b1, b2]
pipes = [p1, p2, p3, p4, p5, p6, p7,
 p8, p9, p10, p11, p12, p13, p14,
 p15]
junctions = [j1, j2, j3]
hblocks = [
 *bounds, *pipes, *junctions]
rnodes = []
tblocks = []
for i, pipe in enumerate(pipes):
    tnode = tnodes[i]
    rnode = th.Node('r' + str(i))
    rnodes.append(rnode)
    r = th.Resistor([tnode, rnode], 0.1, 0.01)
    tblocks.append(r)
    if i > 0 and i <= 3:
        hf = th.HeatFlowInBound([rnode], 10)
    else:
        hf = th.HeatFlowInBound([rnode], -10)
    tblocks.append(hf)

nodes = hnodes + tnodes + rnodes
blocks = hblocks + tblocks
thc = th.Circuit(nodes, blocks)
system_matrix = thc.SystemMatrix()
result = thc.Solve()
result.Display()
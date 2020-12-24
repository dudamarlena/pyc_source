# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/monty-carlo/machine/machine.py
# Compiled at: 2011-09-07 20:02:41
"""
Created on Aug 12, 2011

@author: mali
"""
from objectdefs import *
import numpy as num, pylab
from mpl_toolkits.mplot3d import Axes3D
import math, matplotlib.pyplot as plt, profile

def machine(system):
    if type(system) != system:
        print 'The Monte Carlo engine must have the input system of type system.'
        print 'Please prepare your state as an system type object.'
    else:
        print 'Initializing the algorithm...'
        magnetization_beta = []
        for dependency in system.dependencies:
            for dep_name in dependency:
                magnetization_list = num.array([])
                energy_list = num.array([])
                standard_dev = 0
                err = 0
                ctr = 0
                print 'Simulating the system with beta = ' + str(beta)
                while err > 20 or err == 0 or ctr < 20:
                    state, params = monte_carlo_iter(neigh, state, beta, plot=False)
                    magnetization_list = num.append(magnetization_list, params[0])
                    energy_list = num.append(energy_list, params[1])
                    standard_dev = num.std(energy_list[-4:])
                    err = standard_dev / num.mean(energy_list[-4:])
                    print '    [' + str(ctr) + ']Standard Deviation: ' + str(standard_dev)
                    ctr = ctr + 1

                magnetization_beta.append(magnetization_list[(-1)])
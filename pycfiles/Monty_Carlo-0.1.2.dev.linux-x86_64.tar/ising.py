# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/monty-carlo/atomic/ising.py
# Compiled at: 2011-09-07 20:02:41
from objectdefs import *
import matplotlib.pyplot as plt, copy, numpy as num, pylab
from mpl_toolkits.mplot3d import Axes3D
print_en = True

def ising_interaction_func(element, surroundings, self_contrib=1, surr_contrib=1):
    energy = self_contrib * element.spin
    for other_object in surroundings:
        energy = energy + element.spin * other_object.spin * surr_contrib


ising_interaction = ElementalInteraction()
ising_interaction.function = ising_interaction_func()

def ising_energy_def():
    pass
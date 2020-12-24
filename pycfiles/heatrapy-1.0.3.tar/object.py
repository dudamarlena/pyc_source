# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: heatrapy/objects/object.py
# Compiled at: 2018-04-19 10:22:07
from __future__ import unicode_literals
from .. import mats
import os, copy
from .. import solvers

class object:
    """object class

    This class creates thermal objects to be used in more complex systems.
    It includes two methods to apply and remove fields.

    """

    def __init__(self, amb_temperature, materials=('Cu', ), borders=(1, 11), materials_order=(0, ), dx=0.01, dt=0.1, file_name=b'data.txt', boundaries=(0, 0), Q=[], Q0=[], initial_state=False, heat_save=False):
        """Initializes the object.

        amb_temperature: ambient temperature of the whole system
        materials: list of strings of all the used materials present in the
            folder materials
        borders: list of the points where there is a change of material
        materials_order: list of the materials list indexes that defines the
            material properties given by borders
        dx: the space step
        dt: the times step
        file_name: file name where the temperature and heat flux are saved
        boundaries: list of two entries that define the boundary condition
            for temperature. If 0 the boundary condition is insulation
        Q: list of fixed heat source coefficient.
        Q0: list of temperature dependent heat source coefficient.
        initial_state: initial state of the materials. True if applied field
            and False is removed field.
        heat_save: True if saving the heat at the two borders.

        """
        cond01 = isinstance(amb_temperature, float)
        cond01 = cond01 or isinstance(amb_temperature, int)
        cond02 = isinstance(materials, tuple)
        cond03 = isinstance(borders, tuple)
        cond04 = isinstance(materials_order, tuple)
        cond05 = isinstance(dx, int) or isinstance(dx, float)
        cond06 = isinstance(dt, int) or isinstance(dt, float)
        cond07 = isinstance(file_name, unicode)
        cond07 = cond07 or isinstance(file_name, str)
        cond08 = isinstance(boundaries, tuple)
        cond09 = isinstance(Q, list)
        cond10 = isinstance(Q0, list)
        cond11 = isinstance(initial_state, bool)
        cond12 = isinstance(heat_save, bool)
        condition = cond01 and cond02 and cond03 and cond04 and cond05
        condition = condition and cond06 and cond07 and cond08 and cond09
        condition = condition and cond10 and cond11 and cond12
        if not condition:
            raise ValueError
        self.borders = borders
        self.materials = range(len(materials))
        self.boundaries = boundaries
        self.amb_temperature = amb_temperature
        for i in range(len(materials)):
            tadi = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'tadi.txt'
            tadd = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'tadd.txt'
            cpa = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'cpa.txt'
            cp0 = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'cp0.txt'
            k0 = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'k0.txt'
            ka = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'ka.txt'
            rho0 = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'rho0.txt'
            rhoa = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + materials[i] + b'/' + b'rhoa.txt'
            self.materials[i] = mats.calmatpro(tadi, tadd, cpa, cp0, k0, ka, rho0, rhoa)

        self.materials_index = [
         None]
        for i in range(len(borders) - 1):
            for j in range(borders[i], borders[(i + 1)]):
                self.materials_index.append(materials_order[i])

        self.materials_index.append(None)
        self.num_points = borders[(-1)] + 1
        self.file_name = file_name
        self.dx = dx
        self.dt = dt
        self.temperature = [[amb_temperature, amb_temperature]]
        self.Cp = [None]
        self.rho = [None]
        self.Q = [None]
        self.Q0 = [None]
        self.k = [self.materials[self.materials_index[1]].k0(amb_temperature)]
        for i in range(1, borders[(-1)]):
            self.temperature.append([amb_temperature, amb_temperature])
            self.rho.append(self.materials[self.materials_index[i]].rho0(amb_temperature))
            self.Cp.append(self.materials[self.materials_index[i]].cp0(amb_temperature))
            self.k.append(self.materials[self.materials_index[i]].k0(amb_temperature))
            self.Q.append(0.0)
            self.Q0.append(0.0)

        self.temperature.append([amb_temperature, amb_temperature])
        self.rho.append(None)
        self.Cp.append(None)
        self.Q.append(None)
        self.Q0.append(None)
        self.k.append(self.materials[self.materials_index[(-2)]].k0(amb_temperature))
        if Q != []:
            self.Q = Q
        if Q0 != []:
            self.Q0 = Q0
        self.state = [ initial_state for i in range(borders[(-1)] + 1) ]
        self.time_passed = 0.0
        self.Q_ref = copy.copy(self.Q)
        self.Q0_ref = copy.copy(self.Q0)
        line = b'time(s)'
        for i in range(len(self.temperature)):
            line = line + b',T[' + str(i) + b'] (K)'

        if heat_save:
            line = line + b',Q (J/m)'
        line = line + b'\n'
        f = open(self.file_name, b'a')
        f.write(line)
        f.close()
        return

    def activate(self, initial_point, final_point):
        """Activation of the material

        activates a given space interval of the material,
        between the initial_point and final_point.

        """
        for i in range(initial_point, final_point):
            if self.state[i] is False:
                self.temperature[i][0] = self.temperature[i][0] + self.materials[self.materials_index[i]].tadi(self.temperature[i][0])
                self.rho[i] = self.materials[self.materials_index[i]].rhoa(self.temperature[i][0])
                self.Cp[i] = self.materials[self.materials_index[i]].cpa(self.temperature[i][0])
                self.k[i] = self.materials[self.materials_index[i]].ka(self.temperature[i][0])
                self.state[i] = True
            else:
                message = b'point %f already activated' % float(i)
                print message

    def deactivate(self, initial_point, final_point):
        """Deactivation of the material

        deactivates a given space interval of the material,
        between the initial_point and final_point.

        """
        for i in range(initial_point, final_point):
            if self.state[i] is True:
                self.temperature[i][0] = self.temperature[i][0] - self.materials[self.materials_index[i]].tadd(self.temperature[i][0])
                self.rho[i] = self.materials[self.materials_index[i]].rho0(self.temperature[i][0])
                self.Cp[i] = self.materials[self.materials_index[i]].cp0(self.temperature[i][0])
                self.k[i] = self.materials[self.materials_index[i]].k0(self.temperature[i][0])
                self.state[i] = False
            else:
                message = b'point %f already deactivated' % float(i)
                print message
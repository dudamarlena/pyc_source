# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/layer.py
# Compiled at: 2015-11-15 13:26:57
from .units import to_units, cm
from .material import Material
import numpy
__all__ = [
 'Layer', 'GradedLayer', 'CompoundLayer']

class Layer(object):

    def __init__(self, thickness, alloy, doping=None):
        """
        Parameters
        ----------
        thickness : physical quantity
            thickness of the layer
        alloy : openbandparams.IIIVZincBlendeAlloy
            alloy the layer is composed of
        doping : physical quantity (default=None)
            net ionized dopant concentration, e.g. 1e18/cm3.
            Positive for p-type (acceptors), negative for n-type (donors).
        """
        self._thickness = to_units(thickness, cm)
        self._material = Material(alloy=alloy, doping=doping)

    def get_thickness(self):
        """
        Returns the layer thickness (cm).
        """
        return self._thickness

    def get_material(self, x):
        """
        Returns the material at a given position (cm) within the layer.
        
        Parameters
        ----------
        x : float
            position (cm) between zero and the layer thickness
        """
        if x < 0.0 or x > self.get_thickness() * 1.0000000001:
            raise ValueError(('x not within range [{:g}, {:g}]').format(0.0, self.get_thickness()))
        return self._material

    def get_materials(self, N):
        xs = numpy.linspace(0.0, self.get_thickness(), N)
        return [ self.get_material(x) for x in xs ]

    def get_flatband(self, T=300.0):
        """
        returns x, Ev, Ec, Ei
        
        x will be [0, thickness]
        Ev will be [VBO, VBO]
        Ec will be [CBO, CBO]
        Ei will be [VBO+Ei, VBO+Ei]
        
        Arguments
        ---------
        T : float
            the temperature
        """
        x = (
         0.0, self.get_thickness())
        VBO = self._material.VBO(T=T)
        CBO = self._material.CBO(T=T)
        ILO = VBO + self._material.Ei(T=T)
        return (x, (VBO, VBO), (CBO, CBO), (ILO, ILO))


class GradedLayer(Layer):

    def __init__(self, thickness, material_func):
        """
        Parameters
        ----------
        thickness : physical quantity
            thickness of the layer
        material_func : f(x, xmax) -> Material
            callable that accepts the position and thickness and returns
            the Material at that position
        """
        self._thickness = to_units(thickness, cm)
        self._material_func = material_func

    def get_material(self, x):
        """
        Returns the material at a given position (cm) within the layer.
        
        Parameters
        ----------
        x : float
            position (cm) between zero and the layer thickness
        """
        if x < 0.0 or x > self.get_thickness():
            raise ValueError(('x not within range [{:g}, {:g}]').format(0.0, self.get_thickness()))
        return self._material_func(x, self.get_thickness())

    def get_materials(self, N):
        xs = numpy.linspace(0.0, self.get_thickness(), N)
        return [ self.get_material(x) for x in xs ]

    def get_flatband(self, T=300.0, N=50):
        """
        returns x, Ev, Ec, Ei
        
        x will be [0, thickness]
        Ev will be [VBO, VBO]
        Ec will be [CBO, CBO]
        Ei will be [VBO+Ei, VBO+Ei]
        
        Arguments
        ---------
        T : float
            the temperature
        """
        x = numpy.linspace(0.0, self.get_thickness(), N)
        mats = self.get_materials(N)
        VBO = [ mat.VBO(T=T) for mat in mats ]
        CBO = [ mat.CBO(T=T) for mat in mats ]
        ILO = [ mat.VBO(T=T) + mat.Ei(T=T) for mat in mats ]
        return (x, VBO, CBO, ILO)


class CompoundLayer(Layer):

    def __init__(self, layers=None):
        self._layers = []
        if layers is not None:
            for layer in layers:
                self.append(layer)

        return

    def __iter__(self):
        return self._layers.__iter__()

    def append(self, layer):
        """
        Append a layer on the right/bottom.
        """
        if not isinstance(layer, Layer):
            raise TypeError('Layers must be an instance of the `Layer` class.')
        self._layers.append(layer)

    def insert(self, index, layer):
        """
        Insert a layer at the given index.
        """
        if not isinstance(layer, Layer):
            raise TypeError('Layers must be an instance of the `Layer` class.')
        self._layers.insert(index, layer)

    def get_thickness(self):
        """
        Returns the layer thickness (cm).
        """
        sum = 0
        for layer in self:
            sum += layer.get_thickness()

        return sum

    def get_material(self, x):
        """
        Returns the material at a given position (cm) within the layer.
        
        Parameters
        ----------
        x : float
            position (cm) between zero and the layer thickness
        """
        if len(self._layers) < 1:
            raise ValueError('There must be at least one layer.')
        if x < 0.0 or x > self.get_thickness():
            raise ValueError(('x not within range [{:g}, {:g}]').format(0.0, self.get_thickness()))
        last_x = 0
        for layer in self:
            next_x = last_x + layer.get_thickness()
            if x <= next_x:
                return layer.get_material(x - last_x)
            last_x = next_x
        else:
            raise RuntimeError('unexpected execution path')

    def get_flatband(self, T=300.0):
        """
        returns x, Ev, Ec, Ei
        
        x will be [0, ..., thickness]
        Ev will be [VBO, ..., VBO]
        Ec will be [CBO, ..., CBO]
        Ei will be [VBO+Ei, ..., VBO+Ei]
        
        Arguments
        ---------
        T : float
            the temperature
        """
        if len(self._layers) < 1:
            raise ValueError('There must be at least one layer.')
        x, Ev, Ec, Ei = ([], [], [], [])
        last_x = 0
        for layer in self:
            l_x, l_Ev, l_Ec, l_Ei = layer.get_flatband(T=T)
            for layer_x in l_x:
                x.append(last_x + layer_x)

            Ev.extend(l_Ev)
            Ec.extend(l_Ec)
            Ei.extend(l_Ei)
            thickness = l_x[(-1)]
            last_x += thickness

        return (
         x, Ev, Ec, Ei)
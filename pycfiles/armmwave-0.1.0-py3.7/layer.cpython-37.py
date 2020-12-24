# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/armmwave/layer.py
# Compiled at: 2019-11-15 15:45:08
# Size of source mod 2**32: 4775 bytes
"""
This module contains the attributes and methods of the ``BaseLayer``
class, and classes that inherit from it. Each ``BaseLayer`` has
some physical properties that we need to access (and possibly update)
throughout our calculations.
"""
import numpy as np

class BaseLayer:
    __doc__ = "The ``BaseLayer`` class is the parent from which all other classes\n    derive. Its purpose is to establish the bare-minimum attributes\n    needed for a given layer.\n\n    Attributes\n    ----------\n    rind : float\n        The refractive index of the layer. Default is 1.\n    thick : float\n        The thickness of the layer (in meters). Default is 1.\n    tand : float\n        The loss tangent of the layer. Default is 0---i.e., a lossless\n        material.\n    desc : str\n        A descriptive string for the layer. For example, the name of the\n        material. Default is 'Basic layer'.\n    "

    def __init__(self, rind=1.0, thick=1.0, tand=0.0, desc='Basic layer'):
        self.rind = rind
        self.thick = thick
        self.tand = tand
        self.desc = desc

    def __repr__(self):
        return '{} (Basic layer)'.format(self.desc)

    def get_rind(self):
        """Return the layer refractive index."""
        return self.rind

    def get_thick(self):
        """Return the layer thickness."""
        return self.thick

    def get_tand(self):
        """Return the layer loss tangent."""
        return self.tand

    def get_desc(self):
        """Return the layer description."""
        return self.desc


class Layer(BaseLayer):
    __doc__ = "The ``Layer`` class is the primary class for model creation. Inherits\n    from ``BaseLayer``.\n\n    Parameters\n    ----------\n    rind : float, optional\n        The refractive index of the layer. Default is 1.\n    thick : float, optional\n        The thickness of the layer (in meters). Default is 1.\n    tand : float, optional\n        The loss tangent of the layer. Default is 0---i.e., a lossless\n        material.\n    halperna : float, optional\n        The Halpern `a` coefficient, used to caclulate a frequency-dependent\n        loss tangent term. Default is `None`, which corresponds to a constant\n        loss term.\n    halpernb : float, optional\n        The Halpern `b` coefficient, used to caclulate a frequency-dependent\n        loss tangent term. Default is `None`, which corresponds to a constant\n        loss term.\n    desc : str, optional\n        A descriptive string for the layer. For example, the name of the\n        material. Default is 'Basic layer'\n    "

    def __init__(self, halperna=None, halpernb=None, **kwargs):
        (super().__init__)(**kwargs)
        self.halperna = halperna
        self.halpernb = halpernb

    def __repr__(self):
        return '{} (Sim layer)'.format(self.desc)


class Source(BaseLayer):
    __doc__ = 'The ``Source`` is required to be the first layer in the stack. Inherits\n    from ``BaseLayer``.\n\n    The source may have any refractive index or loss tangent, but it is\n    required to have infinite thickness.\n\n    NOTE: While it is possible to set the loss tangent of the layer to a\n    non-zero value, it is not recommended. The case of an absorbing\n    initial medium is not implemented yet.\n    '

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        self.thick = np.inf
        self.previous = _Void()
        self.desc = 'Source layer'

    def __repr__(self):
        return '{} (Source layer)'.format(self.desc)


class Terminator(BaseLayer):
    __doc__ = 'The ``Terminator`` is required to be the last layer in the stack.\n    Inherits from ``BaseLayer``.\n\n    The ``Terminator`` may have any refractive index or loss tangent, but\n    it must have infinite thickness. As a convenience, the Terminator layer\n    may be instantiated with the `vac` flag, where the default is `vac ==\n    True`. `True` sets the refractive index of the ``Terminator`` to 1, and its\n    attenuation to 0. `False` matches refractive index of previous\n    layer, again setting the ``Terminator`` attenuation to zero.\n    '

    def __init__(self, vac=True, **kwargs):
        (super().__init__)(**kwargs)
        self.thick = np.inf
        self.next = _Void()
        self.desc = 'Terminator layer'
        self.vac = vac

    def __repr__(self):
        return '{} (Terminator layer)'.format(self.desc)


class _Void(BaseLayer):
    __doc__ = '     THE VOID     '

    def __init__(self):
        super().__init__()
        self.thick = np.inf
        self.desc = 'THE VOID'

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.thick == other.thick and self.desc == 'THE VOID'
        return False

    def __repr__(self):
        return 'There is nothing but {}'.format(self.desc)
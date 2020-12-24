# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/calculations/data_objects.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 6747 bytes
"""
    The following classes are not meant to be used directly, rather you should
    create the corresponding model instances and retrieve the DataObject from 
    them.
    
    The rationale behind not using the model instances directly is that
    they are difficult to serialize or pickle (memory-)efficiently.
    This is mainly due to all of the boiler-plate code that takes care of
    references, saving, loading, calculating properties from other properties
    etc. A lot of this is not needed for the actual calculation.    
    The data objects below, on the other hand, only contain the data needed to
    be able to calculate XRD patterns.
"""

class DataObject(object):
    __doc__ = '\n    The base class for all DataObject instances.\n    \n    The constructor takes any number of keyword arguments it will set as\n    attributes on the instance.\n    '

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


class AtomTypeData(DataObject):
    __doc__ = ' The DataObject describing an AtomType. '
    par_a = None
    par_b = None
    par_c = None
    debye = None


class AtomData(DataObject):
    __doc__ = ' The DataObject describing an Atom. '
    atom_type = None
    pn = None
    default_z = None
    z = None


class ComponentData(DataObject):
    __doc__ = ' The DataObject describing an Atom '
    layer_atoms = None
    interlayer_atoms = None
    volume = None
    weight = None
    d001 = None
    default_c = None
    delta_c = None
    lattice_d = None


class CSDSData(DataObject):
    __doc__ = ' The DataObject describing the CSDS distribution. '
    average = None
    maximum = None
    minimum = None
    alpha_scale = None
    alpha_offset = None
    beta_scale = None
    beta_offset = None


class GonioData(DataObject):
    __doc__ = ' The DataObject describing the Goniometer setup. '
    min_2theta = None
    max_2theta = None
    steps = None
    has_soller1 = False
    soller1 = None
    has_soller2 = False
    soller2 = None
    divergence_mode = 'FIXED'
    divergence = None
    mcr_2theta = 0
    has_absorption_correction = None
    absorption = 45.0
    sample_surf_density = 20.0
    radius = None
    wavelength = None
    wavelength_distribution = None
    sample_length = None


class ProbabilityData(DataObject):
    __doc__ = ' The DataObject describing the layer stacking probabilities '
    valid = None
    G = None
    W = None
    P = None


class PhaseData(DataObject):
    __doc__ = ' The DataObject describing a phase '
    apply_lpf = True
    apply_correction = True
    components = None
    probability = None
    sigma_star = None
    csds = None


class SpecimenData(DataObject):
    __doc__ = ' The DataObject describing a specimen '
    goniometer = None
    absorption = None
    phases = None
    observed_intensity = None
    total_intensity = None
    phase_intensities = None
    correction = None


class MixtureData(DataObject):
    __doc__ = ' The DataObject describing a mixture '
    specimens = None
    fractions = None
    bgshifts = None
    scales = None
    parsed = False
    calculated = False
    optimized = False
    n = 0
    m = 0
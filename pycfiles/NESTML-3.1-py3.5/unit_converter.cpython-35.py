# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/unit_converter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2921 bytes
from astropy import units

class UnitConverter(object):
    __doc__ = '\n    Calculates the factor needed to convert a given unit to its\n    NEST counterpart. I.e.: potentials are expressed as mV, consultancies as nS etc.\n    '

    @classmethod
    def get_factor(cls, unit):
        """
        Gives a factor for a given unit that transforms it to a "neuroscience" scale
        If the given unit is not listed as a neuroscience unit, the factor is 1
        :param unit: an astropy unit
        :type unit: IrreducibleUnit or Unit or CompositeUnit
        :return: a factor to that unit, converting it to "neuroscience" scales.
        :rtype float
        """
        if not (isinstance(unit, units.IrreducibleUnit) or isinstance(unit, units.CompositeUnit)):
            if not isinstance(unit, units.Unit):
                assert isinstance(unit, units.PrefixUnit), 'UnitConverter: given parameter is not a unit (%s)!' % type(unit)
                if unit.physical_type == 'dimensionless':
                    return unit.si
                target_unit = None
                if unit.physical_type == 'electrical conductance':
                    target_unit = units.nS
                if unit.physical_type == 'electrical resistance':
                    target_unit = units.Gohm
                if unit.physical_type == 'time':
                    target_unit = units.ms
                if unit.physical_type == 'electrical capacitance':
                    target_unit = units.pF
                if unit.physical_type == 'electrical potential':
                    target_unit = units.mV
                if unit.physical_type == 'electrical current':
                    target_unit = units.pA
                if target_unit is not None:
                    return (unit / target_unit).si.scale
                if unit == unit.bases[0] and len(unit.bases) == 1:
                    return 1.0
                factor = 1.0
                for i in range(0, len(unit.bases)):
                    factor *= cls.get_factor(unit.bases[i]) ** unit.powers[i]

                return factor
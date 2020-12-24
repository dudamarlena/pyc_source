# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/iii_v_zinc_blende_binary.py
# Compiled at: 2015-04-09 03:26:05
__all__ = [
 'IIIVZincBlendeBinary']
from .iii_v_zinc_blende_alloy import IIIVZincBlendeAlloy

class IIIVZincBlendeBinary(IIIVZincBlendeAlloy):
    """
    The base class for all III-V zinc blende binary alloys.
    """

    def __repr__(self):
        return self.name

    def latex(self):
        return self.name

    def element_fraction(self, element):
        """
        Returns the fractional concentration of `element` with respect
        to its sublattice. In a III-V binary, the fraction is either 1 if
        `element` is present, or 0 if it is not.
        """
        if element in self.elements:
            return 1.0
        else:
            return 0.0
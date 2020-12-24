# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parterre/testing.py
# Compiled at: 2009-08-29 17:38:56
"""Parterre variant test cases
    Copyright (C) 2008  Eric Wald
    
    This module runs tests for each variant in the module.
    
    This package may be reused for non-commercial purposes without charge,
    and without notifying the authors.  Use of any part of this package for
    commercial purposes without permission from the authors is prohibited.
"""
import unittest
from parlance.functions import fails
from parlance.test.gameboard import StandardVariantTests

class AbstractionVariantTests(StandardVariantTests):
    """Tests for the abstraction2 map variant"""
    variant = 'abstraction2'


class AfricanVariantTests(StandardVariantTests):
    """Tests for the african2 map variant"""
    variant = 'african2'


class AmericasVariantTests(StandardVariantTests):
    """Tests for the americas4 map variant"""
    variant = 'americas4'


class ChromaticVariantTests(StandardVariantTests):
    """Tests for the chromatic map variant"""
    variant = 'chromatic'


class ClassicalVariantTests(StandardVariantTests):
    """Tests for the classical map variant"""
    variant = 'classical'


class FleetRomeVariantTests(StandardVariantTests):
    """Tests for the fleet_rome map variant"""
    variant = 'fleet_rome'


class Hundred3VariantTests(StandardVariantTests):
    """Tests for the hundred3 map variant"""
    variant = 'hundred3'


class Hundred31VariantTests(StandardVariantTests):
    """Tests for the hundred31 map variant"""
    variant = 'hundred31'


class Hundred32VariantTests(StandardVariantTests):
    """Tests for the hundred32 map variant"""
    variant = 'hundred32'


class IberianVariantTests(StandardVariantTests):
    """Tests for the iberian2 map variant"""
    variant = 'iberian2'

    @fails
    def test_gascony_encoding(self):
        key = 'GAS'
        name = self.var().provinces[key]
        self.failUnlessEqual(type(name), unicode)
        self.failUnlessEqual(name, 'Gascuña')


class ModernVariantTests(StandardVariantTests):
    """Tests for the modern map variant"""
    variant = 'modern'


class SailHoVariantTests(StandardVariantTests):
    """Tests for the sailho map variant"""
    variant = 'sailho'


class ShiftAroundVariantTests(StandardVariantTests):
    """Tests for the shift_around map variant"""
    variant = 'shift_around'


class SouthAmerica32VariantTests(StandardVariantTests):
    """Tests for the south_america32 map variant"""
    variant = 'south_america32'


class SouthAmerica51VariantTests(StandardVariantTests):
    """Tests for the south_america51 map variant"""
    variant = 'south_america51'


class SouthEastAsiaVariantTests(StandardVariantTests):
    """Tests for the south_east_asia3 map variant"""
    variant = 'south_east_asia3'


class VersaillesVariantTests(StandardVariantTests):
    """Tests for the versailles3 map variant"""
    variant = 'versailles3'


class WorldVariantTests(StandardVariantTests):
    """Tests for the world3 map variant"""
    variant = 'world3'


if __name__ == '__main__':
    unittest.main()
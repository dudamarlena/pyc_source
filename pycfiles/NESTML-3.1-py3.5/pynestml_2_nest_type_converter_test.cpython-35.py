# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/pynestml_2_nest_type_converter_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2896 bytes
import unittest
from astropy import units
from pynestml.codegeneration.pynestml_2_nest_type_converter import PyNestml2NestTypeConverter
from pynestml.symbols.boolean_type_symbol import BooleanTypeSymbol
from pynestml.symbols.integer_type_symbol import IntegerTypeSymbol
from pynestml.symbols.nest_time_type_symbol import NESTTimeTypeSymbol
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.real_type_symbol import RealTypeSymbol
from pynestml.symbols.string_type_symbol import StringTypeSymbol
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.symbols.void_type_symbol import VoidTypeSymbol
from pynestml.utils.unit_type import UnitType
PredefinedUnits.register_units()
PredefinedTypes.register_types()
convert = PyNestml2NestTypeConverter.convert

class PyNestMl2NESTTypeConverterTest(unittest.TestCase):

    def test_boolean_type(self):
        bts = BooleanTypeSymbol()
        result = convert(bts)
        self.assertEqual(result, 'bool')

    def test_real_type(self):
        rts = RealTypeSymbol()
        result = convert(rts)
        self.assertEqual(result, 'double')

    def test_void_type(self):
        vts = VoidTypeSymbol()
        result = convert(vts)
        self.assertEqual(result, 'void')

    def test_string_type(self):
        sts = StringTypeSymbol()
        result = convert(sts)
        self.assertEqual(result, 'std::string')

    def test_integer_type(self):
        its = IntegerTypeSymbol()
        result = convert(its)
        self.assertEqual(result, 'long')

    def test_unit_type(self):
        ms_unit = UnitType(name=str(units.ms), unit=units.ms)
        uts = UnitTypeSymbol(unit=ms_unit)
        result = convert(uts)
        self.assertEqual(result, 'double')

    def test_buffer_type(self):
        bts = IntegerTypeSymbol()
        bts.is_buffer = True
        result = convert(bts)
        self.assertEqual(result, 'nest::RingBuffer')

    def test_time_type(self):
        tts = NESTTimeTypeSymbol()
        result = convert(tts)
        self.assertEqual(result, 'nest::Time')
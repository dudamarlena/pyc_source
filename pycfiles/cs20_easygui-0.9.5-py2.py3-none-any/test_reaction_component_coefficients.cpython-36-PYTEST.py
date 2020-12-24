# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/test/test_reaction_component_coefficients.py
# Compiled at: 2017-12-08 16:34:46
# Size of source mod 2**32: 1151 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from kinetics import chemkin

class test_reaction_component_coefficients(unittest.TestCase):

    def test_reaction_coeff_params_T_text(self):
        try:
            parsed = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
            reactions = chemkin.Reaction(parsed, 'panama')
        except Exception as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_reaction_coeff_params_T_negative(self):
        try:
            parsed = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
            reactions = chemkin.Reaction(parsed, -100)
        except Exception as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_reaction_coeff_params_T_flow(self):
        try:
            parsed = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
            reactions = chemkin.Reaction(parsed, float('inf'))
        except Exception as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None
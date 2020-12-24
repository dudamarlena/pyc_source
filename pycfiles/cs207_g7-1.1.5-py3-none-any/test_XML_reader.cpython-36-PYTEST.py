# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/test/test_XML_reader.py
# Compiled at: 2017-12-08 16:35:16
# Size of source mod 2**32: 3884 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from kinetics import chemkin
import numpy as np

class test_XML_Readers(unittest.TestCase):

    def test_XML_reader_1(self):
        r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_good1.xml')
        expected = ['H', 'O', 'OH', 'H2', 'O2']
        @py_assert1 = r_reader.get_species
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 == expected
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.get_species\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(r_reader) if 'r_reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r_reader) else 'r_reader',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format9 = (@pytest_ar._format_assertmsg('ReactionParser getting incorrect species.') + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    def test_XML_bad_reactants(self):
        r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_bad_reactants.xml')
        try:
            reactions = r_reader.parse_reactions()
        except Exception as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = (@pytest_ar._format_assertmsg('Bad reactants should raise a TypeError.') + '\n>assert %(py7)s') % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_XML_bad_products(self):
        r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_bad_products.xml')
        try:
            reactions = r_reader.parse_reactions()
        except Exception as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = (@pytest_ar._format_assertmsg('Bad products should raise a TypeError.') + '\n>assert %(py7)s') % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_XML_reader_2_V1(self):
        r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_good2.xml')
        reactions = r_reader.parse_reactions()
        chem = chemkin.Reaction(r_reader, 750)
        V1, V2 = chem.reaction_components()
        print(repr(chem))
        print(V1)
        @py_assert3 = [[1], [0], [0], [2], [1]]
        @py_assert2 = V1 == @py_assert3
        @py_assert7 = all(@py_assert2)
        if not @py_assert7:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (V1, @py_assert3)) % {'py1':@pytest_ar._saferepr(V1) if 'V1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(V1) else 'V1',  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format9 = (@pytest_ar._format_assertmsg('XML Reader loading incorrect v1 in file xml_good2.xml') + '\n>assert %(py8)s\n{%(py8)s = %(py0)s(%(py6)s)\n}') % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py6':@py_format5,  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert3 = @py_assert7 = None

    def test_XML_reader_2_V2(self):
        r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_good2.xml')
        reactions = r_reader.parse_reactions()
        chem = chemkin.Reaction(r_reader, 750)
        V1, V2 = chem.reaction_components()
        @py_assert3 = [[0], [1], [1], [0], [0]]
        @py_assert2 = V2 == @py_assert3
        @py_assert7 = all(@py_assert2)
        if not @py_assert7:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (V2, @py_assert3)) % {'py1':@pytest_ar._saferepr(V2) if 'V2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(V2) else 'V2',  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format9 = (@pytest_ar._format_assertmsg('XML Reader loading incorrect v1 in file xml_good2.xml') + '\n>assert %(py8)s\n{%(py8)s = %(py0)s(%(py6)s)\n}') % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py6':@py_format5,  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert3 = @py_assert7 = None

    def test_XML_homework(self):
        r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
        reactions = r_reader.parse_reactions()
        T = 750
        chem = chemkin.Reaction(r_reader, T)
        X = [2, 1, 0.5, 1, 1]
        V1, V2 = chem.reaction_components()
        k = chem.reaction_coeff_params()
        rrs = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
        ans = np.array([-3607077.87280406, -5613545.18362079, 9220623.05642485, 2006467.31081673, -2006467.31081673])
        diffs = np.array([rrs - ans])
        @py_assert2 = 1e-07
        @py_assert1 = diffs < @py_assert2
        @py_assert6 = @py_assert1.all
        @py_assert8 = @py_assert6()
        if not @py_assert8:
            @py_format4 = @pytest_ar._call_reprcompare(('<', ), (@py_assert1,), ('%(py0)s < %(py3)s', ), (diffs, @py_assert2)) % {'py0':@pytest_ar._saferepr(diffs) if 'diffs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(diffs) else 'diffs',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.all\n}()\n}') % {'py5':@py_format4,  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert2 = @py_assert6 = @py_assert8 = None

    def test_XML_reversible(self):
        r_reader = chemkin.ReactionParser('kinetics/test/xml/rxns_reversible.xml')
        reactions = r_reader.parse_reactions()
        chem = chemkin.Reaction(r_reader, 1500)
        X = [2, 1, 0.5, 1, 1, 1.0, 0.5, 1.5]
        V1, V2 = chem.reaction_components()
        k = chem.reaction_coeff_params()
        rrs = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
        ans = np.array([89270713727987.25, -320691804865713.7, -112277955225117.38, 86184567576824.7, 82059197481207.2, 336486898686318.2, -8582946144078.839, -152448671237427.4])
        diffs = np.array([rrs - ans])
        @py_assert2 = 1e-07
        @py_assert1 = diffs < @py_assert2
        @py_assert6 = @py_assert1.all
        @py_assert8 = @py_assert6()
        if not @py_assert8:
            @py_format4 = @pytest_ar._call_reprcompare(('<', ), (@py_assert1,), ('%(py0)s < %(py3)s', ), (diffs, @py_assert2)) % {'py0':@pytest_ar._saferepr(diffs) if 'diffs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(diffs) else 'diffs',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.all\n}()\n}') % {'py5':@py_format4,  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert2 = @py_assert6 = @py_assert8 = None
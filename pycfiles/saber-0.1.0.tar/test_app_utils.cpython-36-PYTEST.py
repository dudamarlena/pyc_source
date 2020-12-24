# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_app_utils.py
# Compiled at: 2018-11-30 14:46:37
# Size of source mod 2**32: 1623 bytes
"""Any and all unit tests for the app_utils (saber/utils/app_utils.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from ..utils import app_utils
from .resources.dummy_constants import *

def test_get_pubmed_xml_errors():
    """Asserts that call to `app_utils.get_pubmed_xml()` raises a ValueError error when an invalid
    value for argument `pmid` is passed."""
    invalid_pmids = [
     [
      'test'], 'test', 0.0, 0, -1, (42, )]
    for pmid in invalid_pmids:
        with pytest.raises(ValueError):
            app_utils.get_pubmed_xml(pmid)


def test_harmonize_entities():
    """Asserts that app_utils.harmonize_entities() returns the expected results."""
    one_on_test = {'PRGE': True}
    one_on_expected = {'ANAT':False,  'CHED':False,  'DISO':False,  'LIVB':False, 
     'PRGE':True,  'TRIG':False}
    multi_on_test = {'PRGE':True, 
     'CHED':True,  'TRIG':False}
    multi_on_expected = {'ANAT':False,  'CHED':True,  'DISO':False,  'LIVB':False, 
     'PRGE':True,  'TRIG':False}
    none_on_test = {}
    none_on_expected = {'ANAT':False, 
     'CHED':False,  'DISO':False,  'LIVB':False, 
     'PRGE':False,  'TRIG':False}
    @py_assert3 = app_utils.harmonize_entities
    @py_assert7 = @py_assert3(DUMMY_ENTITIES, one_on_test)
    @py_assert1 = one_on_expected == @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.harmonize_entities\n}(%(py5)s, %(py6)s)\n}', ), (one_on_expected, @py_assert7)) % {'py0':@pytest_ar._saferepr(one_on_expected) if 'one_on_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_on_expected) else 'one_on_expected',  'py2':@pytest_ar._saferepr(app_utils) if 'app_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app_utils) else 'app_utils',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_ENTITIES) if 'DUMMY_ENTITIES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_ENTITIES) else 'DUMMY_ENTITIES',  'py6':@pytest_ar._saferepr(one_on_test) if 'one_on_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_on_test) else 'one_on_test',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert7 = None
    @py_assert3 = app_utils.harmonize_entities
    @py_assert7 = @py_assert3(DUMMY_ENTITIES, multi_on_test)
    @py_assert1 = multi_on_expected == @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.harmonize_entities\n}(%(py5)s, %(py6)s)\n}', ), (multi_on_expected, @py_assert7)) % {'py0':@pytest_ar._saferepr(multi_on_expected) if 'multi_on_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(multi_on_expected) else 'multi_on_expected',  'py2':@pytest_ar._saferepr(app_utils) if 'app_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app_utils) else 'app_utils',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_ENTITIES) if 'DUMMY_ENTITIES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_ENTITIES) else 'DUMMY_ENTITIES',  'py6':@pytest_ar._saferepr(multi_on_test) if 'multi_on_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(multi_on_test) else 'multi_on_test',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert7 = None
    @py_assert3 = app_utils.harmonize_entities
    @py_assert7 = @py_assert3(DUMMY_ENTITIES, none_on_test)
    @py_assert1 = none_on_expected == @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.harmonize_entities\n}(%(py5)s, %(py6)s)\n}', ), (none_on_expected, @py_assert7)) % {'py0':@pytest_ar._saferepr(none_on_expected) if 'none_on_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none_on_expected) else 'none_on_expected',  'py2':@pytest_ar._saferepr(app_utils) if 'app_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app_utils) else 'app_utils',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_ENTITIES) if 'DUMMY_ENTITIES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_ENTITIES) else 'DUMMY_ENTITIES',  'py6':@pytest_ar._saferepr(none_on_test) if 'none_on_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none_on_test) else 'none_on_test',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert7 = None
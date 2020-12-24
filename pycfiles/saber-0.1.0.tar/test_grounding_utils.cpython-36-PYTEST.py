# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_grounding_utils.py
# Compiled at: 2018-12-06 09:58:56
# Size of source mod 2**32: 1481 bytes
"""Any and all unit tests for the grounding_utils (saber/utils/grounding_utils.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from ..utils import grounding_utils

@pytest.fixture
def annotation():
    """Returns a dictionary object similar to one that might be returned by `Saber.annotate()`
    """
    annotation = {'ents':[
      {'text':'Hdm2', 
       'label':'PRGE',  'start':23,  'end':27},
      {'text':'MK2', 
       'label':'PRGE',  'start':31,  'end':34},
      {'text':'p53', 
       'label':'PRGE',  'start':66,  'end':69}], 
     'text':'The phosphorylation of Hdm2 by MK2 promotes the ubiquitination of p53.', 
     'title':''}
    return annotation


def test_query_uniprot(annotation):
    """
    """
    text = annotation['ents'][1]['text']
    actual = grounding_utils._query_uniprot(text, 9606, limit=1)
    @py_assert2 = len(actual)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = actual[0]['Entry']
    @py_assert3 = 'P49137'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = actual[0]
    @py_assert3 = @py_assert1.keys
    @py_assert5 = @py_assert3()
    @py_assert7 = len(@py_assert5)
    @py_assert10 = 3
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.keys\n}()\n})\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    actual = grounding_utils._query_uniprot('p')
    @py_assert2 = []
    @py_assert1 = actual == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (actual, @py_assert2)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_ground(annotation):
    """
    """
    actual = grounding_utils.ground(annotation, ('human', 'mouse'), limit=2)
    @py_assert2 = None
    @py_assert1 = actual is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (actual, @py_assert2)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    for ent in actual['ents']:
        @py_assert0 = 'xrefs'
        @py_assert4 = ent.keys
        @py_assert6 = @py_assert4()
        @py_assert2 = @py_assert0 in @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.keys\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(ent) if 'ent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ent) else 'ent',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_query_hgnc(annotation):
    """
    """
    actual = grounding_utils._query_hgnc(annotation)
    @py_assert2 = None
    @py_assert1 = actual is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (actual, @py_assert2)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
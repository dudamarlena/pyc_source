# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ddanier/work/django/django_hits/tests/test_basics.py
# Compiled at: 2015-09-10 02:54:10
# Size of source mod 2**32: 372 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from django_hits.models import Hit
from django.contrib.auth.models import AnonymousUser

@pytest.mark.django_db
def test_simple_hit():
    hit = Hit.objects.hit('something', None, '127.0.0.1')
    @py_assert1 = hit.views
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.views\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(hit) if 'hit' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hit) else 'hit',  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = hit.visits
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.visits\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(hit) if 'hit' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hit) else 'hit',  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    hit = Hit.objects.hit('something', None, '127.0.0.1')
    @py_assert1 = hit.views
    @py_assert4 = 2
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.views\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(hit) if 'hit' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hit) else 'hit',  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = hit.visits
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.visits\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(hit) if 'hit' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hit) else 'hit',  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/event_listener/test_static.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 377 bytes
"""Tests for the static event listener subclass."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import timedelta
from astrality.event_listener import Static

def test_static_events():
    static = Static({})
    @py_assert0 = 'static'
    @py_assert4 = static.events
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.events\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(static) if 'static' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(static) else 'static',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_static_event_listener_until_next_event():
    default_static = Static({})
    @py_assert1 = default_static.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert7 = 36500
    @py_assert9 = timedelta(days=@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n} == %(py10)s\n{%(py10)s = %(py6)s(days=%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(default_static) if 'default_static' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_static) else 'default_static',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(timedelta) if 'timedelta' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timedelta) else 'timedelta',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/event_listener/test_time_of_day.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2499 bytes
"""Tests for the time_of_day event listener."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import datetime
import pytest
from astrality.event_listener import TimeOfDay

@pytest.fixture
def default_time_of_day_event_listener():
    """Return a default time_of_day event listener object."""
    return TimeOfDay({'type': 'time_of_day'})


def test_processing_of_time_of_day_config(default_time_of_day_event_listener):
    """Test that the processing of the time_of_day config is correct."""
    @py_assert0 = 'sunday'
    @py_assert4 = default_time_of_day_event_listener.workdays
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.workdays\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'monday'
    @py_assert4 = default_time_of_day_event_listener.workdays
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.workdays\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = default_time_of_day_event_listener.workdays['monday']
    @py_assert2 = @py_assert0.start
    @py_assert4 = @py_assert2.tm_hour
    @py_assert7 = 9
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.start\n}.tm_hour\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = default_time_of_day_event_listener.workdays['monday']
    @py_assert2 = @py_assert0.start
    @py_assert4 = @py_assert2.tm_min
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.start\n}.tm_min\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = default_time_of_day_event_listener.workdays['friday']
    @py_assert2 = @py_assert0.end
    @py_assert4 = @py_assert2.tm_hour
    @py_assert7 = 17
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.end\n}.tm_hour\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = default_time_of_day_event_listener.workdays['friday']
    @py_assert2 = @py_assert0.end
    @py_assert4 = @py_assert2.tm_min
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.end\n}.tm_min\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_current_event_of_time_of_day_event_listener(default_time_of_day_event_listener, freezer):
    """Test that the correct events are returned."""
    work_monday = datetime(year=2018, month=2, day=12, hour=10)
    freezer.move_to(work_monday)
    @py_assert1 = default_time_of_day_event_listener.event
    @py_assert3 = @py_assert1()
    @py_assert6 = 'on'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    monday_freetime = datetime(year=2018, month=2, day=12, hour=18)
    freezer.move_to(monday_freetime)
    @py_assert1 = default_time_of_day_event_listener.event
    @py_assert3 = @py_assert1()
    @py_assert6 = 'off'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    saturday = datetime(year=2018, month=2, day=17, hour=10)
    freezer.move_to(saturday)
    @py_assert1 = default_time_of_day_event_listener.event
    @py_assert3 = @py_assert1()
    @py_assert6 = 'off'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_time_until_next_event_for_time_of_day_event_listener(default_time_of_day_event_listener, freezer):
    """Test that the correct number of seconds until next period is correct."""
    work_monday = datetime(year=2018, month=2, day=12, hour=10)
    freezer.move_to(work_monday)
    @py_assert1 = default_time_of_day_event_listener.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 7
    @py_assert12 = 60
    @py_assert14 = @py_assert10 * @py_assert12
    @py_assert15 = 60
    @py_assert17 = @py_assert14 * @py_assert15
    @py_assert18 = 60
    @py_assert20 = @py_assert17 + @py_assert18
    @py_assert9 = @py_assert7 == @py_assert20
    if not @py_assert9:
        @py_format21 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == (((%(py11)s * %(py13)s) * %(py16)s) + %(py19)s)', ), (@py_assert7, @py_assert20)) % {'py0':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format23 = 'assert %(py22)s' % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert18 = @py_assert20 = None
    monday_freetime = datetime(year=2018, month=2, day=12, hour=18)
    freezer.move_to(monday_freetime)
    @py_assert1 = default_time_of_day_event_listener.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 15
    @py_assert12 = 60
    @py_assert14 = @py_assert10 * @py_assert12
    @py_assert15 = 60
    @py_assert17 = @py_assert14 * @py_assert15
    @py_assert18 = 60
    @py_assert20 = @py_assert17 + @py_assert18
    @py_assert9 = @py_assert7 == @py_assert20
    if not @py_assert9:
        @py_format21 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == (((%(py11)s * %(py13)s) * %(py16)s) + %(py19)s)', ), (@py_assert7, @py_assert20)) % {'py0':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format23 = 'assert %(py22)s' % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert18 = @py_assert20 = None
    saturday = datetime(year=2018, month=2, day=17, hour=10)
    freezer.move_to(saturday)
    @py_assert1 = default_time_of_day_event_listener.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 47
    @py_assert12 = 60
    @py_assert14 = @py_assert10 * @py_assert12
    @py_assert15 = 60
    @py_assert17 = @py_assert14 * @py_assert15
    @py_assert18 = 60
    @py_assert20 = @py_assert17 + @py_assert18
    @py_assert9 = @py_assert7 == @py_assert20
    if not @py_assert9:
        @py_format21 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == (((%(py11)s * %(py13)s) * %(py16)s) + %(py19)s)', ), (@py_assert7, @py_assert20)) % {'py0':@pytest_ar._saferepr(default_time_of_day_event_listener) if 'default_time_of_day_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_time_of_day_event_listener) else 'default_time_of_day_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format23 = 'assert %(py22)s' % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert18 = @py_assert20 = None
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/event_listener/test_daylight.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2916 bytes
"""Tests for the daylight event listener subclass."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import datetime, timedelta
import pytest
from astrality.event_listener import Daylight

@pytest.fixture
def daylight_config():
    """A daylight event listener configuration in Trondheim, Norway."""
    return {'type':'daylight', 
     'latitude':0, 
     'longitude':0, 
     'elevation':0}


@pytest.fixture
def daylight(daylight_config):
    """A daylight event listener in Trondheim, Norway."""
    return Daylight(daylight_config)


@pytest.fixture
def dawn(daylight):
    return daylight.construct_astral_location().sun()['dawn']


@pytest.fixture
def before_dawn(dawn):
    delta = timedelta(minutes=(-2))
    return dawn + delta


@pytest.fixture
def after_dawn(dawn):
    delta = timedelta(minutes=2)
    return dawn + delta


def test_that_night_is_correctly_identified(daylight, before_dawn, freezer):
    freezer.move_to(before_dawn)
    event = daylight.event()
    @py_assert2 = 'night'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_that_day_is_correctly_identified(daylight, after_dawn, freezer):
    freezer.move_to(after_dawn)
    event = daylight.event()
    @py_assert2 = 'day'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@pytest.fixture
def dusk(daylight):
    return daylight.construct_astral_location().sun()['dusk']


@pytest.fixture
def before_dusk(dusk):
    delta = timedelta(minutes=(-2))
    return dusk + delta


@pytest.fixture
def after_dusk(dusk):
    delta = timedelta(minutes=2)
    return dusk + delta


def test_that_night_is_correctly_identified_after_dusk(daylight, after_dusk, freezer):
    freezer.move_to(after_dusk)
    event = daylight.event()
    @py_assert2 = 'night'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_that_day_is_correctly_identified_before_dusk(daylight, before_dusk, freezer):
    freezer.move_to(before_dusk)
    event = daylight.event()
    @py_assert2 = 'day'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_time_left_before_new_event(daylight, before_dusk, freezer):
    freezer.move_to(before_dusk)
    @py_assert1 = daylight.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 120
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(daylight) if 'daylight' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(daylight) else 'daylight',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_time_right_before_midnight(daylight, freezer):
    """
    This function requires special handling when the UTC time is later than all
    daylight events within the same day, which is the case right before
    midnight.
    """
    before_midnight = datetime(year=2019,
      month=12,
      day=23,
      hour=23,
      second=59,
      microsecond=0)
    freezer.move_to(before_midnight)
    time_left = daylight.time_until_next_event()
    @py_assert0 = 0
    @py_assert5 = time_left.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert2 = @py_assert0 < @py_assert7
    @py_assert9 = 60
    @py_assert11 = 60
    @py_assert13 = @py_assert9 * @py_assert11
    @py_assert14 = 24
    @py_assert16 = @py_assert13 * @py_assert14
    @py_assert3 = @py_assert7 < @py_assert16
    if not (@py_assert2 and @py_assert3):
        @py_format17 = @pytest_ar._call_reprcompare(('<', '<'), (@py_assert2, @py_assert3), ('%(py1)s < %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.total_seconds\n}()\n}',
                                                                                             '%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.total_seconds\n}()\n} < ((%(py10)s * %(py12)s) * %(py15)s)'), (@py_assert0, @py_assert7, @py_assert16)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(time_left) if 'time_left' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time_left) else 'time_left',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert16 = None


def test_time_until_night_when_other_periods_are_inbetween(daylight, before_dusk, freezer):
    freezer.move_to(before_dusk - timedelta(hours=6))
    @py_assert1 = daylight.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 120
    @py_assert12 = 6
    @py_assert14 = 60
    @py_assert16 = @py_assert12 * @py_assert14
    @py_assert17 = 60
    @py_assert19 = @py_assert16 * @py_assert17
    @py_assert20 = @py_assert10 + @py_assert19
    @py_assert9 = @py_assert7 == @py_assert20
    if not @py_assert9:
        @py_format21 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == (%(py11)s + ((%(py13)s * %(py15)s) * %(py18)s))', ), (@py_assert7, @py_assert20)) % {'py0':@pytest_ar._saferepr(daylight) if 'daylight' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(daylight) else 'daylight',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format23 = 'assert %(py22)s' % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert19 = @py_assert20 = None
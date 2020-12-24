# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/event_listener/test_solar.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 4108 bytes
"""Tests for the solar event listener subclass."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
import pytest
from astrality.event_listener import Solar

@pytest.fixture
def solar_config():
    """A solar event listener configuration in Trondheim, Norway."""
    return {'type':'solar', 
     'latitude':0, 
     'longitude':0, 
     'elevation':0}


@pytest.fixture
def solar(solar_config):
    """A solar event listener in Trondheim, Norway."""
    return Solar(solar_config)


@pytest.fixture
def dawn(solar):
    return solar.construct_astral_location().sun()['dawn']


@pytest.fixture
def before_dawn(dawn):
    delta = timedelta(minutes=(-2))
    return dawn + delta


@pytest.fixture
def after_dawn(dawn):
    delta = timedelta(minutes=2)
    return dawn + delta


def test_that_night_is_correctly_identified(solar, before_dawn, freezer):
    freezer.move_to(before_dawn)
    event = solar.event()
    @py_assert2 = 'night'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_that_sunrise_is_correctly_identified(solar, after_dawn, freezer):
    freezer.move_to(after_dawn)
    event = solar.event()
    @py_assert2 = 'sunrise'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@pytest.fixture
def dusk(solar):
    return solar.construct_astral_location().sun()['dusk']


@pytest.fixture
def before_dusk(dusk):
    delta = timedelta(minutes=(-2))
    return dusk + delta


@pytest.fixture
def after_dusk(dusk):
    delta = timedelta(minutes=2)
    return dusk + delta


def test_that_night_is_correctly_identified_after_dusk(solar, after_dusk, freezer):
    freezer.move_to(after_dusk)
    event = solar.event()
    @py_assert2 = 'night'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_that_sunset_is_correctly_identified_before_dusk(solar, before_dusk, freezer):
    freezer.move_to(before_dusk)
    event = solar.event()
    @py_assert2 = 'sunset'
    @py_assert1 = event == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (event, @py_assert2)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_location(solar):
    location = solar.construct_astral_location()
    @py_assert2 = str(location)
    @py_assert5 = 'CityNotImportant/RegionIsNotImportantEither, tz=UTC, lat=0.00, lon=0.00'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(location) if 'location' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(location) else 'location',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_time_left_before_new_event(solar, before_dusk, freezer):
    freezer.move_to(before_dusk)
    @py_assert1 = solar.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 120
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(solar) if 'solar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(solar) else 'solar',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_time_right_before_midnight(solar, freezer):
    """
    This function requires special handling when the UTC time is later than all
    solar events within the same day, which is the case right before midnight.
    """
    before_midnight = datetime(year=2019,
      month=12,
      day=23,
      hour=23,
      second=59,
      microsecond=0)
    freezer.move_to(before_midnight)
    time_left = solar.time_until_next_event()
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


def test_config_event_listener_method():
    solar_event_listener_application_config = {'type': 'solar'}
    solar_event_listener = Solar(solar_event_listener_application_config)
    @py_assert0 = solar_event_listener.event_listener_config['latitude']
    @py_assert3 = 0
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.mark.parametrize('hour,sun', [
 (23, 'night'),
 (1, 'night'),
 (5, 'sunrise'),
 (10, 'morning'),
 (13, 'afternoon'),
 (22, 'sunset')])
def test_locations_where_some_events_never_occur(freezer, hour, sun):
    """
    Test that locations with missing solar events are handled gracefully.

    During summer, closer to the poles, the sun never dips properly below
    the horizon. In this case astral throws an AstralError, and we have
    to fall back to some hard coded defaults instead.
    """
    summer = datetime(year=2018,
      month=5,
      day=24,
      hour=hour,
      minute=0,
      tzinfo=(tzlocal()))
    freezer.move_to(summer)
    polar_location = {'type':'solar', 
     'latitude':89, 
     'longitude':89, 
     'elevation':0}
    polar_sun = Solar(polar_location)
    @py_assert1 = polar_sun.event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == sun
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py6)s', ), (@py_assert3, sun)) % {'py0':@pytest_ar._saferepr(polar_sun) if 'polar_sun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(polar_sun) else 'polar_sun',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(sun) if 'sun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sun) else 'sun'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = 0
    @py_assert5 = polar_sun.time_until_next_event
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert7.total_seconds
    @py_assert11 = @py_assert9()
    @py_assert2 = @py_assert0 < @py_assert11
    @py_assert13 = 24
    @py_assert15 = 60
    @py_assert17 = @py_assert13 * @py_assert15
    @py_assert18 = 60
    @py_assert20 = @py_assert17 * @py_assert18
    @py_assert3 = @py_assert11 < @py_assert20
    if not (@py_assert2 and @py_assert3):
        @py_format21 = @pytest_ar._call_reprcompare(('<', '<'), (@py_assert2, @py_assert3), ('%(py1)s < %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.time_until_next_event\n}()\n}.total_seconds\n}()\n}',
                                                                                             '%(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} < ((%(py14)s * %(py16)s) * %(py19)s)'), (@py_assert0, @py_assert11, @py_assert20)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(polar_sun) if 'polar_sun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(polar_sun) else 'polar_sun',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format23 = 'assert %(py22)s' % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert18 = @py_assert20 = None
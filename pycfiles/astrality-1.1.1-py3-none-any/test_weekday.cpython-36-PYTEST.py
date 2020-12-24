# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/event_listener/test_weekday.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2310 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import datetime, timedelta
import logging, pytest
from astrality.event_listener import Weekday

@pytest.fixture
def weekday():
    """Return default weekday timer."""
    return Weekday({'type': 'weekday'})


@pytest.fixture
def noon_friday():
    return datetime(year=2018, month=1, day=26, hour=12)


def test_weekday_events(weekday):
    @py_assert1 = weekday.events
    @py_assert4 = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
                   'sunday')
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.events\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(weekday) if 'weekday' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday) else 'weekday',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_weekday_event(weekday, noon_friday, freezer):
    """Test that the correct weekday is identified."""
    freezer.move_to(noon_friday)
    @py_assert1 = weekday.event
    @py_assert3 = @py_assert1()
    @py_assert6 = 'friday'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday) if 'weekday' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday) else 'weekday',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_weekday_time_until_next_event(weekday, noon_friday, freezer):
    """Test that the number of seconds until next weekday is correct."""
    freezer.move_to(noon_friday)
    @py_assert1 = weekday.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert7 = 12
    @py_assert9 = timedelta(hours=@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n} == %(py10)s\n{%(py10)s = %(py6)s(hours=%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(weekday) if 'weekday' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday) else 'weekday',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(timedelta) if 'timedelta' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timedelta) else 'timedelta',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_using_force_event_config_option(noon_friday, freezer, caplog):
    """Test the use of force_event option."""
    solar_event_listener_application_config = {'type':'weekday', 
     'force_event':'monday'}
    freezer.move_to(noon_friday)
    weekday_event_listener = Weekday(solar_event_listener_application_config)
    @py_assert1 = weekday_event_listener.event
    @py_assert3 = @py_assert1()
    @py_assert6 = 'monday'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday_event_listener) if 'weekday_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_event_listener) else 'weekday_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = caplog.record_tuples
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.record_tuples\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_using_force_event_config_option_with_wrong_event_type(noon_friday, freezer, caplog):
    """Test the use of force_event with an invalid event type."""
    solar_event_listener_application_config = {'type':'weekday', 
     'force_event':'Mothers_day'}
    freezer.move_to(noon_friday)
    weekday_event_listener = Weekday(solar_event_listener_application_config)
    @py_assert1 = weekday_event_listener.event
    @py_assert3 = @py_assert1()
    @py_assert6 = 'Mothers_day'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday_event_listener) if 'weekday_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_event_listener) else 'weekday_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = logging.WARNING
    @py_assert4 = caplog.record_tuples[0][1]
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.WARNING\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(logging) if 'logging' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(logging) else 'logging',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
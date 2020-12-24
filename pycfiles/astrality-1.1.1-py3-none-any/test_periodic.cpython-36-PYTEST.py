# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/event_listener/test_periodic.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2486 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import datetime, timedelta
import pytest
from astrality.event_listener import Periodic

@pytest.fixture
def periodic():
    """Return a default periodic timer."""
    return Periodic({'type': 'periodic'})


@pytest.mark.parametrize('event, is_event', [
 ('0', True),
 ('1', True),
 ('80', True),
 ('-1', False),
 ('1.2', False),
 ('night', False)])
def test_periodic_events_are_correctly_identified(event, is_event, periodic):
    """Test that events are correctly identified as valid."""
    @py_assert3 = periodic.events
    @py_assert1 = event in @py_assert3
    @py_assert7 = @py_assert1 == is_event
    if not @py_assert7:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s.events\n}', ), (event, @py_assert3)) % {'py0':@pytest_ar._saferepr(event) if 'event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event) else 'event',  'py2':@pytest_ar._saferepr(periodic) if 'periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(periodic) else 'periodic',  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('(%(py6)s) == %(py8)s', ), (@py_assert1, is_event)) % {'py6':@py_format5,  'py8':@pytest_ar._saferepr(is_event) if 'is_event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_event) else 'is_event'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert7 = None


def test_periodic_beginning_event(freezer):
    """Test that the first event is 0."""
    periodic = Periodic({})
    @py_assert1 = periodic.event
    @py_assert3 = @py_assert1()
    @py_assert6 = '0'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(periodic) if 'periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(periodic) else 'periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_periodic_standard_timedelta(freezer):
    """Test that the maximum timedelta is returned."""
    default_periodic = Periodic({})
    @py_assert1 = default_periodic.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 3600
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(default_periodic) if 'default_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_periodic) else 'default_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_using_custom_periodic_event_listener(freezer):
    """Test that a custom defined period is correctly behaved."""
    custom_periodic_config = {'type':'periodic', 
     'seconds':1, 
     'minutes':2, 
     'hours':3, 
     'days':4}
    custom_periodic = Periodic(custom_periodic_config)
    @py_assert1 = custom_periodic.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert7 = 1
    @py_assert9 = 2
    @py_assert11 = 3
    @py_assert13 = 4
    @py_assert15 = timedelta(seconds=@py_assert7, minutes=@py_assert9, hours=@py_assert11, days=@py_assert13)
    @py_assert5 = @py_assert3 == @py_assert15
    if not @py_assert5:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n} == %(py16)s\n{%(py16)s = %(py6)s(seconds=%(py8)s, minutes=%(py10)s, hours=%(py12)s, days=%(py14)s)\n}', ), (@py_assert3, @py_assert15)) % {'py0':@pytest_ar._saferepr(custom_periodic) if 'custom_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_periodic) else 'custom_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(timedelta) if 'timedelta' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timedelta) else 'timedelta',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_weekday_time_until_next_event_of_periodic_event_listener(freezer):
    """Test that time left until next event is always correct."""
    now = datetime.now()
    freezer.move_to(now)
    default_periodic = Periodic({})
    @py_assert1 = default_periodic.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 60
    @py_assert12 = 60
    @py_assert14 = @py_assert10 * @py_assert12
    @py_assert9 = @py_assert7 == @py_assert14
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == (%(py11)s * %(py13)s)', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(default_periodic) if 'default_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_periodic) else 'default_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = None
    fourty_minutes = timedelta(minutes=40)
    freezer.move_to(now + fourty_minutes)
    @py_assert1 = default_periodic.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 20
    @py_assert12 = 60
    @py_assert14 = @py_assert10 * @py_assert12
    @py_assert9 = @py_assert7 == @py_assert14
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == (%(py11)s * %(py13)s)', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(default_periodic) if 'default_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_periodic) else 'default_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = None
    freezer.move_to(now + 2 * fourty_minutes)
    @py_assert1 = default_periodic.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert10 = 40
    @py_assert12 = 60
    @py_assert14 = @py_assert10 * @py_assert12
    @py_assert9 = @py_assert7 == @py_assert14
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == (%(py11)s * %(py13)s)', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(default_periodic) if 'default_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_periodic) else 'default_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_enumeration_of_periodic_event_listener_events(freezer):
    """Test that event is incremented by one correctly."""
    now = datetime.now()
    freezer.move_to(now)
    default_periodic = Periodic({})
    @py_assert1 = default_periodic.event
    @py_assert3 = @py_assert1()
    @py_assert6 = '0'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(default_periodic) if 'default_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_periodic) else 'default_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    fourty_minutes = timedelta(minutes=40)
    freezer.move_to(now + fourty_minutes)
    @py_assert1 = default_periodic.event
    @py_assert3 = @py_assert1()
    @py_assert6 = '0'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(default_periodic) if 'default_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_periodic) else 'default_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    freezer.move_to(now + 2 * fourty_minutes)
    @py_assert1 = default_periodic.event
    @py_assert3 = @py_assert1()
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.event\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(default_periodic) if 'default_periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_periodic) else 'default_periodic',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/event_listener/test_event_listener.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2404 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from astrality.event_listener import Periodic, Solar, Static, Weekday, event_listener_factory

@pytest.fixture
def solar_config():
    return {'type':'solar', 
     'longitude':1, 
     'latitude':2, 
     'elevation':3}


@pytest.fixture
def weekday_config():
    return {'type': 'weekday'}


@pytest.fixture
def periodic_config():
    return {'type':'periodic', 
     'seconds':0, 
     'minutes':1, 
     'hours':2, 
     'days':3}


@pytest.fixture
def static_config():
    return {'type': 'static'}


class TestEventListenerFactory:

    def test_event_listener_factory_with_solar_confi(self, solar_config):
        @py_assert3 = event_listener_factory(solar_config)
        @py_assert6 = isinstance(@py_assert3, Solar)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n}, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(event_listener_factory) if 'event_listener_factory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_listener_factory) else 'event_listener_factory',  'py2':@pytest_ar._saferepr(solar_config) if 'solar_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(solar_config) else 'solar_config',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(Solar) if 'Solar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Solar) else 'Solar',  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert3 = @py_assert6 = None

    def test_event_listener_factory_with_weekday_confi(self, weekday_config):
        @py_assert3 = event_listener_factory(weekday_config)
        @py_assert6 = isinstance(@py_assert3, Weekday)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n}, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(event_listener_factory) if 'event_listener_factory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_listener_factory) else 'event_listener_factory',  'py2':@pytest_ar._saferepr(weekday_config) if 'weekday_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_config) else 'weekday_config',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(Weekday) if 'Weekday' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Weekday) else 'Weekday',  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert3 = @py_assert6 = None

    def test_event_listener_factory_with_periodic_confi(self, periodic_config):
        @py_assert3 = event_listener_factory(periodic_config)
        @py_assert6 = isinstance(@py_assert3, Periodic)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n}, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(event_listener_factory) if 'event_listener_factory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_listener_factory) else 'event_listener_factory',  'py2':@pytest_ar._saferepr(periodic_config) if 'periodic_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(periodic_config) else 'periodic_config',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(Periodic) if 'Periodic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Periodic) else 'Periodic',  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert3 = @py_assert6 = None

    def test_event_listener_factory_with_static_confi(self, static_config):
        @py_assert3 = event_listener_factory(static_config)
        @py_assert6 = isinstance(@py_assert3, Static)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n}, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(event_listener_factory) if 'event_listener_factory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_listener_factory) else 'event_listener_factory',  'py2':@pytest_ar._saferepr(static_config) if 'static_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(static_config) else 'static_config',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(Static) if 'Static' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Static) else 'Static',  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert3 = @py_assert6 = None


@pytest.fixture
def solar_event_listener(solar_config):
    return Solar(solar_config)


@pytest.fixture
def weekday_event_listener(weekday_config):
    return Weekday(weekday_config)


@pytest.fixture
def periodic_event_listener(periodic_config):
    return Periodic(periodic_config)


@pytest.fixture
def static_event_listener(static_config):
    return Static(static_config)


class TestEventListenerDefaultConfiguration:

    def test_all_options_specified_of_solar_event_listener(self, solar_config, solar_event_listener):
        @py_assert1 = solar_event_listener.event_listener_config
        @py_assert3 = @py_assert1 == solar_config
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.event_listener_config\n} == %(py4)s', ), (@py_assert1, solar_config)) % {'py0':@pytest_ar._saferepr(solar_event_listener) if 'solar_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(solar_event_listener) else 'solar_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(solar_config) if 'solar_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(solar_config) else 'solar_config'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None

    def test_replacement_of_missing_event_listener_config_option(self, solar_config):
        solar_config.pop('elevation')
        solar_event_listener = Solar(solar_config)
        @py_assert1 = solar_event_listener.event_listener_config
        @py_assert3 = @py_assert1 != solar_config
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.event_listener_config\n} != %(py4)s', ), (@py_assert1, solar_config)) % {'py0':@pytest_ar._saferepr(solar_event_listener) if 'solar_event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(solar_event_listener) else 'solar_event_listener',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(solar_config) if 'solar_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(solar_config) else 'solar_config'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert0 = solar_event_listener.event_listener_config['longitude']
        @py_assert3 = 1
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = solar_event_listener.event_listener_config['latitude']
        @py_assert3 = 2
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = solar_event_listener.event_listener_config['elevation']
        @py_assert3 = 0
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
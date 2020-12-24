# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/tests/test_settings.py
# Compiled at: 2015-06-17 12:23:17
# Size of source mod 2**32: 1749 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, yield_fixture
from mock import patch
from ..settings import SettingsFactory

class TestSettingsFactory(object):

    @fixture
    def factory(self):
        return SettingsFactory('mymodule', {'base': 'settings'})

    @yield_fixture
    def mFactory(self):
        patcher = patch('impaf.settings.Factory')
        with patcher as (mock):
            mock.return_value.make_settings.return_value = ({'one': 1},
             {'two': 2})
            yield mock

    def test_for_uwsgi(self, factory, mFactory):
        self._assert_factory(factory, mFactory, 'uwsgi', [
         ('local', False)])

    def test_for_tests(self, factory, mFactory):
        self._assert_factory(factory, mFactory, 'tests', [
         ('tests', False)])

    def test_for_shell(self, factory, mFactory):
        self._assert_factory(factory, mFactory, 'shell', [
         ('shell', False), ('local_shell', False)])

    def test_for_command(self, factory, mFactory):
        self._assert_factory(factory, mFactory, 'command', [
         ('command', False), ('local_command', False)])

    def _assert_factory(self, factory, mFactory, endpoint, modules):
        @py_assert1 = factory.get_for
        @py_assert4 = @py_assert1(endpoint)
        @py_assert7 = (
         {'one': 1, 'paths': {'two': 2}}, {'two': 2})
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_for\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(factory) if 'factory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(factory) else 'factory', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(endpoint) if 'endpoint' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(endpoint) else 'endpoint', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
        mFactory.assert_called_once_with('mymodule')
        external_factory = mFactory.return_value
        external_factory.make_settings(settings=factory.settings, additional_modules=modules)
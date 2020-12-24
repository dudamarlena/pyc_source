# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/tests/test_application.py
# Compiled at: 2015-06-26 13:59:22
# Size of source mod 2**32: 3062 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, yield_fixture
from mock import MagicMock, patch
from ..application import Application

class ExampleApplication(Application):

    def __init__(self, module, settings_factory):
        super().__init__(module)
        self._settings_factory = settings_factory

    def _generate_settings(self, settings, endpoint):
        super()._generate_settings(settings, endpoint, self._settings_factory)


class TestApplication(object):

    @fixture
    def app(self, mSettingsFactory):
        return ExampleApplication('module', mSettingsFactory)

    @fixture
    def mSettingsFactory(self):
        return MagicMock()

    @yield_fixture
    def mConfigurator(self, app):
        patcher = patch('impaf.application.Configurator')
        with patcher as (mock):
            yield mock

    @yield_fixture
    def m_create_app(self, app):
        patcher = patch.object(app, '_create_app')
        with patcher as (mock):
            yield mock

    @yield_fixture
    def mimport_module(self):
        patcher = patch('impaf.application.import_module')
        with patcher as (mock):
            yield mock

    def test_create_app(self, app, mSettingsFactory, mConfigurator, mimport_module):
        """
        ._create_app should:
            - generate settings
            - create pyramid.config.Configurator
            - populate Configurator.registry
            - create routes
        """
        get_for = mSettingsFactory.return_value.get_for
        settings = MagicMock()
        paths = MagicMock()
        get_for.return_value = (settings, paths)
        mConfigurator.return_value.registry = {}
        mimport_module.return_value.__file__ = 'path'
        app._create_app({'base': 'settings'}, 'uwsgi')
        mimport_module.assert_called_once_with('module')
        @py_assert1 = app.settings
        @py_assert3 = @py_assert1 == settings
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.settings\n} == %(py4)s', ), (@py_assert1, settings)) % {'py4': @pytest_ar._saferepr(settings) if 'settings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(settings) else 'settings', 'py0': @pytest_ar._saferepr(app) if 'app' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app) else 'app', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = app.paths
        @py_assert3 = @py_assert1 == paths
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.paths\n} == %(py4)s', ), (@py_assert1, paths)) % {'py4': @pytest_ar._saferepr(paths) if 'paths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paths) else 'paths', 'py0': @pytest_ar._saferepr(app) if 'app' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app) else 'app', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        mConfigurator.assert_called_once_with(settings=settings.to_dict.return_value)
        @py_assert1 = app.config
        @py_assert5 = mConfigurator.return_value
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} == %(py6)s\n{%(py6)s = %(py4)s.return_value\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(mConfigurator) if 'mConfigurator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mConfigurator) else 'mConfigurator', 'py0': @pytest_ar._saferepr(app) if 'app' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app) else 'app', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = mConfigurator.return_value
        @py_assert3 = @py_assert1.registry
        @py_assert6 = {'settings': settings, 'paths': paths}
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.return_value\n}.registry\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(mConfigurator) if 'mConfigurator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mConfigurator) else 'mConfigurator', 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_run_uwsgi(self, app, m_create_app):
        """
        run_uwsgi should create wsgi app
        """
        app.config = MagicMock()
        result = app({'base': 'settings'})
        @py_assert3 = app.config
        @py_assert5 = @py_assert3.make_wsgi_app
        @py_assert7 = @py_assert5.return_value
        @py_assert1 = result == @py_assert7
        if not @py_assert1:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.config\n}.make_wsgi_app\n}.return_value\n}', ), (result, @py_assert7)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result', 'py6': @pytest_ar._saferepr(@py_assert5), 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(app) if 'app' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app) else 'app'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        m_create_app.assert_called_once_with({'base': 'settings'}, 'uwsgi')

    def test_run_tests(self, app, m_create_app):
        app.run_tests({'base': 'settings'})
        m_create_app.assert_called_once_with({'base': 'settings'}, 'tests')

    def test_run_shell(self, app, m_create_app):
        app.run_shell({'base': 'settings'})
        m_create_app.assert_called_once_with({'base': 'settings'}, 'shell')

    def test_run_command(self, app, m_create_app):
        app.run_command({'base': 'settings'})
        m_create_app.assert_called_once_with({'base': 'settings'}, 'command')
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/tests/test_routing.py
# Compiled at: 2015-08-05 13:44:09
# Size of source mod 2**32: 5888 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import fixture, yield_fixture
from mock import MagicMock, patch, sentinel
from tempfile import NamedTemporaryFile
from yaml import dump
from ..routing import RouteYamlParser, Routing

class TestRouteYamlParser(object):

    @fixture
    def parser(self):
        return RouteYamlParser('/highway/to/hell')

    @yield_fixture
    def mread_yaml(self, parser):
        patcher = patch.object(parser, 'read_yaml')
        with patcher as (mock):
            yield mock

    @yield_fixture
    def mparse_route_yaml(self, parser):
        patcher = patch.object(parser, '_parse_route_yaml')
        with patcher as (mock):
            yield mock

    def test_parse(self, parser, mread_yaml, mparse_route_yaml):

        def example_generator(data):
            yield 10

        def side_effect():
            parser.data = sentinel.data

        mread_yaml.side_effect = side_effect
        mparse_route_yaml.side_effect = example_generator
        @py_assert2 = parser.parse
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         10]
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.parse\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        mread_yaml.assert_called_once_with()
        mparse_route_yaml.assert_called_once_with(sentinel.data)

    def test_read_yaml(self, parser):
        tmp = NamedTemporaryFile(delete=False)
        tmp.write(bytes(dump({'mydata': 15}), 'utf8'))
        tmp.close()
        parser.path = tmp.name
        parser.read_yaml()
        @py_assert1 = parser.data
        @py_assert4 = {'mydata': 15}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.data\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_parsing(self, parser):
        data = {'convent': {'controllers': [
                                     {'controller': 'ConventListController', 
                                      'route': 'convent:list', 
                                      'url': '/'},
                                     {'controller': 'ConventEditController', 
                                      'route': 'convent:edit', 
                                      'url': '/edit'}]}, 
         
         'game': {'controllers': [
                                  {'controller': 'GameListController', 
                                   'route': 'game:list', 
                                   'url': '/g'},
                                  {'controller': 'GameEditController', 
                                   'route': 'game:edit', 
                                   'url': '/g/edit'}]}}
        result = list(parser._parse_route_yaml(data))
        key_sorting = lambda x: x['controller']
        result.sort(key=key_sorting)
        @py_assert3 = [
         {'controller': 'convent.controllers.ConventListController', 'route': 'convent:list', 'url': '/'}, {'controller': 'convent.controllers.ConventEditController', 'route': 'convent:edit', 'url': '/edit'}, {'controller': 'game.controllers.GameListController', 'route': 'game:list', 'url': '/g'}, {'controller': 'game.controllers.GameEditController', 'route': 'game:edit', 'url': '/g/edit'}]
        @py_assert6 = sorted(@py_assert3, key=key_sorting)
        @py_assert1 = result == @py_assert6
        if not @py_assert1:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py2)s(%(py4)s, key=%(py5)s)\n}', ), (result, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result', 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(key_sorting) if 'key_sorting' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(key_sorting) else 'key_sorting', 'py2': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted'}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert6 = None


class ExampleController(object):
    renderer = 'myrenderer'
    path_info = None


class TestRouting(object):

    @fixture
    def mapp(self):
        return MagicMock()

    @fixture
    def routing(self, mapp):
        return Routing(mapp)

    @yield_fixture
    def mRouteYamlParser(self):
        patcher = patch('impaf.routing.RouteYamlParser')
        with patcher as (mock):
            yield mock

    @fixture
    def mconfig(self, mapp):
        return mapp.config

    @fixture
    def mpaths(self, mapp):
        return mapp.paths

    @yield_fixture
    def madd(self, routing):
        patcher = patch.object(routing, 'add')
        with patcher as (mock):
            yield mock

    @yield_fixture
    def madd_view(self, routing):
        patcher = patch.object(routing, 'add_view')
        with patcher as (mock):
            yield mock

    @yield_fixture
    def mread_from_file(self, routing):
        patcher = patch.object(routing, 'read_from_file')
        with patcher as (mock):
            yield mock

    def test_read_from_file(self, routing, mRouteYamlParser, madd):
        """
        .read_from_file should parse yaml file and add routes from it
        """
        mroute = {'controller': 'something'}
        mRouteYamlParser.return_value.parse.return_value = [mroute]
        routing.read_from_file(sentinel.pathtofile)
        madd.assert_called_once_with(**mroute)
        mRouteYamlParser.assert_called_once_with(sentinel.pathtofile)
        mRouteYamlParser.return_value.parse.assert_called_once_with()

    def test_add(self, routing, mconfig, madd_view):
        routing.add('controller', 'route', 'url', 'arg', kw='arg')
        mconfig.add_route('route', 'url', 'arg', kw='arg')
        madd_view.assert_called_once_with('controller', route_name='route')

    def test_add_view(self, routing, mconfig):
        mconfig.maybe_dotted.return_value = ExampleController
        routing.add_view('impaf.tests.test_routing.ExampleController', route_name='something')
        mconfig.add_view('impaf.tests.test_routing.ExampleController', route_name='something', renderer='myrenderer')

    def test_read_from_dotted(self, routing, mpaths, mread_from_file):
        routing.read_from_dotted('my.dotted.path')
        mpaths.get_path_dotted.assert_called_once_with('my.dotted.path')
        mread_from_file.assert_called_once_with(mpaths.get_path_dotted.return_value)
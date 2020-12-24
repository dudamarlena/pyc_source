# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/allengooch/Projects/personal/configaro/tests/test_configaro.py
# Compiled at: 2018-05-29 11:34:07
# Size of source mod 2**32: 7767 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, munch, pytest
CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config'))
SAMPLE_DATA = {'name':'defaults', 
 'log':{'file':'some-file.txt', 
  'level':'ERROR'}, 
 'monitoring':{'haproxy':{'disabled': False}, 
  'nginx':{'disabled': True}}}

def test__module_path():
    from configaro import _module_path
    @py_assert2 = 'defaults'
    @py_assert4 = _module_path(CONFIG_DIR, @py_assert2)
    @py_assert8 = os.path
    @py_assert10 = @py_assert8.join
    @py_assert13 = 'defaults.py'
    @py_assert15 = @py_assert10(CONFIG_DIR, @py_assert13)
    @py_assert6 = @py_assert4 == @py_assert15
    if not @py_assert6:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py16)s\n{%(py16)s = %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s.path\n}.join\n}(%(py12)s, %(py14)s)\n}', ), (@py_assert4, @py_assert15)) % {'py0':@pytest_ar._saferepr(_module_path) if '_module_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_module_path) else '_module_path',  'py1':@pytest_ar._saferepr(CONFIG_DIR) if 'CONFIG_DIR' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CONFIG_DIR) else 'CONFIG_DIR',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py12':@pytest_ar._saferepr(CONFIG_DIR) if 'CONFIG_DIR' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CONFIG_DIR) else 'CONFIG_DIR',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None


def test__import_module():
    from configaro import _import_module
    module = _import_module(CONFIG_DIR, 'defaults')
    @py_assert1 = module.config
    @py_assert3 = @py_assert1 == SAMPLE_DATA
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} == %(py4)s', ), (@py_assert1, SAMPLE_DATA)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(SAMPLE_DATA) if 'SAMPLE_DATA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SAMPLE_DATA) else 'SAMPLE_DATA'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    with pytest.raises(ImportError):
        _import_module(CONFIG_DIR, 'default')


def test__merge():
    from configaro import _merge
    defaults = SAMPLE_DATA
    locals = {'name':'locals', 
     'log':{'level': 'DEBUG'}, 
     'monitoring':{'haproxy': {'disabled': True}}}
    expected = {'name':'locals', 
     'log':{'file':'some-file.txt', 
      'level':'DEBUG'}, 
     'monitoring':{'haproxy':{'disabled': True}, 
      'nginx':{'disabled': True}}}
    merged = dict(_merge(defaults, locals))
    @py_assert1 = merged == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (merged, expected)) % {'py0':@pytest_ar._saferepr(merged) if 'merged' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merged) else 'merged',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test__load():
    from configaro import _load, _module_path
    path = _module_path(CONFIG_DIR, 'defaults')
    config = _load(path)
    @py_assert0 = config['name']
    @py_assert3 = 'defaults'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test__cast():
    from configaro import _cast
    @py_assert1 = 'None'
    @py_assert3 = _cast(@py_assert1)
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(_cast) if '_cast' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_cast) else '_cast',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = 'False'
    @py_assert4 = _cast(@py_assert2)
    @py_assert7 = isinstance(@py_assert4, bool)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(_cast) if '_cast' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_cast) else '_cast',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(bool) if 'bool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bool) else 'bool',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert2 = '1'
    @py_assert4 = _cast(@py_assert2)
    @py_assert7 = isinstance(@py_assert4, int)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(_cast) if '_cast' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_cast) else '_cast',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert2 = '1.234'
    @py_assert4 = _cast(@py_assert2)
    @py_assert7 = isinstance(@py_assert4, float)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(_cast) if '_cast' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_cast) else '_cast',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(float) if 'float' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(float) else 'float',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert2 = 'Hello'
    @py_assert4 = _cast(@py_assert2)
    @py_assert7 = isinstance(@py_assert4, str)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(_cast) if '_cast' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_cast) else '_cast',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert7 = None


def test__get():
    from configaro import ConfigPropertyNotFoundError, _get
    data = munch.munchify(SAMPLE_DATA)
    @py_assert2 = 'name'
    @py_assert4 = _get(data, @py_assert2)
    @py_assert7 = 'defaults'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = 'log.level'
    @py_assert4 = _get(data, @py_assert2)
    @py_assert7 = 'ERROR'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = 'monitoring.haproxy.disabled'
    @py_assert4 = _get(data, @py_assert2)
    @py_assert7 = False
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = 'monitoring.nginx.disabled'
    @py_assert4 = _get(data, @py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    with pytest.raises(ConfigPropertyNotFoundError):
        @py_assert2 = 'monitoring.nginx.disable'
        @py_assert4 = _get(data, @py_assert2)
        @py_assert7 = True
        @py_assert6 = @py_assert4 is @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = 'monitoring.nginx.disable'
    @py_assert4 = None
    @py_assert6 = _get(data, @py_assert2, default=@py_assert4)
    @py_assert9 = None
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py1)s, %(py3)s, default=%(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test__put():
    from configaro import _get, _put
    data = munch.munchify(SAMPLE_DATA)
    _put(data, 'name', 'locals')
    @py_assert2 = 'name'
    @py_assert4 = _get(data, @py_assert2)
    @py_assert7 = 'locals'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    _put(data, 'log.level', 'DEBUG')
    @py_assert2 = 'log.level'
    @py_assert4 = _get(data, @py_assert2)
    @py_assert7 = 'DEBUG'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_get) if '_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get) else '_get',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test__config_package_dir():
    from configaro import _config_package_dir
    @py_assert1 = 'tests.config'
    @py_assert3 = _config_package_dir(@py_assert1)
    @py_assert5 = @py_assert3 == CONFIG_DIR
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py6)s', ), (@py_assert3, CONFIG_DIR)) % {'py0':@pytest_ar._saferepr(_config_package_dir) if '_config_package_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_config_package_dir) else '_config_package_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(CONFIG_DIR) if 'CONFIG_DIR' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(CONFIG_DIR) else 'CONFIG_DIR'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test___config_module_paths():
    from configaro import _config_module_paths
    expected = [
     os.path.join(CONFIG_DIR, 'defaults.py'),
     os.path.join(CONFIG_DIR, 'locals.py')]
    paths = _config_module_paths('tests.config')
    @py_assert2 = sorted(paths)
    @py_assert7 = sorted(expected)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py1':@pytest_ar._saferepr(paths) if 'paths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paths) else 'paths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None


def test_exports():
    from configaro import __all__ as exports
    expected = [
     'ConfigError',
     'ConfigModuleNotFoundError',
     'ConfigModuleNotValidError',
     'ConfigObjectNotInitialized',
     'ConfigPropertyNotFoundError',
     'ConfigPropertyNotScalarError',
     'ConfigUpdateNotValidError',
     'get',
     'init',
     'put']
    @py_assert2 = sorted(exports)
    @py_assert7 = sorted(expected)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py1':@pytest_ar._saferepr(exports) if 'exports' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exports) else 'exports',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None


def test_init():
    from configaro import init
    init('tests.config')


def test_get():
    from configaro import ConfigPropertyNotFoundError, get, init
    init('tests.config')
    expected = {'name':'locals', 
     'log':{'file':'some-file.txt', 
      'level':'DEBUG'}, 
     'monitoring':{'haproxy':{'disabled': True}, 
      'nginx':{'disabled': True}}}
    config = get()
    @py_assert1 = config.log
    @py_assert3 = @py_assert1.level
    @py_assert6 = 'DEBUG'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.log\n}.level\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert3 = munch.munchify
    @py_assert6 = @py_assert3(expected)
    @py_assert1 = config == @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.munchify\n}(%(py5)s)\n}', ), (config, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(munch) if 'munch' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(munch) else 'munch',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    log = get('log')
    @py_assert1 = log.level
    @py_assert4 = 'DEBUG'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.level\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    log = munch.unmunchify(log)
    @py_assert2 = expected['log']
    @py_assert1 = log == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (log, @py_assert2)) % {'py0':@pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = 'name'
    @py_assert3 = get(@py_assert1)
    @py_assert6 = 'locals'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'log.level'
    @py_assert3 = get(@py_assert1)
    @py_assert6 = 'DEBUG'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'monitoring.haproxy.disabled'
    @py_assert3 = get(@py_assert1)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'monitoring.nginx.disabled'
    @py_assert3 = get(@py_assert1)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    with pytest.raises(ConfigPropertyNotFoundError):
        @py_assert1 = 'monitoring.nginx.disable'
        @py_assert3 = get(@py_assert1)
        @py_assert6 = True
        @py_assert5 = @py_assert3 is @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'monitoring.nginx.disable'
    @py_assert3 = None
    @py_assert5 = get(@py_assert1, default=@py_assert3)
    @py_assert8 = None
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, default=%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_put():
    from configaro import ConfigPropertyNotScalarError, ConfigUpdateNotValidError, get, init, put
    init('tests.config')
    put('log.level=INFO')
    config = get()
    @py_assert1 = config.log
    @py_assert3 = @py_assert1.level
    @py_assert6 = 'INFO'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.log\n}.level\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    with pytest.raises(ConfigUpdateNotValidError):
        put('log.level')
    with pytest.raises(ConfigPropertyNotScalarError):
        put('log=INFO')


def test_ConfigaroError():
    from configaro import ConfigError
    message = 'this is an error'
    error = ConfigError(message)
    @py_assert1 = error.message
    @py_assert3 = @py_assert1 == message
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py4)s', ), (@py_assert1, message)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_NotInitializedError():
    from configaro import ConfigError, ConfigObjectNotInitialized
    error = ConfigObjectNotInitialized()
    @py_assert3 = isinstance(error, ConfigError)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(ConfigError) if 'ConfigError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ConfigError) else 'ConfigError',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = error.message
    @py_assert4 = 'config object not initialized'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_ConfigNotFoundError():
    from configaro import ConfigError, ConfigModuleNotFoundError
    path = '/some/path'
    error = ConfigModuleNotFoundError(path)
    @py_assert3 = isinstance(error, ConfigError)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(ConfigError) if 'ConfigError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ConfigError) else 'ConfigError',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = error.message
    @py_assert4 = f"config module not found: {path}"
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = error.path
    @py_assert3 = @py_assert1 == path
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, path)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    path = '/another/path'
    error = ConfigModuleNotFoundError(path=path)
    @py_assert1 = error.path
    @py_assert3 = @py_assert1 == path
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, path)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_ConfigNotValidError():
    from configaro import ConfigError, ConfigModuleNotValidError
    path = '/some/path'
    error = ConfigModuleNotValidError(path)
    @py_assert3 = isinstance(error, ConfigError)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(ConfigError) if 'ConfigError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ConfigError) else 'ConfigError',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = error.message
    @py_assert4 = f"config module not valid: {path}"
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = error.path
    @py_assert3 = @py_assert1 == path
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, path)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    error = ConfigModuleNotValidError(path=path)
    @py_assert1 = error.path
    @py_assert3 = @py_assert1 == path
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, path)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_PropertyNotFoundError():
    from configaro import ConfigError, ConfigPropertyNotFoundError
    data = None
    prop_name = 'prop.inner'
    error = ConfigPropertyNotFoundError(data, prop_name)
    @py_assert3 = isinstance(error, ConfigError)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(ConfigError) if 'ConfigError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ConfigError) else 'ConfigError',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = error.message
    @py_assert4 = f"config property not found: {prop_name}"
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = error.data
    @py_assert3 = @py_assert1 == data
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.data\n} == %(py4)s', ), (@py_assert1, data)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = error.prop_name
    @py_assert3 = @py_assert1 == prop_name
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.prop_name\n} == %(py4)s', ), (@py_assert1, prop_name)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(prop_name) if 'prop_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prop_name) else 'prop_name'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    error = ConfigPropertyNotFoundError(prop_name=prop_name, data=data)
    @py_assert1 = error.data
    @py_assert3 = @py_assert1 == data
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.data\n} == %(py4)s', ), (@py_assert1, data)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = error.prop_name
    @py_assert3 = @py_assert1 == prop_name
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.prop_name\n} == %(py4)s', ), (@py_assert1, prop_name)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(prop_name) if 'prop_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prop_name) else 'prop_name'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_PropertyNotScalarError():
    from configaro import ConfigError, ConfigPropertyNotScalarError
    data = None
    prop_name = 'prop.inner'
    error = ConfigPropertyNotScalarError(data, prop_name)
    @py_assert3 = isinstance(error, ConfigError)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(ConfigError) if 'ConfigError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ConfigError) else 'ConfigError',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = error.message
    @py_assert4 = f"config property not scalar: {prop_name}"
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = error.data
    @py_assert3 = @py_assert1 == data
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.data\n} == %(py4)s', ), (@py_assert1, data)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = error.prop_name
    @py_assert3 = @py_assert1 == prop_name
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.prop_name\n} == %(py4)s', ), (@py_assert1, prop_name)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(prop_name) if 'prop_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prop_name) else 'prop_name'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    error = ConfigPropertyNotScalarError(prop_name=prop_name, data=data)
    @py_assert1 = error.data
    @py_assert3 = @py_assert1 == data
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.data\n} == %(py4)s', ), (@py_assert1, data)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = error.prop_name
    @py_assert3 = @py_assert1 == prop_name
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.prop_name\n} == %(py4)s', ), (@py_assert1, prop_name)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(prop_name) if 'prop_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prop_name) else 'prop_name'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_UpdateNotValidError():
    from configaro import ConfigError, ConfigUpdateNotValidError
    update = 'prop=value'
    error = ConfigUpdateNotValidError(update)
    @py_assert3 = isinstance(error, ConfigError)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(ConfigError) if 'ConfigError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ConfigError) else 'ConfigError',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = error.message
    @py_assert4 = f"config update not valid: {update}"
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.message\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = error.update
    @py_assert3 = @py_assert1 == update
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.update\n} == %(py4)s', ), (@py_assert1, update)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(update) if 'update' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(update) else 'update'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    error = ConfigUpdateNotValidError(update=update)
    @py_assert1 = error.update
    @py_assert3 = @py_assert1 == update
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.update\n} == %(py4)s', ), (@py_assert1, update)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(update) if 'update' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(update) else 'update'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
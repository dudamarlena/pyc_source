# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/itxaka/Projects/tox-plus/tests/test_interpreters.py
# Compiled at: 2015-09-01 06:06:20
# Size of source mod 2**32: 3456 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, os, pytest
from tox_plus.interpreters import *
from tox_plus.config import get_plugin_manager

@pytest.fixture
def interpreters():
    pm = get_plugin_manager()
    return Interpreters(hook=pm.hook)


@pytest.mark.skipif("sys.platform != 'win32'")
def test_locate_via_py(monkeypatch):

    class PseudoPy:

        def sysexec(self, *args):
            @py_assert0 = args[0]
            @py_assert3 = '-3.2'
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            @py_assert0 = args[1]
            @py_assert3 = '-c'
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            return sys.executable

    @staticmethod
    def ret_pseudopy(name):
        @py_assert2 = 'py'
        @py_assert1 = name == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (name, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        return PseudoPy()

    monkeypatch.setattr(py.path.local, 'sysfind', ret_pseudopy)
    @py_assert1 = '3'
    @py_assert3 = '2'
    @py_assert5 = locate_via_py(@py_assert1, @py_assert3)
    @py_assert9 = sys.executable
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.executable\n}', ), (@py_assert5, @py_assert9)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(locate_via_py) if 'locate_via_py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(locate_via_py) else 'locate_via_py',  'py4': @pytest_ar._saferepr(@py_assert3),  'py8': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_tox_get_python_executable():

    class envconfig:
        basepython = sys.executable
        envname = 'pyxx'

    p = tox_get_python_executable(envconfig)
    @py_assert3 = py.path
    @py_assert5 = @py_assert3.local
    @py_assert8 = sys.executable
    @py_assert10 = @py_assert5(@py_assert8)
    @py_assert1 = p == @py_assert10
    if not @py_assert1:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.path\n}.local\n}(%(py9)s\n{%(py9)s = %(py7)s.executable\n})\n}',), (p, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py4': @pytest_ar._saferepr(@py_assert3),  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py11': @pytest_ar._saferepr(@py_assert10),  'py7': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys'}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    for ver in [''] + '2.4 2.5 2.6 2.7 3.0 3.1 3.2 3.3'.split():
        name = 'python%s' % ver
        if sys.platform == 'win32':
            pydir = 'python%s' % ver.replace('.', '')
            x = py.path.local('c:\\%s' % pydir)
            print(x)
            if not x.check():
                continue
        else:
            if not py.path.local.sysfind(name):
                continue
            envconfig.basepython = name
            p = tox_get_python_executable(envconfig)
            if not p:
                @py_format1 = ('' + 'assert %(py0)s') % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format1))
            popen = py.std.subprocess.Popen([str(p), '-V'], stderr=py.std.subprocess.PIPE)
            stdout, stderr = popen.communicate()
            @py_assert3 = py.builtin
            @py_assert5 = @py_assert3._totext
            @py_assert8 = 'ascii'
            @py_assert10 = @py_assert5(stderr, @py_assert8)
            @py_assert1 = ver in @py_assert10
            if not @py_assert1:
                @py_format12 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.builtin\n}._totext\n}(%(py7)s, %(py9)s)\n}',), (ver, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(ver) if 'ver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ver) else 'ver',  'py4': @pytest_ar._saferepr(@py_assert3),  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py11': @pytest_ar._saferepr(@py_assert10),  'py7': @pytest_ar._saferepr(stderr) if 'stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stderr) else 'stderr'}
                @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
                raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None


def test_find_executable_extra(monkeypatch):

    @staticmethod
    def sysfind(x):
        return 'hello'

    monkeypatch.setattr(py.path.local, 'sysfind', sysfind)

    class envconfig:
        basepython = '1lk23j'
        envname = 'pyxx'

    t = tox_get_python_executable(envconfig)
    @py_assert2 = 'hello'
    @py_assert1 = t == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (t, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(t) if 't' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(t) else 't'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_run_and_get_interpreter_info():
    name = os.path.basename(sys.executable)
    info = run_and_get_interpreter_info(name, sys.executable)
    @py_assert1 = info.version_info
    @py_assert6 = sys.version_info
    @py_assert8 = tuple(@py_assert6)
    @py_assert3 = @py_assert1 == @py_assert8
    if not @py_assert3:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.version_info\n} == %(py9)s\n{%(py9)s = %(py4)s(%(py7)s\n{%(py7)s = %(py5)s.version_info\n})\n}',), (@py_assert1, @py_assert8)) % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py4': @pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = info.name
    @py_assert3 = @py_assert1 == name
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py4)s',), (@py_assert1, name)) % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py4': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = info.executable
    @py_assert5 = sys.executable
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executable\n} == %(py6)s\n{%(py6)s = %(py4)s.executable\n}',), (@py_assert1, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py4': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


class TestInterpreters:

    def test_get_executable(self, interpreters):

        class envconfig:
            basepython = sys.executable
            envname = 'pyxx'

        x = interpreters.get_executable(envconfig)
        @py_assert3 = sys.executable
        @py_assert1 = x == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.executable\n}',), (x, @py_assert3)) % {'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys'}
            @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        info = interpreters.get_info(envconfig)
        @py_assert1 = info.version_info
        @py_assert6 = sys.version_info
        @py_assert8 = tuple(@py_assert6)
        @py_assert3 = @py_assert1 == @py_assert8
        if not @py_assert3:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.version_info\n} == %(py9)s\n{%(py9)s = %(py4)s(%(py7)s\n{%(py7)s = %(py5)s.version_info\n})\n}',), (@py_assert1, @py_assert8)) % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py4': @pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
        @py_assert1 = info.executable
        @py_assert5 = sys.executable
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executable\n} == %(py6)s\n{%(py6)s = %(py4)s.executable\n}',), (@py_assert1, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py4': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = info.runnable
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.runnable\n}') % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None

    def test_get_executable_no_exist(self, interpreters):

        class envconfig:
            basepython = '1lkj23'
            envname = 'pyxx'

        @py_assert1 = interpreters.get_executable
        @py_assert4 = @py_assert1(envconfig)
        @py_assert6 = not @py_assert4
        if not @py_assert6:
            @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_executable\n}(%(py3)s)\n}') % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py0': @pytest_ar._saferepr(interpreters) if 'interpreters' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interpreters) else 'interpreters',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert4 = @py_assert6 = None
        info = interpreters.get_info(envconfig)
        @py_assert1 = info.version_info
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.version_info\n}') % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = info.name
        @py_assert4 = '1lkj23'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = info.executable
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.executable\n}') % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = info.runnable
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.runnable\n}') % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None

    def test_get_sitepackagesdir_error(self, interpreters):

        class envconfig:
            basepython = sys.executable
            envname = '123'

        info = interpreters.get_info(envconfig)
        s = interpreters.get_sitepackagesdir(info, '')
        if not s:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
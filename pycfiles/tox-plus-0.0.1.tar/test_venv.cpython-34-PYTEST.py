# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/itxaka/Projects/tox-plus/tests/test_venv.py
# Compiled at: 2015-09-01 06:06:20
# Size of source mod 2**32: 20000 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, py, tox_plus, pytest, os, sys, tox_plus.config
from tox_plus.venv import *
from tox_plus.interpreters import NoInterpreterInfo

def test_getdigest(tmpdir):
    @py_assert2 = getdigest(tmpdir)
    @py_assert5 = '0'
    @py_assert7 = 32
    @py_assert9 = @py_assert5 * @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s * %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(getdigest) if 'getdigest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getdigest) else 'getdigest',  'py1': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_getsupportedinterpreter(monkeypatch, newconfig, mocksession):
    config = newconfig([], '\n        [testenv:python]\n        basepython=%s\n    ' % sys.executable)
    venv = VirtualEnv(config.envconfigs['python'], session=mocksession)
    interp = venv.getsupportedinterpreter()
    @py_assert1 = py.path
    @py_assert3 = @py_assert1.local
    @py_assert6 = @py_assert3(interp)
    @py_assert8 = @py_assert6.realpath
    @py_assert10 = @py_assert8()
    @py_assert14 = py.path
    @py_assert16 = @py_assert14.local
    @py_assert19 = sys.executable
    @py_assert21 = @py_assert16(@py_assert19)
    @py_assert23 = @py_assert21.realpath
    @py_assert25 = @py_assert23()
    @py_assert12 = @py_assert10 == @py_assert25
    if not @py_assert12:
        @py_format27 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.local\n}(%(py5)s)\n}.realpath\n}()\n} == %(py26)s\n{%(py26)s = %(py24)s\n{%(py24)s = %(py22)s\n{%(py22)s = %(py17)s\n{%(py17)s = %(py15)s\n{%(py15)s = %(py13)s.path\n}.local\n}(%(py20)s\n{%(py20)s = %(py18)s.executable\n})\n}.realpath\n}()\n}',), (@py_assert10, @py_assert25)) % {'py18': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py15': @pytest_ar._saferepr(@py_assert14),  'py22': @pytest_ar._saferepr(@py_assert21),  'py9': @pytest_ar._saferepr(@py_assert8),  'py24': @pytest_ar._saferepr(@py_assert23),  'py17': @pytest_ar._saferepr(@py_assert16),  'py2': @pytest_ar._saferepr(@py_assert1),  'py20': @pytest_ar._saferepr(@py_assert19),  'py0': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py4': @pytest_ar._saferepr(@py_assert3),  'py5': @pytest_ar._saferepr(interp) if 'interp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interp) else 'interp',  'py26': @pytest_ar._saferepr(@py_assert25),  'py7': @pytest_ar._saferepr(@py_assert6),  'py13': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py11': @pytest_ar._saferepr(@py_assert10)}
        @py_format29 = ('' + 'assert %(py28)s') % {'py28': @py_format27}
        raise AssertionError(@pytest_ar._format_explanation(@py_format29))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = None
    monkeypatch.setattr(sys, 'platform', 'win32')
    monkeypatch.setattr(venv.envconfig, 'basepython', 'jython')
    py.test.raises(tox_plus.exception.UnsupportedInterpreter, venv.getsupportedinterpreter)
    monkeypatch.undo()
    monkeypatch.setattr(venv.envconfig, 'envname', 'py1')
    monkeypatch.setattr(venv.envconfig, 'basepython', 'notexistingpython')
    py.test.raises(tox_plus.exception.InterpreterNotFound, venv.getsupportedinterpreter)
    monkeypatch.undo()
    info = NoInterpreterInfo(name=venv.name)
    info.executable = 'something'
    monkeypatch.setattr(config.interpreters, 'get_info', lambda *args**args: info)
    pytest.raises(tox_plus.exception.InvocationError, venv.getsupportedinterpreter)


def test_create(monkeypatch, mocksession, newconfig):
    config = newconfig([], '\n        [testenv:py123]\n    ')
    envconfig = config.envconfigs['py123']
    venv = VirtualEnv(envconfig, session=mocksession)
    @py_assert1 = venv.path
    @py_assert5 = envconfig.envdir
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py6)s\n{%(py6)s = %(py4)s.envdir\n}',), (@py_assert1, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = venv.path
    @py_assert3 = @py_assert1.check
    @py_assert5 = @py_assert3()
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.check\n}()\n}') % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 >= @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>=',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py6)s',), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = l[0].args
    @py_assert0 = 'virtualenv'
    @py_assert4 = args[2]
    @py_assert6 = str(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    if sys.platform != 'win32':
        @py_assert1 = py.path
        @py_assert3 = @py_assert1.local
        @py_assert6 = sys.executable
        @py_assert8 = @py_assert3(@py_assert6)
        @py_assert10 = @py_assert8.realpath
        @py_assert12 = @py_assert10()
        @py_assert16 = py.path
        @py_assert18 = @py_assert16.local
        @py_assert20 = args[0]
        @py_assert22 = @py_assert18(@py_assert20)
        @py_assert24 = @py_assert22.realpath
        @py_assert26 = @py_assert24()
        @py_assert14 = @py_assert12 == @py_assert26
        if not @py_assert14:
            @py_format28 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.local\n}(%(py7)s\n{%(py7)s = %(py5)s.executable\n})\n}.realpath\n}()\n} == %(py27)s\n{%(py27)s = %(py25)s\n{%(py25)s = %(py23)s\n{%(py23)s = %(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py15)s.path\n}.local\n}(%(py21)s)\n}.realpath\n}()\n}',), (@py_assert12, @py_assert26)) % {'py19': @pytest_ar._saferepr(@py_assert18),  'py27': @pytest_ar._saferepr(@py_assert26),  'py15': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py23': @pytest_ar._saferepr(@py_assert22),  'py9': @pytest_ar._saferepr(@py_assert8),  'py25': @pytest_ar._saferepr(@py_assert24),  'py17': @pytest_ar._saferepr(@py_assert16),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py4': @pytest_ar._saferepr(@py_assert3),  'py5': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py7': @pytest_ar._saferepr(@py_assert6),  'py21': @pytest_ar._saferepr(@py_assert20),  'py13': @pytest_ar._saferepr(@py_assert12),  'py11': @pytest_ar._saferepr(@py_assert10)}
            @py_format30 = ('' + 'assert %(py29)s') % {'py29': @py_format28}
            raise AssertionError(@pytest_ar._format_explanation(@py_format30))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert22 = @py_assert24 = @py_assert26 = None
        @py_assert1 = venv.getcommandpath
        @py_assert3 = 'easy_install'
        @py_assert6 = py.path
        @py_assert8 = @py_assert6.local
        @py_assert10 = @py_assert8()
        @py_assert12 = @py_assert1(@py_assert3, cwd=@py_assert10)
        if not @py_assert12:
            @py_format14 = ('' + 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.getcommandpath\n}(%(py4)s, cwd=%(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.local\n}()\n})\n}') % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py13': @pytest_ar._saferepr(@py_assert12),  'py11': @pytest_ar._saferepr(@py_assert10),  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py7': @pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    interp = venv._getliveconfig().python
    @py_assert3 = venv.envconfig
    @py_assert5 = @py_assert3.python_info
    @py_assert7 = @py_assert5.executable
    @py_assert1 = interp == @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.envconfig\n}.python_info\n}.executable\n}',), (interp, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(interp) if 'interp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interp) else 'interp',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = venv.path_config
    @py_assert3 = @py_assert1.check
    @py_assert5 = False
    @py_assert7 = @py_assert3(exists=@py_assert5)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path_config\n}.check\n}(exists=%(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


@pytest.mark.skipif("sys.platform == 'win32'")
def test_commandpath_venv_precendence(tmpdir, monkeypatch, mocksession, newconfig):
    config = newconfig([], '\n        [testenv:py123]\n    ')
    envconfig = config.envconfigs['py123']
    venv = VirtualEnv(envconfig, session=mocksession)
    tmpdir.ensure('easy_install')
    monkeypatch.setenv('PATH', str(tmpdir), prepend=os.pathsep)
    envconfig.envbindir.ensure('easy_install')
    p = venv.getcommandpath('easy_install')
    @py_assert1 = py.path
    @py_assert3 = @py_assert1.local
    @py_assert6 = @py_assert3(p)
    @py_assert8 = @py_assert6.relto
    @py_assert11 = envconfig.envbindir
    @py_assert13 = @py_assert8(@py_assert11)
    if not @py_assert13:
        @py_format15 = (@pytest_ar._format_assertmsg(p) + '\n>assert %(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.local\n}(%(py5)s)\n}.relto\n}(%(py12)s\n{%(py12)s = %(py10)s.envbindir\n})\n}') % {'py0': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py4': @pytest_ar._saferepr(@py_assert3),  'py14': @pytest_ar._saferepr(@py_assert13),  'py10': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(@py_assert1),  'py12': @pytest_ar._saferepr(@py_assert11),  'py5': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = None


def test_create_sitepackages(monkeypatch, mocksession, newconfig):
    config = newconfig([], '\n        [testenv:site]\n        sitepackages=True\n\n        [testenv:nosite]\n        sitepackages=False\n    ')
    envconfig = config.envconfigs['site']
    venv = VirtualEnv(envconfig, session=mocksession)
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 >= @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = l[0].args
    @py_assert0 = '--system-site-packages'
    @py_assert6 = map(str, args)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py4)s, %(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert6 = None
    mocksession._clearmocks()
    envconfig = config.envconfigs['nosite']
    venv = VirtualEnv(envconfig, session=mocksession)
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 >= @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = l[0].args
    @py_assert0 = '--system-site-packages'
    @py_assert6 = map(str, args)
    @py_assert2 = @py_assert0 not in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py7)s\n{%(py7)s = %(py3)s(%(py4)s, %(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert6 = None
    @py_assert0 = '--no-site-packages'
    @py_assert6 = map(str, args)
    @py_assert2 = @py_assert0 not in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py7)s\n{%(py7)s = %(py3)s(%(py4)s, %(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert6 = None


def test_install_deps_wildcard(newmocksession):
    mocksession = newmocksession([], '\n        [tox]\n        distshare = {toxworkdir}/distshare\n        [testenv:py123]\n        deps=\n            {distshare}/dep1-*\n    ')
    venv = mocksession.getenv('py123')
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    distshare = venv.session.config.distshare
    distshare.ensure('dep1-1.0.zip')
    distshare.ensure('dep1-1.1.zip')
    venv.install_deps()
    @py_assert2 = len(l)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = l[(-1)].args
    @py_assert0 = l[(-1)]
    @py_assert2 = @py_assert0.cwd
    @py_assert6 = venv.envconfig
    @py_assert8 = @py_assert6.config
    @py_assert10 = @py_assert8.toxinidir
    @py_assert4 = @py_assert2 == @py_assert10
    if not @py_assert4:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.cwd\n} == %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.envconfig\n}.config\n}.toxinidir\n}', ), (@py_assert2, @py_assert10)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py9': @pytest_ar._saferepr(@py_assert8),  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert0 = 'pip'
    @py_assert4 = args[0]
    @py_assert6 = str(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = args[1]
    @py_assert3 = 'install'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    args = [arg for arg in args if str(arg).endswith('dep1-1.1.zip')]
    @py_assert2 = len(args)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


@pytest.mark.parametrize('envdc', [True, False])
def test_install_downloadcache(newmocksession, monkeypatch, tmpdir, envdc):
    if envdc:
        monkeypatch.setenv('PIP_DOWNLOAD_CACHE', tmpdir)
    else:
        monkeypatch.delenv('PIP_DOWNLOAD_CACHE', raising=False)
    mocksession = newmocksession([], '\n        [testenv:py123]\n        deps=\n            dep1\n            dep2\n    ')
    venv = mocksession.getenv('py123')
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    venv.install_deps()
    @py_assert2 = len(l)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = l[(-1)].args
    @py_assert0 = l[(-1)]
    @py_assert2 = @py_assert0.cwd
    @py_assert6 = venv.envconfig
    @py_assert8 = @py_assert6.config
    @py_assert10 = @py_assert8.toxinidir
    @py_assert4 = @py_assert2 == @py_assert10
    if not @py_assert4:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.cwd\n} == %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.envconfig\n}.config\n}.toxinidir\n}', ), (@py_assert2, @py_assert10)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py9': @pytest_ar._saferepr(@py_assert8),  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert0 = 'pip'
    @py_assert4 = args[0]
    @py_assert6 = str(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = args[1]
    @py_assert3 = 'install'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'dep1'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'dep2'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    deps = list(filter(None, [x[1] for x in venv._getliveconfig().deps]))
    @py_assert2 = ['dep1', 'dep2']
    @py_assert1 = deps == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (deps, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(deps) if 'deps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(deps) else 'deps'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_install_deps_indexserver(newmocksession):
    mocksession = newmocksession([], '\n        [tox]\n        indexserver =\n            abc = ABC\n            abc2 = ABC\n        [testenv:py123]\n        deps=\n            dep1\n            :abc:dep2\n            :abc2:dep3\n    ')
    venv = mocksession.getenv('py123')
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    l[:] = []
    venv.install_deps()
    @py_assert2 = len(l)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = ' '.join(l[0].args)
    @py_assert0 = '-i '
    @py_assert2 = @py_assert0 not in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'dep1'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    args = ' '.join(l[1].args)
    @py_assert0 = '-i ABC'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'dep2'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    args = ' '.join(l[2].args)
    @py_assert0 = '-i ABC'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'dep3'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_install_deps_pre(newmocksession):
    mocksession = newmocksession([], '\n        [testenv]\n        pip_pre=true\n        deps=\n            dep1\n    ')
    venv = mocksession.getenv('python')
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    l[:] = []
    venv.install_deps()
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = ' '.join(l[0].args)
    @py_assert0 = '--pre '
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'dep1'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_installpkg_indexserver(newmocksession, tmpdir):
    mocksession = newmocksession([], '\n        [tox]\n        indexserver =\n            default = ABC\n    ')
    venv = mocksession.getenv('python')
    l = mocksession._pcalls
    p = tmpdir.ensure('distfile.tar.gz')
    mocksession.installpkg(venv, p)
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = ' '.join(l[0].args)
    @py_assert0 = '-i ABC'
    @py_assert2 = @py_assert0 in args
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_install_recreate(newmocksession, tmpdir):
    pkg = tmpdir.ensure('package.tar.gz')
    mocksession = newmocksession(['--recreate'], '\n        [testenv]\n        deps=xyz\n    ')
    venv = mocksession.getenv('python')
    venv.update()
    mocksession.installpkg(venv, pkg)
    mocksession.report.expect('verbosity0', '*create*')
    venv.update()
    mocksession.report.expect('verbosity0', '*recreate*')


def test_test_hashseed_is_in_output(newmocksession):
    original_make_hashseed = tox_plus.config.make_hashseed
    tox_plus.config.make_hashseed = lambda : '123456789'
    try:
        mocksession = newmocksession([], '\n            [testenv]\n        ')
    finally:
        tox_plus.config.make_hashseed = original_make_hashseed

    venv = mocksession.getenv('python')
    venv.update()
    venv.test()
    mocksession.report.expect('verbosity0', "python runtests: PYTHONHASHSEED='123456789'")


def test_test_runtests_action_command_is_in_output(newmocksession):
    mocksession = newmocksession([], '\n        [testenv]\n        commands = echo foo bar\n    ')
    venv = mocksession.getenv('python')
    venv.update()
    venv.test()
    mocksession.report.expect('verbosity0', '*runtests*commands?0? | echo foo bar')


def test_install_error(newmocksession, monkeypatch):
    mocksession = newmocksession(['--recreate'], '\n        [testenv]\n        deps=xyz\n        commands=\n            qwelkqw\n    ')
    venv = mocksession.getenv('python')
    venv.test()
    mocksession.report.expect('error', '*not find*qwelkqw*')
    @py_assert1 = venv.status
    @py_assert4 = 'commands failed'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_install_command_not_installed(newmocksession, monkeypatch):
    mocksession = newmocksession(['--recreate'], '\n        [testenv]\n        commands=\n            py.test\n    ')
    venv = mocksession.getenv('python')
    venv.test()
    mocksession.report.expect('warning', '*test command found but not*')
    @py_assert1 = venv.status
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_install_command_whitelisted(newmocksession, monkeypatch):
    mocksession = newmocksession(['--recreate'], '\n        [testenv]\n        whitelist_externals = py.test\n                              xy*\n        commands=\n            py.test\n            xyz\n    ')
    venv = mocksession.getenv('python')
    venv.test()
    mocksession.report.expect('warning', '*test command found but not*', invert=True)
    @py_assert1 = venv.status
    @py_assert4 = 'commands failed'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.skipif("not sys.platform.startswith('linux')")
def test_install_command_not_installed_bash(newmocksession):
    mocksession = newmocksession(['--recreate'], '\n        [testenv]\n        commands=\n            bash\n    ')
    venv = mocksession.getenv('python')
    venv.test()
    mocksession.report.expect('warning', '*test command found but not*')


def test_install_python3(tmpdir, newmocksession):
    if not py.path.local.sysfind('python3.3'):
        pytest.skip('needs python3.3')
    mocksession = newmocksession([], '\n        [testenv:py123]\n        basepython=python3.3\n        deps=\n            dep1\n            dep2\n    ')
    venv = mocksession.getenv('py123')
    venv.create()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = l[0].args
    @py_assert1 = args[2]
    @py_assert3 = str(@py_assert1)
    @py_assert6 = 'virtualenv'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    l[:] = []
    action = mocksession.newaction(venv, 'hello')
    venv._install(['hello'], action=action)
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    args = l[0].args
    @py_assert0 = 'pip'
    @py_assert4 = args[0]
    @py_assert6 = str(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    for x in args:
        @py_assert0 = '--download-cache'
        @py_assert2 = @py_assert0 not in args
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, args)) % {'py3': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = (@pytest_ar._format_assertmsg(args) + '\n>assert %(py5)s') % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


class TestCreationConfig:

    def test_basic(self, newconfig, mocksession, tmpdir):
        config = newconfig([], '')
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        cconfig = venv._getliveconfig()
        @py_assert1 = cconfig.matches
        @py_assert4 = @py_assert1(cconfig)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.matches\n}(%(py3)s)\n}') % {'py3': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py0': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        path = tmpdir.join('configdump')
        cconfig.writeconfig(path)
        newconfig = CreationConfig.readconfig(path)
        @py_assert1 = newconfig.matches
        @py_assert4 = @py_assert1(cconfig)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.matches\n}(%(py3)s)\n}') % {'py3': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py0': @pytest_ar._saferepr(newconfig) if 'newconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(newconfig) else 'newconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        @py_assert1 = cconfig.matches
        @py_assert4 = @py_assert1(newconfig)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.matches\n}(%(py3)s)\n}') % {'py3': @pytest_ar._saferepr(newconfig) if 'newconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(newconfig) else 'newconfig',  'py0': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None

    def test_matchingdependencies(self, newconfig, mocksession):
        config = newconfig([], '\n            [testenv]\n            deps=abc\n        ')
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        cconfig = venv._getliveconfig()
        config = newconfig([], '\n            [testenv]\n            deps=xyz\n        ')
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        otherconfig = venv._getliveconfig()
        @py_assert1 = cconfig.matches
        @py_assert4 = @py_assert1(otherconfig)
        @py_assert6 = not @py_assert4
        if not @py_assert6:
            @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.matches\n}(%(py3)s)\n}') % {'py3': @pytest_ar._saferepr(otherconfig) if 'otherconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(otherconfig) else 'otherconfig',  'py0': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert4 = @py_assert6 = None

    def test_matchingdependencies_file(self, newconfig, mocksession):
        config = newconfig([], '\n            [tox]\n            distshare={toxworkdir}/distshare\n            [testenv]\n            deps=abc\n                 {distshare}/xyz.zip\n        ')
        xyz = config.distshare.join('xyz.zip')
        xyz.ensure()
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        cconfig = venv._getliveconfig()
        @py_assert1 = cconfig.matches
        @py_assert4 = @py_assert1(cconfig)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.matches\n}(%(py3)s)\n}') % {'py3': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py0': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        xyz.write('hello')
        newconfig = venv._getliveconfig()
        @py_assert1 = cconfig.matches
        @py_assert4 = @py_assert1(newconfig)
        @py_assert6 = not @py_assert4
        if not @py_assert6:
            @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.matches\n}(%(py3)s)\n}') % {'py3': @pytest_ar._saferepr(newconfig) if 'newconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(newconfig) else 'newconfig',  'py0': @pytest_ar._saferepr(cconfig) if 'cconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cconfig) else 'cconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert4 = @py_assert6 = None

    def test_matchingdependencies_latest(self, newconfig, mocksession):
        config = newconfig([], '\n            [tox]\n            distshare={toxworkdir}/distshare\n            [testenv]\n            deps={distshare}/xyz-*\n        ')
        config.distshare.ensure('xyz-1.2.0.zip')
        xyz2 = config.distshare.ensure('xyz-1.2.1.zip')
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        cconfig = venv._getliveconfig()
        md5, path = cconfig.deps[0]
        @py_assert1 = path == xyz2
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (path, xyz2)) % {'py0': @pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py2': @pytest_ar._saferepr(xyz2) if 'xyz2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(xyz2) else 'xyz2'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert3 = path.computehash
        @py_assert5 = @py_assert3()
        @py_assert1 = md5 == @py_assert5
        if not @py_assert1:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.computehash\n}()\n}', ), (md5, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(md5) if 'md5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(md5) else 'md5',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    def test_python_recreation(self, tmpdir, newconfig, mocksession):
        pkg = tmpdir.ensure('package.tar.gz')
        config = newconfig([], '')
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        cconfig = venv._getliveconfig()
        venv.update()
        @py_assert1 = venv.path_config
        @py_assert3 = @py_assert1.check
        @py_assert5 = @py_assert3()
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path_config\n}.check\n}()\n}') % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        mocksession.installpkg(venv, pkg)
        @py_assert1 = venv.path_config
        @py_assert3 = @py_assert1.check
        @py_assert5 = @py_assert3()
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path_config\n}.check\n}()\n}') % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = mocksession._pcalls
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s._pcalls\n}') % {'py0': @pytest_ar._saferepr(mocksession) if 'mocksession' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mocksession) else 'mocksession',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
        args1 = map(str, mocksession._pcalls[0].args)
        @py_assert0 = 'virtualenv'
        @py_assert3 = ' '
        @py_assert5 = @py_assert3.join
        @py_assert8 = @py_assert5(args1)
        @py_assert2 = @py_assert0 in @py_assert8
        if not @py_assert2:
            @py_format10 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s.join\n}(%(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(args1) if 'args1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args1) else 'args1'}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert8 = None
        mocksession.report.expect('*', '*create*')
        mocksession._clearmocks()
        venv.update()
        mocksession.report.expect('*', '*reusing*')
        mocksession._clearmocks()
        cconfig.python = py.path.local('balla')
        cconfig.writeconfig(venv.path_config)
        venv.update()
        mocksession.report.expect('verbosity0', '*recreate*')

    def test_dep_recreation(self, newconfig, mocksession):
        config = newconfig([], '')
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        venv.update()
        cconfig = venv._getliveconfig()
        cconfig.deps[:] = [('1' * 32, 'xyz.zip')]
        cconfig.writeconfig(venv.path_config)
        mocksession._clearmocks()
        venv.update()
        mocksession.report.expect('*', '*recreate*')

    def test_develop_recreation(self, newconfig, mocksession):
        config = newconfig([], '')
        envconfig = config.envconfigs['python']
        venv = VirtualEnv(envconfig, session=mocksession)
        venv.update()
        cconfig = venv._getliveconfig()
        cconfig.usedevelop = True
        cconfig.writeconfig(venv.path_config)
        mocksession._clearmocks()
        venv.update()
        mocksession.report.expect('verbosity0', '*recreate*')


class TestVenvTest:

    def test_envbinddir_path(self, newmocksession, monkeypatch):
        monkeypatch.setenv('PIP_RESPECT_VIRTUALENV', '1')
        mocksession = newmocksession([], '\n            [testenv:python]\n            commands=abc\n        ')
        venv = mocksession.getenv('python')
        monkeypatch.setenv('PATH', 'xyz')
        l = []
        monkeypatch.setattr('py.path.local.sysfind', classmethod(lambda *args**args: l.append(kwargs) or 0 / 0))
        py.test.raises(ZeroDivisionError, "venv._install(list('123'))")
        @py_assert0 = l.pop()['paths']
        @py_assert3 = [
         venv.envconfig.envbindir]
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        py.test.raises(ZeroDivisionError, 'venv.test()')
        @py_assert0 = l.pop()['paths']
        @py_assert3 = [
         venv.envconfig.envbindir]
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        py.test.raises(ZeroDivisionError, "venv.run_install_command(['qwe'])")
        @py_assert0 = l.pop()['paths']
        @py_assert3 = [
         venv.envconfig.envbindir]
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        monkeypatch.setenv('PIP_RESPECT_VIRTUALENV', '1')
        monkeypatch.setenv('PIP_REQUIRE_VIRTUALENV', '1')
        monkeypatch.setenv('__PYVENV_LAUNCHER__', '1')
        py.test.raises(ZeroDivisionError, "venv.run_install_command(['qwe'])")
        @py_assert0 = 'PIP_RESPECT_VIRTUALENV'
        @py_assert4 = os.environ
        @py_assert2 = @py_assert0 not in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.environ\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'PIP_REQUIRE_VIRTUALENV'
        @py_assert4 = os.environ
        @py_assert2 = @py_assert0 not in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.environ\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = '__PYVENV_LAUNCHER__'
        @py_assert4 = os.environ
        @py_assert2 = @py_assert0 not in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.environ\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None


def test_env_variables_added_to_pcall(tmpdir, mocksession, newconfig, monkeypatch):
    pkg = tmpdir.ensure('package.tar.gz')
    monkeypatch.setenv('X123', '123')
    monkeypatch.setenv('YY', '456')
    config = newconfig([], '\n        [testenv:python]\n        commands=python -V\n        passenv = x123\n        setenv =\n            ENV_VAR = value\n    ')
    mocksession._clearmocks()
    venv = VirtualEnv(config.envconfigs['python'], session=mocksession)
    mocksession.installpkg(venv, pkg)
    venv.test()
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    for x in l:
        env = x.env
        @py_assert2 = None
        @py_assert1 = env is not @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (env, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        @py_assert0 = 'ENV_VAR'
        @py_assert2 = @py_assert0 in env
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, env)) % {'py3': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = env['ENV_VAR']
        @py_assert3 = 'value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = env['VIRTUAL_ENV']
        @py_assert5 = venv.path
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 == @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.path\n})\n}', ), (@py_assert0, @py_assert7)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py4': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None
        @py_assert0 = env['X123']
        @py_assert3 = '123'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    @py_assert0 = l[0].env['YY']
    @py_assert3 = '456'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'YY'
    @py_assert3 = l[1]
    @py_assert5 = @py_assert3.env
    @py_assert2 = @py_assert0 not in @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.env\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert1 = [
     'ENV_VAR', 'VIRTUAL_ENV', 'PYTHONHASHSEED', 'X123', 'PATH']
    @py_assert3 = set(@py_assert1)
    @py_assert5 = @py_assert3.issubset
    @py_assert7 = l[1]
    @py_assert9 = @py_assert7.env
    @py_assert11 = @py_assert5(@py_assert9)
    if not @py_assert11:
        @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.issubset\n}(%(py10)s\n{%(py10)s = %(py8)s.env\n})\n}') % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py4': @pytest_ar._saferepr(@py_assert3),  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_installpkg_no_upgrade(tmpdir, newmocksession):
    pkg = tmpdir.ensure('package.tar.gz')
    mocksession = newmocksession([], '')
    venv = mocksession.getenv('python')
    venv.just_created = True
    venv.envconfig.envdir.ensure(dir=1)
    mocksession.installpkg(venv, pkg)
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = '-U'
    @py_assert3 = l[0]
    @py_assert5 = @py_assert3.args
    @py_assert2 = @py_assert0 not in @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.args\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None


def test_installpkg_upgrade(newmocksession, tmpdir):
    pkg = tmpdir.ensure('package.tar.gz')
    mocksession = newmocksession([], '')
    venv = mocksession.getenv('python')
    @py_assert2 = 'just_created'
    @py_assert4 = hasattr(venv, @py_assert2)
    @py_assert6 = not @py_assert4
    if not @py_assert6:
        @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr',  'py1': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    mocksession.installpkg(venv, pkg)
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    index = l[0].args.index(str(pkg))
    @py_assert2 = 0
    @py_assert1 = index >= @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert1,), ('%(py0)s >= %(py3)s', ), (index, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(index) if 'index' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(index) else 'index'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = '-U'
    @py_assert3 = l[0].args[:index]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '--no-deps'
    @py_assert3 = l[0].args[:index]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_run_install_command(newmocksession):
    mocksession = newmocksession([], '')
    venv = mocksession.getenv('python')
    venv.just_created = True
    venv.envconfig.envdir.ensure(dir=1)
    action = mocksession.newaction(venv, 'hello')
    venv.run_install_command(packages=['whatever'], action=action)
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'pip'
    @py_assert3 = l[0].args[0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'install'
    @py_assert3 = l[0]
    @py_assert5 = @py_assert3.args
    @py_assert2 = @py_assert0 in @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.args\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    env = l[0].env
    @py_assert2 = None
    @py_assert1 = env is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (env, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_run_custom_install_command(newmocksession):
    mocksession = newmocksession([], '\n        [testenv]\n        install_command=easy_install {opts} {packages}\n    ')
    venv = mocksession.getenv('python')
    venv.just_created = True
    venv.envconfig.envdir.ensure(dir=1)
    action = mocksession.newaction(venv, 'hello')
    venv.run_install_command(packages=['whatever'], action=action)
    l = mocksession._pcalls
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'easy_install'
    @py_assert3 = l[0].args[0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = l[0].args[1:]
    @py_assert3 = [
     'whatever']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_command_relative_issue26(newmocksession, tmpdir, monkeypatch):
    mocksession = newmocksession([], '\n        [testenv]\n    ')
    x = tmpdir.ensure('x')
    venv = mocksession.getenv('python')
    x2 = venv.getcommandpath('./x', cwd=tmpdir)
    @py_assert1 = x == x2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (x, x2)) % {'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x',  'py2': @pytest_ar._saferepr(x2) if 'x2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x2) else 'x2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    mocksession.report.not_expect('warning', '*test command found but not*')
    x3 = venv.getcommandpath('/bin/bash', cwd=tmpdir)
    @py_assert2 = '/bin/bash'
    @py_assert1 = x3 == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x3, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x3) if 'x3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x3) else 'x3'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    mocksession.report.not_expect('warning', '*test command found but not*')
    monkeypatch.setenv('PATH', str(tmpdir))
    x4 = venv.getcommandpath('x', cwd=tmpdir)
    @py_assert1 = x4.endswith
    @py_assert4 = os.sep
    @py_assert6 = 'x'
    @py_assert8 = @py_assert4 + @py_assert6
    @py_assert9 = @py_assert1(@py_assert8)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.endswith\n}((%(py5)s\n{%(py5)s = %(py3)s.sep\n} + %(py7)s))\n}') % {'py3': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py0': @pytest_ar._saferepr(x4) if 'x4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x4) else 'x4',  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    mocksession.report.expect('warning', '*test command found but not*')
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/itxaka/Projects/tox-plus/tests/test_result.py
# Compiled at: 2015-09-01 06:06:20
# Size of source mod 2**32: 2253 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, py
from tox_plus.result import ResultLog
import tox_plus, pytest

@pytest.fixture
def pkg(tmpdir):
    p = tmpdir.join('hello-1.0.tar.gz')
    p.write('whatever')
    return p


def test_pre_set_header(pkg):
    replog = ResultLog()
    d = replog.dict
    @py_assert1 = replog.dict
    @py_assert3 = @py_assert1 == d
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dict\n} == %(py4)s', ), (@py_assert1, d)) % {'py0': @pytest_ar._saferepr(replog) if 'replog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replog) else 'replog',  'py4': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = replog.dict['reportversion']
    @py_assert3 = '1'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = replog.dict['toxversion']
    @py_assert4 = tox_plus.__version__
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.__version__\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tox_plus) if 'tox_plus' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tox_plus) else 'tox_plus',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = replog.dict['platform']
    @py_assert4 = sys.platform
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.platform\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = replog.dict['host']
    @py_assert4 = py.std
    @py_assert6 = @py_assert4.socket
    @py_assert8 = @py_assert6.getfqdn
    @py_assert10 = @py_assert8()
    @py_assert2 = @py_assert0 == @py_assert10
    if not @py_assert2:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.std\n}.socket\n}.getfqdn\n}()\n}', ), (@py_assert0, @py_assert10)) % {'py3': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py1': @pytest_ar._saferepr(@py_assert0),  'py9': @pytest_ar._saferepr(@py_assert8),  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    data = replog.dumps_json()
    replog2 = ResultLog.loads_json(data)
    @py_assert1 = replog2.dict
    @py_assert5 = replog.dict
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dict\n} == %(py6)s\n{%(py6)s = %(py4)s.dict\n}', ), (@py_assert1, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(replog2) if 'replog2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replog2) else 'replog2',  'py4': @pytest_ar._saferepr(replog) if 'replog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replog) else 'replog',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_set_header(pkg):
    replog = ResultLog()
    d = replog.dict
    replog.set_header(installpkg=pkg)
    @py_assert1 = replog.dict
    @py_assert3 = @py_assert1 == d
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dict\n} == %(py4)s', ), (@py_assert1, d)) % {'py0': @pytest_ar._saferepr(replog) if 'replog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replog) else 'replog',  'py4': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = replog.dict['reportversion']
    @py_assert3 = '1'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = replog.dict['toxversion']
    @py_assert4 = tox_plus.__version__
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.__version__\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tox_plus) if 'tox_plus' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tox_plus) else 'tox_plus',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = replog.dict['platform']
    @py_assert4 = sys.platform
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.platform\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = replog.dict['host']
    @py_assert4 = py.std
    @py_assert6 = @py_assert4.socket
    @py_assert8 = @py_assert6.getfqdn
    @py_assert10 = @py_assert8()
    @py_assert2 = @py_assert0 == @py_assert10
    if not @py_assert2:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.std\n}.socket\n}.getfqdn\n}()\n}', ), (@py_assert0, @py_assert10)) % {'py3': @pytest_ar._saferepr(py) if 'py' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py) else 'py',  'py1': @pytest_ar._saferepr(@py_assert0),  'py9': @pytest_ar._saferepr(@py_assert8),  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert0 = replog.dict['installpkg']
    @py_assert3 = {'basename': 'hello-1.0.tar.gz',  'md5': pkg.computehash('md5'),  'sha256': pkg.computehash('sha256')}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    data = replog.dumps_json()
    replog2 = ResultLog.loads_json(data)
    @py_assert1 = replog2.dict
    @py_assert5 = replog.dict
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dict\n} == %(py6)s\n{%(py6)s = %(py4)s.dict\n}', ), (@py_assert1, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(replog2) if 'replog2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replog2) else 'replog2',  'py4': @pytest_ar._saferepr(replog) if 'replog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replog) else 'replog',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_addenv_setpython(pkg):
    replog = ResultLog()
    replog.set_header(installpkg=pkg)
    envlog = replog.get_envlog('py26')
    envlog.set_python_info(py.path.local(sys.executable))
    @py_assert0 = envlog.dict['python']['version_info']
    @py_assert5 = sys.version_info
    @py_assert7 = list(@py_assert5)
    @py_assert2 = @py_assert0 == @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.version_info\n})\n}', ), (@py_assert0, @py_assert7)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py4': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None
    @py_assert0 = envlog.dict['python']['version']
    @py_assert4 = sys.version
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.version\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = envlog.dict['python']['executable']
    @py_assert4 = sys.executable
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.executable\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_get_commandlog(pkg):
    replog = ResultLog()
    replog.set_header(installpkg=pkg)
    envlog = replog.get_envlog('py26')
    @py_assert0 = 'setup'
    @py_assert4 = envlog.dict
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.dict\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envlog) if 'envlog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envlog) else 'envlog',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    setuplog = envlog.get_commandlog('setup')
    setuplog.add_command(['virtualenv', '...'], 'venv created', 0)
    @py_assert1 = setuplog.list
    @py_assert4 = [{'command': ['virtualenv', '...'],  'output': 'venv created',  'retcode': '0'}]
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.list\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(setuplog) if 'setuplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(setuplog) else 'setuplog',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = envlog.dict['setup']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    setuplog2 = replog.get_envlog('py26').get_commandlog('setup')
    @py_assert1 = setuplog2.list
    @py_assert5 = setuplog.list
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.list\n} == %(py6)s\n{%(py6)s = %(py4)s.list\n}', ), (@py_assert1, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(setuplog2) if 'setuplog2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(setuplog2) else 'setuplog2',  'py4': @pytest_ar._saferepr(setuplog) if 'setuplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(setuplog) else 'setuplog',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/itxaka/Projects/tox-plus/tests/test_z_cmdline.py
# Compiled at: 2015-09-01 06:06:20
# Size of source mod 2**32: 21216 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, tox_plus, py, pytest
from tox_plus._pytestplugin import ReportExpectMock
try:
    import json
except ImportError:
    import simplejson as json

pytest_plugins = 'pytester'
from tox_plus.session import Session
from tox_plus.config import parseconfig

def test_report_protocol(newconfig):
    config = newconfig([], '\n            [testenv:mypython]\n            deps=xy\n    ')

    class Popen:

        def __init__(self, *args, **kwargs):
            pass

        def communicate(self):
            return ('', '')

        def wait(self):
            pass

    session = Session(config, popen=Popen, Report=ReportExpectMock)
    report = session.report
    report.expect('using')
    venv = session.getvenv('mypython')
    venv.update()
    report.expect('logpopen')


def test__resolve_pkg(tmpdir, mocksession):
    distshare = tmpdir.join('distshare')
    spec = distshare.join('pkg123-*')
    py.test.raises(tox_plus.exception.MissingDirectory, 'mocksession._resolve_pkg(spec)')
    distshare.ensure(dir=1)
    py.test.raises(tox_plus.exception.MissingDependency, 'mocksession._resolve_pkg(spec)')
    distshare.ensure('pkg123-1.3.5.zip')
    p = distshare.ensure('pkg123-1.4.5.zip')
    mocksession.report.clear()
    result = mocksession._resolve_pkg(spec)
    @py_assert1 = result == p
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, p)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    mocksession.report.expect('info', 'determin*pkg123*')
    distshare.ensure('pkg123-1.4.7dev.zip')
    mocksession._clearmocks()
    result = mocksession._resolve_pkg(spec)
    mocksession.report.expect('warning', '*1.4.7*')
    @py_assert1 = result == p
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, p)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    mocksession._clearmocks()
    distshare.ensure('pkg123-1.4.5a1.tar.gz')
    result = mocksession._resolve_pkg(spec)
    @py_assert1 = result == p
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, p)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test__resolve_pkg_doubledash(tmpdir, mocksession):
    distshare = tmpdir.join('distshare')
    p = distshare.ensure('pkg-mine-1.3.0.zip')
    res = mocksession._resolve_pkg(distshare.join('pkg-mine*'))
    @py_assert1 = res == p
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (res, p)) % {'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res',  'py2': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    distshare.ensure('pkg-mine-1.3.0a1.zip')
    res = mocksession._resolve_pkg(distshare.join('pkg-mine*'))
    @py_assert1 = res == p
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (res, p)) % {'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res',  'py2': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


class TestSession:

    def test_make_sdist(self, initproj):
        initproj('example123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            '})
        config = parseconfig([])
        session = Session(config)
        sdist = session.get_installpkg_path()
        @py_assert1 = sdist.check
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.check\n}()\n}') % {'py0': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = sdist.ext
        @py_assert4 = '.zip'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ext\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert3 = config.distdir
        @py_assert5 = @py_assert3.join
        @py_assert8 = sdist.basename
        @py_assert10 = @py_assert5(@py_assert8)
        @py_assert1 = sdist == @py_assert10
        if not @py_assert1:
            @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.distdir\n}.join\n}(%(py9)s\n{%(py9)s = %(py7)s.basename\n})\n}',), (sdist, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py4': @pytest_ar._saferepr(@py_assert3),  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py11': @pytest_ar._saferepr(@py_assert10),  'py7': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist'}
            @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
        sdist2 = session.get_installpkg_path()
        @py_assert1 = sdist2 == sdist
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py2)s',), (sdist2, sdist)) % {'py0': @pytest_ar._saferepr(sdist2) if 'sdist2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist2) else 'sdist2',  'py2': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist'}
            @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        sdist.write('hello')
        @py_assert1 = sdist.stat
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.size
        @py_assert8 = 10
        @py_assert7 = @py_assert5 < @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('<',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.size\n} < %(py9)s',), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        sdist_new = Session(config).get_installpkg_path()
        @py_assert1 = sdist_new == sdist
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py2)s',), (sdist_new, sdist)) % {'py0': @pytest_ar._saferepr(sdist_new) if 'sdist_new' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist_new) else 'sdist_new',  'py2': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist'}
            @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = sdist_new.stat
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.size
        @py_assert8 = 10
        @py_assert7 = @py_assert5 > @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('>',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.size\n} > %(py9)s',), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(sdist_new) if 'sdist_new' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist_new) else 'sdist_new',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None

    def test_make_sdist_distshare(self, tmpdir, initproj):
        distshare = tmpdir.join('distshare')
        initproj('example123-0.6', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [tox]\n            distshare=%s\n            ' % distshare})
        config = parseconfig([])
        session = Session(config)
        sdist = session.get_installpkg_path()
        @py_assert1 = sdist.check
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.check\n}()\n}') % {'py0': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = sdist.ext
        @py_assert4 = '.zip'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ext\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert3 = config.distdir
        @py_assert5 = @py_assert3.join
        @py_assert8 = sdist.basename
        @py_assert10 = @py_assert5(@py_assert8)
        @py_assert1 = sdist == @py_assert10
        if not @py_assert1:
            @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.distdir\n}.join\n}(%(py9)s\n{%(py9)s = %(py7)s.basename\n})\n}',), (sdist, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py4': @pytest_ar._saferepr(@py_assert3),  'py9': @pytest_ar._saferepr(@py_assert8),  'py2': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py11': @pytest_ar._saferepr(@py_assert10),  'py7': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist'}
            @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
        sdist_share = config.distshare.join(sdist.basename)
        @py_assert1 = sdist_share.check
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.check\n}()\n}') % {'py0': @pytest_ar._saferepr(sdist_share) if 'sdist_share' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist_share) else 'sdist_share',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = sdist_share.read
        @py_assert3 = 'rb'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert9 = sdist.read
        @py_assert11 = 'rb'
        @py_assert13 = @py_assert9(@py_assert11)
        @py_assert7 = @py_assert5 == @py_assert13
        if not @py_assert7:
            @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}(%(py4)s)\n} == %(py14)s\n{%(py14)s = %(py10)s\n{%(py10)s = %(py8)s.read\n}(%(py12)s)\n}',), (@py_assert5, @py_assert13)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(sdist_share) if 'sdist_share' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist_share) else 'sdist_share',  'py4': @pytest_ar._saferepr(@py_assert3),  'py14': @pytest_ar._saferepr(@py_assert13),  'py8': @pytest_ar._saferepr(sdist) if 'sdist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist) else 'sdist',  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format17 = (@pytest_ar._format_assertmsg((sdist_share, sdist)) + '\n>assert %(py16)s') % {'py16': @py_format15}
            raise AssertionError(@pytest_ar._format_explanation(@py_format17))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None

    def test_log_pcall(self, mocksession):
        mocksession.config.logdir.ensure(dir=1)
        @py_assert1 = mocksession.config
        @py_assert3 = @py_assert1.logdir
        @py_assert5 = @py_assert3.listdir
        @py_assert7 = @py_assert5()
        @py_assert9 = not @py_assert7
        if not @py_assert9:
            @py_format10 = ('' + 'assert not %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.config\n}.logdir\n}.listdir\n}()\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(mocksession) if 'mocksession' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mocksession) else 'mocksession',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        action = mocksession.newaction(None, 'something')
        action.popen(['echo'])
        match = mocksession.report.getnext('logpopen')
        @py_assert0 = match[1]
        @py_assert2 = @py_assert0.outpath
        @py_assert4 = @py_assert2.relto
        @py_assert7 = mocksession.config
        @py_assert9 = @py_assert7.logdir
        @py_assert11 = @py_assert4(@py_assert9)
        if not @py_assert11:
            @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.outpath\n}.relto\n}(%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.config\n}.logdir\n})\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(mocksession) if 'mocksession' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mocksession) else 'mocksession',  'py1': @pytest_ar._saferepr(@py_assert0),  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py5': @pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None
        @py_assert0 = match[1]
        @py_assert2 = @py_assert0.shell
        @py_assert5 = False
        @py_assert4 = @py_assert2 is @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.shell\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None

    def test_summary_status(self, initproj, capfd):
        initproj('logexample123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [testenv:hello]\n            [testenv:world]\n            '})
        config = parseconfig([])
        session = Session(config)
        envs = session.venvlist
        @py_assert2 = len(envs)
        @py_assert5 = 2
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(envs) if 'envs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envs) else 'envs'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        env1, env2 = envs
        env1.status = 'FAIL XYZ'
        @py_assert1 = env1.status
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.status\n}') % {'py0': @pytest_ar._saferepr(env1) if 'env1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env1) else 'env1',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
        env2.status = 0
        @py_assert1 = env2.status
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.status\n}') % {'py0': @pytest_ar._saferepr(env2) if 'env2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env2) else 'env2',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        session._summary()
        out, err = capfd.readouterr()
        exp = '%s: FAIL XYZ' % env1.envconfig.envname
        @py_assert1 = exp in out
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (exp, out)) % {'py0': @pytest_ar._saferepr(exp) if 'exp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exp) else 'exp',  'py2': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        exp = '%s: commands succeeded' % env2.envconfig.envname
        @py_assert1 = exp in out
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (exp, out)) % {'py0': @pytest_ar._saferepr(exp) if 'exp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exp) else 'exp',  'py2': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_getvenv(self, initproj, capfd):
        initproj('logexample123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [testenv:hello]\n            [testenv:world]\n            '})
        config = parseconfig([])
        session = Session(config)
        venv1 = session.getvenv('hello')
        venv2 = session.getvenv('hello')
        @py_assert1 = venv1 is venv2
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (venv1, venv2)) % {'py0': @pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py2': @pytest_ar._saferepr(venv2) if 'venv2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv2) else 'venv2'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        venv1 = session.getvenv('world')
        venv2 = session.getvenv('world')
        @py_assert1 = venv1 is venv2
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (venv1, venv2)) % {'py0': @pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py2': @pytest_ar._saferepr(venv2) if 'venv2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv2) else 'venv2'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        pytest.raises(LookupError, lambda : session.getvenv('qwe'))


def XXX_test_package(cmd, initproj):
    initproj('myproj-0.6', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'MANIFEST.in': '\n            include doc\n            include myproj\n            ', 
     'tox.ini': ''})
    result = cmd.run('tox-plus', 'package')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*created sdist package at*'])


def test_minversion(cmd, initproj):
    initproj('interp123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [tox]\n            minversion = 6.0\n        '})
    result = cmd.run('tox-plus', '-v')
    result.stdout.fnmatch_lines([
     '*ERROR*tox version is * required is at least 6.0*'])
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


def test_run_custom_install_command_error(cmd, initproj):
    initproj('interp123-0.5', filedefs={'tox.ini': '\n            [testenv]\n            install_command=./tox.ini {opts} {packages}\n        '})
    result = cmd.run('tox-plus')
    result.stdout.fnmatch_lines([
     "ERROR: invocation failed (errno *), args: ['*/tox.ini*"])
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


def test_unknown_interpreter_and_env(cmd, initproj):
    initproj('interp123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [testenv:python]\n            basepython=xyz_unknown_interpreter\n            [testenv]\n            changedir=tests\n        '})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*ERROR*InterpreterNotFound*xyz_unknown_interpreter*'])
    result = cmd.run('tox-plus', '-exyz')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*ERROR*unknown*'])


def test_unknown_interpreter(cmd, initproj):
    initproj('interp123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [testenv:python]\n            basepython=xyz_unknown_interpreter\n            [testenv]\n            changedir=tests\n        '})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*ERROR*InterpreterNotFound*xyz_unknown_interpreter*'])


def test_skip_platform_mismatch(cmd, initproj):
    initproj('interp123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [testenv]\n            changedir=tests\n            platform=x123\n        '})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines('\n        SKIPPED*platform mismatch*\n    ')


def test_skip_unknown_interpreter(cmd, initproj):
    initproj('interp123-0.5', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [testenv:python]\n            basepython=xyz_unknown_interpreter\n            [testenv]\n            changedir=tests\n        '})
    result = cmd.run('tox-plus', '--skip-missing-interpreters')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*SKIPPED*InterpreterNotFound*xyz_unknown_interpreter*'])


def test_unknown_dep(cmd, initproj):
    initproj('dep123-0.7', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'tox.ini': '\n            [testenv]\n            deps=qweqwe123\n            changedir=tests\n        '})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*ERROR*could not install*qweqwe123*'])


def test_unknown_environment(cmd, initproj):
    initproj('env123-0.7', filedefs={'tox.ini': ''})
    result = cmd.run('tox-plus', '-e', 'qpwoei')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*ERROR*unknown*environment*qpwoei*'])


def test_skip_sdist(cmd, initproj):
    initproj('pkg123-0.7', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'setup.py': '\n            syntax error\n        ', 
     'tox.ini': '\n            [tox]\n            skipsdist=True\n            [testenv]\n            commands=python -c "print(\'done\')"\n        '})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_minimal_setup_py_empty(cmd, initproj):
    initproj('pkg123-0.7', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'setup.py': '\n        ', 
     'tox.ini': ''})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    result.stdout.fnmatch_lines([
     '*ERROR*empty*'])


def test_minimal_setup_py_comment_only(cmd, initproj):
    initproj('pkg123-0.7', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'setup.py': '\n# some comment\n\n        ', 
     'tox.ini': ''})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    result.stdout.fnmatch_lines([
     '*ERROR*empty*'])


def test_minimal_setup_py_non_functional(cmd, initproj):
    initproj('pkg123-0.7', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'setup.py': '\n        import sys\n\n        ', 
     'tox.ini': ''})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    result.stdout.fnmatch_lines([
     '*ERROR*check setup.py*'])


def test_sdist_fails(cmd, initproj):
    initproj('pkg123-0.7', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'setup.py': '\n            syntax error\n        ', 
     'tox.ini': ''})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*FAIL*could not package project*'])


def test_package_install_fails(cmd, initproj):
    initproj('pkg123-0.7', filedefs={'tests': {'test_hello.py': 'def test_hello(): pass'},  'setup.py': "\n            from setuptools import setup\n            setup(\n                name='pkg123',\n                description='pkg123 project',\n                version='0.7',\n                license='MIT',\n                platforms=['unix', 'win32'],\n                packages=['pkg123',],\n                install_requires=['qweqwe123'],\n                )\n            ", 
     'tox.ini': ''})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*InvocationError*'])


class TestToxRun:

    @pytest.fixture
    def example123(self, initproj):
        initproj('example123-0.5', filedefs={'tests': {'test_hello.py': '\n                    def test_hello(pytestconfig):\n                        pass\n                '}, 
         'tox.ini': '\n                [testenv]\n                changedir=tests\n                commands= py.test --basetemp={envtmpdir}                                   --junitxml=junit-{envname}.xml\n                deps=pytest\n            '})

    def test_toxuone_env(self, cmd, example123):
        result = cmd.run('tox-plus')
        @py_assert1 = result.ret
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        result.stdout.fnmatch_lines([
         '*junit-python.xml*',
         '*1 passed*'])
        result = cmd.run('tox-plus', '-epython')
        @py_assert1 = result.ret
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        result.stdout.fnmatch_lines([
         '*1 passed*',
         '*summary*',
         '*python: commands succeeded'])

    def test_different_config_cwd(self, cmd, example123, monkeypatch):
        monkeypatch.chdir(cmd.tmpdir)
        result = cmd.run('tox-plus', '-c', 'example123/tox.ini')
        @py_assert1 = result.ret
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        result.stdout.fnmatch_lines([
         '*1 passed*',
         '*summary*',
         '*python: commands succeeded'])

    def test_json(self, cmd, example123):
        testfile = py.path.local('tests').join('test_hello.py')
        @py_assert1 = testfile.check
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.check\n}()\n}') % {'py0': @pytest_ar._saferepr(testfile) if 'testfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(testfile) else 'testfile',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        testfile.write('def test_fail(): assert 0')
        jsonpath = cmd.tmpdir.join('res.json')
        result = cmd.run('tox-plus', '--result-json', jsonpath)
        @py_assert1 = result.ret
        @py_assert4 = 1
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        data = json.load(jsonpath.open('r'))
        verify_json_report_format(data)
        result.stdout.fnmatch_lines([
         '*1 failed*',
         '*summary*',
         '*python: *failed*'])


def test_develop(initproj, cmd):
    initproj('example123', filedefs={'tox.ini': '\n    '})
    result = cmd.run('tox-plus', '-vv', '--develop')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'sdist-make'
    @py_assert4 = result.stdout
    @py_assert6 = @py_assert4.str
    @py_assert8 = @py_assert6()
    @py_assert2 = @py_assert0 not in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.stdout\n}.str\n}()\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py9': @pytest_ar._saferepr(@py_assert8),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_usedevelop(initproj, cmd):
    initproj('example123', filedefs={'tox.ini': '\n            [testenv]\n            usedevelop=True\n    '})
    result = cmd.run('tox-plus', '-vv')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'sdist-make'
    @py_assert4 = result.stdout
    @py_assert6 = @py_assert4.str
    @py_assert8 = @py_assert6()
    @py_assert2 = @py_assert0 not in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.stdout\n}.str\n}()\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py9': @pytest_ar._saferepr(@py_assert8),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_usedevelop_mixed(initproj, cmd):
    initproj('example123', filedefs={'tox.ini': '\n            [testenv:devenv]\n            usedevelop=True\n            [testenv:nondev]\n            usedevelop=False\n    '})
    result = cmd.run('tox-plus', '-vv', '-e', 'devenv')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'sdist-make'
    @py_assert4 = result.stdout
    @py_assert6 = @py_assert4.str
    @py_assert8 = @py_assert6()
    @py_assert2 = @py_assert0 not in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.stdout\n}.str\n}()\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py9': @pytest_ar._saferepr(@py_assert8),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    result = cmd.run('tox-plus', '-vv')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'sdist-make'
    @py_assert4 = result.stdout
    @py_assert6 = @py_assert4.str
    @py_assert8 = @py_assert6()
    @py_assert2 = @py_assert0 in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.stdout\n}.str\n}()\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py9': @pytest_ar._saferepr(@py_assert8),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_test_usedevelop(cmd, initproj):
    initproj('example123-0.5', filedefs={'tests': {'test_hello.py': '\n                def test_hello(pytestconfig):\n                    pass\n            '}, 
     'tox.ini': '\n            [testenv]\n            usedevelop=True\n            changedir=tests\n            commands=\n                py.test --basetemp={envtmpdir} --junitxml=junit-{envname}.xml []\n            deps=pytest\n        '})
    result = cmd.run('tox-plus', '-v')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*junit-python.xml*',
     '*1 passed*'])
    @py_assert0 = 'sdist-make'
    @py_assert4 = result.stdout
    @py_assert6 = @py_assert4.str
    @py_assert8 = @py_assert6()
    @py_assert2 = @py_assert0 not in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.stdout\n}.str\n}()\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py9': @pytest_ar._saferepr(@py_assert8),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    result = cmd.run('tox-plus', '-epython')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*1 passed*',
     '*summary*',
     '*python: commands succeeded'])
    old = cmd.tmpdir.chdir()
    result = cmd.run('tox-plus', '-c', 'example123/tox.ini')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*1 passed*',
     '*summary*',
     '*python: commands succeeded'])
    old.chdir()
    testfile = py.path.local('tests').join('test_hello.py')
    @py_assert1 = testfile.check
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.check\n}()\n}') % {'py0': @pytest_ar._saferepr(testfile) if 'testfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(testfile) else 'testfile',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    testfile.write('def test_fail(): assert 0')
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    result.stdout.fnmatch_lines([
     '*1 failed*',
     '*summary*',
     '*python: *failed*'])


def test_test_piphelp(initproj, cmd):
    initproj('example123', filedefs={'tox.ini': '\n        # content of: tox.ini\n        [testenv]\n        commands=pip -h\n        [testenv:py26]\n        basepython=python\n        [testenv:py27]\n        basepython=python\n    '})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


def test_notest(initproj, cmd):
    initproj('example123', filedefs={'tox.ini': '\n        # content of: tox.ini\n        [testenv:py26]\n        basepython=python\n    '})
    result = cmd.run('tox-plus', '-v', '--notest')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*summary*',
     '*py26*skipped tests*'])
    result = cmd.run('tox-plus', '-v', '--notest', '-epy26')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*py26*reusing*'])


def test_PYC(initproj, cmd, monkeypatch):
    initproj('example123', filedefs={'tox.ini': ''})
    monkeypatch.setenv('PYTHONDOWNWRITEBYTECODE', 1)
    result = cmd.run('tox-plus', '-v', '--notest')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*create*'])


def test_env_VIRTUALENV_PYTHON(initproj, cmd, monkeypatch):
    initproj('example123', filedefs={'tox.ini': ''})
    monkeypatch.setenv('VIRTUALENV_PYTHON', '/FOO')
    result = cmd.run('tox-plus', '-v', '--notest')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = (@pytest_ar._format_assertmsg(result.stdout.lines) + '\n>assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*create*'])


def test_sdistonly(initproj, cmd):
    initproj('example123', filedefs={'tox.ini': '\n    '})
    result = cmd.run('tox-plus', '-v', '--sdistonly')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*sdist-make*setup.py*'])
    @py_assert0 = '-mvirtualenv'
    @py_assert4 = result.stdout
    @py_assert6 = @py_assert4.str
    @py_assert8 = @py_assert6()
    @py_assert2 = @py_assert0 not in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.stdout\n}.str\n}()\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py9': @pytest_ar._saferepr(@py_assert8),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_separate_sdist_no_sdistfile(cmd, initproj):
    distshare = cmd.tmpdir.join('distshare')
    initproj(('pkg123-foo', '0.7'), filedefs={'tox.ini': '\n            [tox]\n            distshare=%s\n        ' % distshare})
    result = cmd.run('tox-plus', '--sdistonly')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    l = distshare.listdir()
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    sdistfile = l[0]
    @py_assert0 = 'pkg123-foo-0.7.zip'
    @py_assert5 = str(sdistfile)
    @py_assert2 = @py_assert0 in @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(sdistfile) if 'sdistfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdistfile) else 'sdistfile',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None


def test_separate_sdist(cmd, initproj):
    distshare = cmd.tmpdir.join('distshare')
    initproj('pkg123-0.7', filedefs={'tox.ini': '\n            [tox]\n            distshare=%s\n            sdistsrc={distshare}/pkg123-0.7.zip\n        ' % distshare})
    result = cmd.run('tox-plus', '--sdistonly')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    l = distshare.listdir()
    @py_assert2 = len(l)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    sdistfile = l[0]
    result = cmd.run('tox-plus', '-v', '--notest')
    @py_assert1 = result.ret
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    result.stdout.fnmatch_lines([
     '*inst*%s*' % sdistfile])


def test_sdist_latest(tmpdir, newconfig):
    distshare = tmpdir.join('distshare')
    config = newconfig([], '\n            [tox]\n            distshare=%s\n            sdistsrc={distshare}/pkg123-*\n    ' % distshare)
    p = distshare.ensure('pkg123-1.4.5.zip')
    distshare.ensure('pkg123-1.4.5a1.zip')
    session = Session(config)
    sdist_path = session.get_installpkg_path()
    @py_assert1 = sdist_path == p
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (sdist_path, p)) % {'py0': @pytest_ar._saferepr(sdist_path) if 'sdist_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist_path) else 'sdist_path',  'py2': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_installpkg(tmpdir, newconfig):
    p = tmpdir.ensure('pkg123-1.0.zip')
    config = newconfig(['--installpkg=%s' % p], '')
    session = Session(config)
    sdist_path = session.get_installpkg_path()
    @py_assert1 = sdist_path == p
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (sdist_path, p)) % {'py0': @pytest_ar._saferepr(sdist_path) if 'sdist_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sdist_path) else 'sdist_path',  'py2': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


@pytest.mark.xfail("sys.platform == 'win32' and sys.version_info < (2,6)", reason='test needs better impl')
def test_envsitepackagesdir(cmd, initproj):
    initproj('pkg512-0.0.5', filedefs={'tox.ini': '\n        [testenv]\n        commands=\n            python -c "print(r\'X:{envsitepackagesdir}\')"\n    '})
    result = cmd.run('tox-plus')
    @py_assert1 = result.ret
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    result.stdout.fnmatch_lines('\n        X:*tox*site-packages*\n    ')


def verify_json_report_format(data, testenvs=True):
    @py_assert0 = data['reportversion']
    @py_assert3 = '1'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = data['toxversion']
    @py_assert4 = tox_plus.__version__
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.__version__\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tox_plus) if 'tox_plus' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tox_plus) else 'tox_plus',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    if testenvs:
        for envname, envdata in data['testenvs'].items():
            for commandtype in ('setup', 'test'):
                if commandtype not in envdata:
                    continue
                for command in envdata[commandtype]:
                    @py_assert0 = command['output']
                    if not @py_assert0:
                        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
                        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
                    @py_assert0 = None
                    @py_assert0 = command['retcode']
                    if not @py_assert0:
                        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
                        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
                    @py_assert0 = None

            if envname != 'GLOB':
                @py_assert1 = envdata['installed_packages']
                @py_assert4 = isinstance(@py_assert1, list)
                if not @py_assert4:
                    @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert1 = @py_assert4 = None
                pyinfo = envdata['python']
                @py_assert1 = pyinfo['version_info']
                @py_assert4 = isinstance(@py_assert1, list)
                if not @py_assert4:
                    @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert1 = @py_assert4 = None
                @py_assert0 = pyinfo['version']
                if not @py_assert0:
                    @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format2))
                @py_assert0 = None
                @py_assert0 = pyinfo['executable']
                if not @py_assert0:
                    @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format2))
                @py_assert0 = None
                continue
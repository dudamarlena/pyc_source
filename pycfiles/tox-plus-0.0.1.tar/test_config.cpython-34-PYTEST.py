# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/itxaka/Projects/tox-plus/tests/test_config.py
# Compiled at: 2015-09-01 06:06:20
# Size of source mod 2**32: 61468 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys
from textwrap import dedent
import py, pytest, tox_plus, tox_plus.config
from tox_plus.config import *
from tox_plus.venv import VirtualEnv

class TestVenvConfig:

    def test_config_parsing_minimal(self, tmpdir, newconfig):
        config = newconfig([], '\n            [testenv:py1]\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s',), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = config.toxworkdir
        @py_assert3 = @py_assert1.realpath
        @py_assert5 = @py_assert3()
        @py_assert9 = tmpdir.join
        @py_assert11 = '.tox'
        @py_assert13 = @py_assert9(@py_assert11)
        @py_assert15 = @py_assert13.realpath
        @py_assert17 = @py_assert15()
        @py_assert7 = @py_assert5 == @py_assert17
        if not @py_assert7:
            @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.toxworkdir\n}.realpath\n}()\n} == %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py10)s\n{%(py10)s = %(py8)s.join\n}(%(py12)s)\n}.realpath\n}()\n}',), (@py_assert5, @py_assert17)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py18': @pytest_ar._saferepr(@py_assert17),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py14': @pytest_ar._saferepr(@py_assert13),  'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py16': @pytest_ar._saferepr(@py_assert15),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
            raise AssertionError(@pytest_ar._format_explanation(@py_format21))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
        @py_assert0 = config.envconfigs['py1']
        @py_assert2 = @py_assert0.basepython
        @py_assert6 = sys.executable
        @py_assert4 = @py_assert2 == @py_assert6
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.basepython\n} == %(py7)s\n{%(py7)s = %(py5)s.executable\n}',), (@py_assert2, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = config.envconfigs['py1']
        @py_assert2 = @py_assert0.deps
        @py_assert5 = []
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.deps\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = config.envconfigs['py1']
        @py_assert2 = @py_assert0.platform
        @py_assert5 = '.*'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.platform\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None

    def test_config_parsing_multienv(self, tmpdir, newconfig):
        config = newconfig([], '\n            [tox]\n            toxworkdir = %s\n            indexserver =\n                xyz = xyz_repo\n            [testenv:py1]\n            deps=hello\n            [testenv:py2]\n            deps=\n                world1\n                :xyz:http://hello/world\n        ' % (tmpdir,))
        @py_assert1 = config.toxworkdir
        @py_assert3 = @py_assert1 == tmpdir
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.toxworkdir\n} == %(py4)s', ), (@py_assert1, tmpdir)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert0 = config.envconfigs['py1']
        @py_assert2 = @py_assert0.envdir
        @py_assert6 = tmpdir.join
        @py_assert8 = 'py1'
        @py_assert10 = @py_assert6(@py_assert8)
        @py_assert4 = @py_assert2 == @py_assert10
        if not @py_assert4:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.envdir\n} == %(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.join\n}(%(py9)s)\n}', ), (@py_assert2, @py_assert10)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py9': @pytest_ar._saferepr(@py_assert8),  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
        dep = config.envconfigs['py1'].deps[0]
        @py_assert1 = dep.name
        @py_assert4 = 'hello'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(dep) if 'dep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dep) else 'dep',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = dep.indexserver
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.indexserver\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(dep) if 'dep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dep) else 'dep',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert0 = config.envconfigs['py2']
        @py_assert2 = @py_assert0.envdir
        @py_assert6 = tmpdir.join
        @py_assert8 = 'py2'
        @py_assert10 = @py_assert6(@py_assert8)
        @py_assert4 = @py_assert2 == @py_assert10
        if not @py_assert4:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.envdir\n} == %(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.join\n}(%(py9)s)\n}', ), (@py_assert2, @py_assert10)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py9': @pytest_ar._saferepr(@py_assert8),  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
        dep1, dep2 = config.envconfigs['py2'].deps
        @py_assert1 = dep1.name
        @py_assert4 = 'world1'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(dep1) if 'dep1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dep1) else 'dep1',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = dep2.name
        @py_assert4 = 'http://hello/world'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(dep2) if 'dep2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dep2) else 'dep2',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = dep2.indexserver
        @py_assert3 = @py_assert1.name
        @py_assert6 = 'xyz'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.indexserver\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(dep2) if 'dep2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dep2) else 'dep2',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = dep2.indexserver
        @py_assert3 = @py_assert1.url
        @py_assert6 = 'xyz_repo'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.indexserver\n}.url\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(dep2) if 'dep2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dep2) else 'dep2',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_envdir_set_manually(self, tmpdir, newconfig):
        config = newconfig([], '\n            [testenv:devenv]\n            envdir = devenv\n        ')
        envconfig = config.envconfigs['devenv']
        @py_assert1 = envconfig.envdir
        @py_assert5 = tmpdir.join
        @py_assert7 = 'devenv'
        @py_assert9 = @py_assert5(@py_assert7)
        @py_assert3 = @py_assert1 == @py_assert9
        if not @py_assert3:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envdir\n} == %(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s.join\n}(%(py8)s)\n}', ), (@py_assert1, @py_assert9)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py8': @pytest_ar._saferepr(@py_assert7),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None

    def test_envdir_set_manually_with_substitutions(self, tmpdir, newconfig):
        config = newconfig([], '\n            [testenv:devenv]\n            envdir = {toxworkdir}/foobar\n        ')
        envconfig = config.envconfigs['devenv']
        @py_assert1 = envconfig.envdir
        @py_assert5 = config.toxworkdir
        @py_assert7 = @py_assert5.join
        @py_assert9 = 'foobar'
        @py_assert11 = @py_assert7(@py_assert9)
        @py_assert3 = @py_assert1 == @py_assert11
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envdir\n} == %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.toxworkdir\n}.join\n}(%(py10)s)\n}', ), (@py_assert1, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None

    def test_force_dep_version(self, initproj):
        """
        Make sure we can override dependencies configured in tox.ini when using the command line
        option --force-dep.
        """
        initproj('example123-0.5', filedefs={'tox.ini': '\n            [tox]\n\n            [testenv]\n            deps=\n                dep1==1.0\n                dep2>=2.0\n                dep3\n                dep4==4.0\n            '})
        config = parseconfig([
         '--force-dep=dep1==1.5', '--force-dep=dep2==2.1',
         '--force-dep=dep3==3.0'])
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.force_dep
        @py_assert6 = [
         'dep1==1.5', 'dep2==2.1', 'dep3==3.0']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.force_dep\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert0 = [str(x) for x in config.envconfigs['python'].deps]
        @py_assert3 = [
         'dep1==1.5', 'dep2==2.1', 'dep3==3.0', 'dep4==4.0']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_is_same_dep(self):
        """
        Ensure correct parseini._is_same_dep is working with a few samples.
        """
        @py_assert1 = DepOption._is_same_dep
        @py_assert3 = 'pkg_hello-world3==1.0'
        @py_assert5 = 'pkg_hello-world3'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._is_same_dep\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(DepOption) if 'DepOption' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DepOption) else 'DepOption',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DepOption._is_same_dep
        @py_assert3 = 'pkg_hello-world3==1.0'
        @py_assert5 = 'pkg_hello-world3>=2.0'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._is_same_dep\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(DepOption) if 'DepOption' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DepOption) else 'DepOption',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DepOption._is_same_dep
        @py_assert3 = 'pkg_hello-world3==1.0'
        @py_assert5 = 'pkg_hello-world3>2.0'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._is_same_dep\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(DepOption) if 'DepOption' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DepOption) else 'DepOption',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DepOption._is_same_dep
        @py_assert3 = 'pkg_hello-world3==1.0'
        @py_assert5 = 'pkg_hello-world3<2.0'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._is_same_dep\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(DepOption) if 'DepOption' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DepOption) else 'DepOption',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DepOption._is_same_dep
        @py_assert3 = 'pkg_hello-world3==1.0'
        @py_assert5 = 'pkg_hello-world3<=2.0'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._is_same_dep\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(DepOption) if 'DepOption' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DepOption) else 'DepOption',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DepOption._is_same_dep
        @py_assert3 = 'pkg_hello-world3==1.0'
        @py_assert5 = 'otherpkg>=2.0'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if not @py_assert9:
            @py_format10 = ('' + 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._is_same_dep\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(DepOption) if 'DepOption' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DepOption) else 'DepOption',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


class TestConfigPlatform:

    def test_config_parse_platform(self, newconfig):
        config = newconfig([], '\n            [testenv:py1]\n            platform = linux2\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert0 = config.envconfigs['py1']
        @py_assert2 = @py_assert0.platform
        @py_assert5 = 'linux2'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.platform\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None

    def test_config_parse_platform_rex(self, newconfig, mocksession, monkeypatch):
        config = newconfig([], '\n            [testenv:py1]\n            platform = a123|b123\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['py1']
        venv = VirtualEnv(envconfig, session=mocksession)
        @py_assert1 = venv.matching_platform
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.matching_platform\n}()\n}') % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        monkeypatch.setattr(sys, 'platform', 'a123')
        @py_assert1 = venv.matching_platform
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.matching_platform\n}()\n}') % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        monkeypatch.setattr(sys, 'platform', 'b123')
        @py_assert1 = venv.matching_platform
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.matching_platform\n}()\n}') % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        monkeypatch.undo()
        @py_assert1 = venv.matching_platform
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.matching_platform\n}()\n}') % {'py0': @pytest_ar._saferepr(venv) if 'venv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv) else 'venv',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    @pytest.mark.parametrize('plat', ['win', 'lin'])
    def test_config_parse_platform_with_factors(self, newconfig, plat, monkeypatch):
        monkeypatch.setattr(sys, 'platform', 'win32')
        config = newconfig([], '\n            [tox]\n            envlist = py27-{win,lin,osx}\n            [testenv]\n            platform =\n                win: win32\n                lin: linux2\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 3
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        platform = config.envconfigs[('py27-' + plat)].platform
        expected = {'win': 'win32',  'lin': 'linux2'}.get(plat)
        @py_assert1 = platform == expected
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (platform, expected)) % {'py0': @pytest_ar._saferepr(platform) if 'platform' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(platform) else 'platform',  'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


class TestConfigPackage:

    def test_defaults(self, tmpdir, newconfig):
        config = newconfig([], '')
        @py_assert1 = config.setupdir
        @py_assert3 = @py_assert1.realpath
        @py_assert5 = @py_assert3()
        @py_assert9 = tmpdir.realpath
        @py_assert11 = @py_assert9()
        @py_assert7 = @py_assert5 == @py_assert11
        if not @py_assert7:
            @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.setupdir\n}.realpath\n}()\n} == %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.realpath\n}()\n}',), (@py_assert5, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
        @py_assert1 = config.toxworkdir
        @py_assert3 = @py_assert1.realpath
        @py_assert5 = @py_assert3()
        @py_assert9 = tmpdir.join
        @py_assert11 = '.tox'
        @py_assert13 = @py_assert9(@py_assert11)
        @py_assert15 = @py_assert13.realpath
        @py_assert17 = @py_assert15()
        @py_assert7 = @py_assert5 == @py_assert17
        if not @py_assert7:
            @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.toxworkdir\n}.realpath\n}()\n} == %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py10)s\n{%(py10)s = %(py8)s.join\n}(%(py12)s)\n}.realpath\n}()\n}',), (@py_assert5, @py_assert17)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py18': @pytest_ar._saferepr(@py_assert17),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py14': @pytest_ar._saferepr(@py_assert13),  'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py16': @pytest_ar._saferepr(@py_assert15),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
            raise AssertionError(@pytest_ar._format_explanation(@py_format21))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.args_are_paths
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.args_are_paths\n}') % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
        @py_assert1 = envconfig.recreate
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.recreate\n}') % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = envconfig.pip_pre
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.pip_pre\n}') % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None

    def test_defaults_distshare(self, tmpdir, newconfig):
        config = newconfig([], '')
        @py_assert1 = config.distshare
        @py_assert5 = config.homedir
        @py_assert7 = @py_assert5.join
        @py_assert9 = '.tox'
        @py_assert11 = 'distshare'
        @py_assert13 = @py_assert7(@py_assert9, @py_assert11)
        @py_assert3 = @py_assert1 == @py_assert13
        if not @py_assert3:
            @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.distshare\n} == %(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.homedir\n}.join\n}(%(py10)s, %(py12)s)\n}', ), (@py_assert1, @py_assert13)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py14': @pytest_ar._saferepr(@py_assert13),  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
            raise AssertionError(@pytest_ar._format_explanation(@py_format17))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None

    def test_defaults_changed_dir(self, tmpdir, newconfig):
        tmpdir.mkdir('abc').chdir()
        config = newconfig([], '')
        @py_assert1 = config.setupdir
        @py_assert3 = @py_assert1.realpath
        @py_assert5 = @py_assert3()
        @py_assert9 = tmpdir.realpath
        @py_assert11 = @py_assert9()
        @py_assert7 = @py_assert5 == @py_assert11
        if not @py_assert7:
            @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.setupdir\n}.realpath\n}()\n} == %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.realpath\n}()\n}',), (@py_assert5, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
        @py_assert1 = config.toxworkdir
        @py_assert3 = @py_assert1.realpath
        @py_assert5 = @py_assert3()
        @py_assert9 = tmpdir.join
        @py_assert11 = '.tox'
        @py_assert13 = @py_assert9(@py_assert11)
        @py_assert15 = @py_assert13.realpath
        @py_assert17 = @py_assert15()
        @py_assert7 = @py_assert5 == @py_assert17
        if not @py_assert7:
            @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.toxworkdir\n}.realpath\n}()\n} == %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py10)s\n{%(py10)s = %(py8)s.join\n}(%(py12)s)\n}.realpath\n}()\n}',), (@py_assert5, @py_assert17)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py18': @pytest_ar._saferepr(@py_assert17),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py14': @pytest_ar._saferepr(@py_assert13),  'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py16': @pytest_ar._saferepr(@py_assert15),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
            raise AssertionError(@pytest_ar._format_explanation(@py_format21))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None

    def test_project_paths(self, tmpdir, newconfig):
        config = newconfig('\n            [tox]\n            toxworkdir=%s\n        ' % tmpdir)
        @py_assert1 = config.toxworkdir
        @py_assert3 = @py_assert1 == tmpdir
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.toxworkdir\n} == %(py4)s', ), (@py_assert1, tmpdir)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None


class TestParseconfig:

    def test_search_parents(self, tmpdir):
        b = tmpdir.mkdir('a').mkdir('b')
        toxinipath = tmpdir.ensure('tox.ini')
        old = b.chdir()
        try:
            config = parseconfig([])
        finally:
            old.chdir()

        @py_assert1 = config.toxinipath
        @py_assert3 = @py_assert1 == toxinipath
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.toxinipath\n} == %(py4)s', ), (@py_assert1, toxinipath)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(toxinipath) if 'toxinipath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(toxinipath) else 'toxinipath',  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None


def test_get_homedir(monkeypatch):
    monkeypatch.setattr(py.path.local, '_gethomedir', classmethod(lambda x: {}[1]))
    @py_assert1 = get_homedir()
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s()\n}') % {'py0': @pytest_ar._saferepr(get_homedir) if 'get_homedir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_homedir) else 'get_homedir',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    monkeypatch.setattr(py.path.local, '_gethomedir', classmethod(lambda x: 0 / 0))
    @py_assert1 = get_homedir()
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s()\n}') % {'py0': @pytest_ar._saferepr(get_homedir) if 'get_homedir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_homedir) else 'get_homedir',  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    monkeypatch.setattr(py.path.local, '_gethomedir', classmethod(lambda x: '123'))
    @py_assert1 = get_homedir()
    @py_assert4 = '123'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(get_homedir) if 'get_homedir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_homedir) else 'get_homedir',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


class TestGetcontextname:

    def test_blank(self, monkeypatch):
        monkeypatch.setattr(os, 'environ', {})
        @py_assert1 = getcontextname()
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(getcontextname) if 'getcontextname' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getcontextname) else 'getcontextname',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_jenkins(self, monkeypatch):
        monkeypatch.setattr(os, 'environ', {'JENKINS_URL': 'xyz'})
        @py_assert1 = getcontextname()
        @py_assert4 = 'jenkins'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(getcontextname) if 'getcontextname' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getcontextname) else 'getcontextname',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_hudson_legacy(self, monkeypatch):
        monkeypatch.setattr(os, 'environ', {'HUDSON_URL': 'xyz'})
        @py_assert1 = getcontextname()
        @py_assert4 = 'jenkins'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(getcontextname) if 'getcontextname' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getcontextname) else 'getcontextname',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


class TestIniParserAgainstCommandsKey:
    __doc__ = 'Test parsing commands with substitutions'

    def test_command_substitution_from_other_section(self, newconfig):
        config = newconfig('\n            [section]\n            key = whatever\n            [testenv]\n            commands =\n                echo {[section]key}\n            ')
        reader = SectionReader('testenv', config._cfg)
        x = reader.getargvlist('commands')
        @py_assert2 = [['echo', 'whatever']]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_command_substitution_from_other_section_multiline(self, newconfig):
        """Ensure referenced multiline commands form from other section injected
        as multiple commands."""
        config = newconfig('\n            [section]\n            commands =\n                      cmd1 param11 param12\n                      # comment is omitted\n                      cmd2 param21                            param22\n            [base]\n            commands = cmd 1                            2 3 4\n                       cmd 2\n            [testenv]\n            commands =\n                {[section]commands}\n                {[section]commands}\n                # comment is omitted\n                echo {[base]commands}\n            ')
        reader = SectionReader('testenv', config._cfg)
        x = reader.getargvlist('commands')
        @py_assert2 = ['cmd1 param11 param12'.split(), 'cmd2 param21 param22'.split(), 'cmd1 param11 param12'.split(), 'cmd2 param21 param22'.split(), ['echo', 'cmd', '1', '2', '3', '4', 'cmd', '2']]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_command_env_substitution(self, newconfig):
        """Ensure referenced {env:key:default} values are substituted correctly."""
        config = newconfig('\n           [testenv:py27]\n           setenv =\n             TEST=testvalue\n           commands =\n             ls {env:TEST}\n        ')
        reader = SectionReader('testenv:py27', config._cfg)
        x = reader.getargvlist('commands')
        @py_assert2 = ['ls testvalue'.split()]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        @py_assert2 = [
         'ls {env:TEST}'.split()]
        @py_assert1 = x != @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        y = reader.getargvlist('setenv')
        @py_assert2 = ['TEST=testvalue'.split()]
        @py_assert1 = y == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (y, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(y) if 'y' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y) else 'y'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


class TestIniParser:

    def test_getstring_single(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key=value\n        ')
        reader = SectionReader('section', config._cfg)
        x = reader.getstring('key')
        @py_assert2 = 'value'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        @py_assert1 = reader.getstring
        @py_assert3 = 'hello'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getstring\n}(%(py4)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        x = reader.getstring('hello', 'world')
        @py_assert2 = 'world'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_missing_substitution(self, tmpdir, newconfig):
        config = newconfig('\n            [mydefault]\n            key2={xyz}\n        ')
        reader = SectionReader('mydefault', config._cfg, fallbacksections=['mydefault'])
        @py_assert2 = None
        @py_assert1 = reader is not @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (reader, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        with py.test.raises(tox_plus.exception.ConfigError):
            reader.getstring('key2')

    def test_getstring_fallback_sections(self, tmpdir, newconfig):
        config = newconfig('\n            [mydefault]\n            key2=value2\n            [section]\n            key=value\n        ')
        reader = SectionReader('section', config._cfg, fallbacksections=['mydefault'])
        x = reader.getstring('key2')
        @py_assert2 = 'value2'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        x = reader.getstring('key3')
        @py_assert1 = not x
        if not @py_assert1:
            @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert1 = None
        x = reader.getstring('key3', 'world')
        @py_assert2 = 'world'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_getstring_substitution(self, tmpdir, newconfig):
        config = newconfig('\n            [mydefault]\n            key2={value2}\n            [section]\n            key={value}\n        ')
        reader = SectionReader('section', config._cfg, fallbacksections=['mydefault'])
        reader.addsubstitutions(value='newvalue', value2='newvalue2')
        x = reader.getstring('key2')
        @py_assert2 = 'newvalue2'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        x = reader.getstring('key3')
        @py_assert1 = not x
        if not @py_assert1:
            @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert1 = None
        x = reader.getstring('key3', '{value2}')
        @py_assert2 = 'newvalue2'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_getlist(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key2=\n                item1\n                {item2}\n        ')
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(item1='not', item2='grr')
        x = reader.getlist('key2')
        @py_assert2 = ['item1', 'grr']
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_getdict(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key2=\n                key1=item1\n                key2={item2}\n        ')
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(item1='not', item2='grr')
        x = reader.getdict('key2')
        @py_assert0 = 'key1'
        @py_assert2 = @py_assert0 in x
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, x)) % {'py3': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'key2'
        @py_assert2 = @py_assert0 in x
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, x)) % {'py3': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = x['key1']
        @py_assert3 = 'item1'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = x['key2']
        @py_assert3 = 'grr'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        x = reader.getdict('key3', {1: 2})
        @py_assert2 = {1: 2}
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_getstring_environment_substitution(self, monkeypatch, newconfig):
        monkeypatch.setenv('KEY1', 'hello')
        config = newconfig('\n            [section]\n            key1={env:KEY1}\n            key2={env:KEY2}\n        ')
        reader = SectionReader('section', config._cfg)
        x = reader.getstring('key1')
        @py_assert2 = 'hello'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        with py.test.raises(tox_plus.exception.ConfigError):
            reader.getstring('key2')

    def test_getstring_environment_substitution_with_default(self, monkeypatch, newconfig):
        monkeypatch.setenv('KEY1', 'hello')
        config = newconfig('\n            [section]\n            key1={env:KEY1:DEFAULT_VALUE}\n            key2={env:KEY2:DEFAULT_VALUE}\n            key3={env:KEY3:}\n        ')
        reader = SectionReader('section', config._cfg)
        x = reader.getstring('key1')
        @py_assert2 = 'hello'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        x = reader.getstring('key2')
        @py_assert2 = 'DEFAULT_VALUE'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        x = reader.getstring('key3')
        @py_assert2 = ''
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_value_matches_section_substituion(self):
        @py_assert1 = '{[setup]commands}'
        @py_assert3 = is_section_substitution(@py_assert1)
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0': @pytest_ar._saferepr(is_section_substitution) if 'is_section_substitution' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_section_substitution) else 'is_section_substitution',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None

    def test_value_doesn_match_section_substitution(self):
        @py_assert1 = '{[ ]commands}'
        @py_assert3 = is_section_substitution(@py_assert1)
        @py_assert6 = None
        @py_assert5 = @py_assert3 is @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(is_section_substitution) if 'is_section_substitution' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_section_substitution) else 'is_section_substitution',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = '{[setup]}'
        @py_assert3 = is_section_substitution(@py_assert1)
        @py_assert6 = None
        @py_assert5 = @py_assert3 is @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(is_section_substitution) if 'is_section_substitution' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_section_substitution) else 'is_section_substitution',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = '{[setup] commands}'
        @py_assert3 = is_section_substitution(@py_assert1)
        @py_assert6 = None
        @py_assert5 = @py_assert3 is @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(is_section_substitution) if 'is_section_substitution' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_section_substitution) else 'is_section_substitution',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_getstring_other_section_substitution(self, newconfig):
        config = newconfig('\n            [section]\n            key = rue\n            [testenv]\n            key = t{[section]key}\n            ')
        reader = SectionReader('testenv', config._cfg)
        x = reader.getstring('key')
        @py_assert2 = 'true'
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_argvlist(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key2=\n                cmd1 {item1} {item2}\n                cmd2 {item2}\n        ')
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(item1='with space', item2='grr')
        @py_assert1 = reader.getargvlist
        @py_assert3 = 'key1'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = []
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getargvlist\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        x = reader.getargvlist('key2')
        @py_assert2 = [['cmd1', 'with', 'space', 'grr'], ['cmd2', 'grr']]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_argvlist_windows_escaping(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            comm = py.test {posargs}\n        ')
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(['hello\\this'])
        argv = reader.getargv('comm')
        @py_assert2 = ['py.test', 'hello\\this']
        @py_assert1 = argv == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (argv, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(argv) if 'argv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(argv) else 'argv'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_argvlist_multiline(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key2=\n                cmd1 {item1} \\ # a comment\n                     {item2}\n        ')
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(item1='with space', item2='grr')
        @py_assert1 = reader.getargvlist
        @py_assert3 = 'key1'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = []
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getargvlist\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        x = reader.getargvlist('key2')
        @py_assert2 = [['cmd1', 'with', 'space', 'grr']]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_argvlist_quoting_in_command(self, tmpdir, newconfig):
        config = newconfig("\n            [section]\n            key1=\n                cmd1 'with space' \\ # a comment\n                     'after the comment'\n        ")
        reader = SectionReader('section', config._cfg)
        x = reader.getargvlist('key1')
        @py_assert2 = [['cmd1', 'with space', 'after the comment']]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_argvlist_positional_substitution(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key2=\n                cmd1 []\n                cmd2 {posargs:{item2}                      other}\n        ')
        reader = SectionReader('section', config._cfg)
        posargs = ['hello', 'world']
        reader.addsubstitutions(posargs, item2='value2')
        @py_assert1 = reader.getargvlist
        @py_assert3 = 'key1'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = []
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getargvlist\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        argvlist = reader.getargvlist('key2')
        @py_assert0 = argvlist[0]
        @py_assert3 = [
         'cmd1']
        @py_assert6 = @py_assert3 + posargs
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s + %(py5)s)', ), (@py_assert0, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(posargs) if 'posargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(posargs) else 'posargs'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert6 = None
        @py_assert0 = argvlist[1]
        @py_assert3 = [
         'cmd2']
        @py_assert6 = @py_assert3 + posargs
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s + %(py5)s)', ), (@py_assert0, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(posargs) if 'posargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(posargs) else 'posargs'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert6 = None
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions([], item2='value2')
        @py_assert1 = reader.getargvlist
        @py_assert3 = 'key1'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = []
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getargvlist\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        argvlist = reader.getargvlist('key2')
        @py_assert0 = argvlist[0]
        @py_assert3 = [
         'cmd1']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = argvlist[1]
        @py_assert3 = [
         'cmd2', 'value2', 'other']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_argvlist_quoted_posargs(self, tmpdir, newconfig):
        config = newconfig("\n            [section]\n            key2=\n                cmd1 --foo-args='{posargs}'\n                cmd2 -f '{posargs}'\n                cmd3 -f {posargs}\n        ")
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(['foo', 'bar'])
        @py_assert1 = reader.getargvlist
        @py_assert3 = 'key1'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = []
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getargvlist\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        x = reader.getargvlist('key2')
        @py_assert2 = [['cmd1', '--foo-args=foo bar'], ['cmd2', '-f', 'foo bar'], ['cmd3', '-f', 'foo', 'bar']]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_argvlist_posargs_with_quotes(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key2=\n                cmd1 -f {posargs}\n        ')
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(['foo', "'bar", "baz'"])
        @py_assert1 = reader.getargvlist
        @py_assert3 = 'key1'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = []
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getargvlist\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        x = reader.getargvlist('key2')
        @py_assert2 = [['cmd1', '-f', 'foo', 'bar baz']]
        @py_assert1 = x == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (x, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_positional_arguments_are_only_replaced_when_standing_alone(self, tmpdir, newconfig):
        config = newconfig("\n            [section]\n            key=\n                cmd0 []\n                cmd1 -m '[abc]'\n                cmd2 -m ''something'' []\n                cmd3 something[]else\n        ")
        reader = SectionReader('section', config._cfg)
        posargs = ['hello', 'world']
        reader.addsubstitutions(posargs)
        argvlist = reader.getargvlist('key')
        @py_assert0 = argvlist[0]
        @py_assert3 = [
         'cmd0']
        @py_assert6 = @py_assert3 + posargs
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s + %(py5)s)', ), (@py_assert0, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(posargs) if 'posargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(posargs) else 'posargs'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert6 = None
        @py_assert0 = argvlist[1]
        @py_assert3 = [
         'cmd1', '-m', '[abc]']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = argvlist[2]
        @py_assert3 = [
         'cmd2', '-m', 'something']
        @py_assert6 = @py_assert3 + posargs
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s + %(py5)s)', ), (@py_assert0, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(posargs) if 'posargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(posargs) else 'posargs'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert6 = None
        @py_assert0 = argvlist[3]
        @py_assert3 = [
         'cmd3', 'something[]else']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_substitution_with_multiple_words(self, newconfig):
        inisource = '\n            [section]\n            key = py.test -n5 --junitxml={envlogdir}/junit-{envname}.xml []\n            '
        config = newconfig(inisource)
        reader = SectionReader('section', config._cfg)
        posargs = ['hello', 'world']
        reader.addsubstitutions(posargs, envlogdir='ENV_LOG_DIR', envname='ENV_NAME')
        expected = [
         'py.test', '-n5', '--junitxml=ENV_LOG_DIR/junit-ENV_NAME.xml', 'hello', 'world']
        @py_assert0 = reader.getargvlist('key')[0]
        @py_assert2 = @py_assert0 == expected
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expected)) % {'py3': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_getargv(self, newconfig):
        config = newconfig('\n            [section]\n            key=some command "with quoting"\n        ')
        reader = SectionReader('section', config._cfg)
        expected = ['some', 'command', 'with quoting']
        @py_assert1 = reader.getargv
        @py_assert3 = 'key'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = @py_assert5 == expected
        if not @py_assert7:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getargv\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, expected)) % {'py8': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_getpath(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            path1={HELLO}\n        ')
        reader = SectionReader('section', config._cfg)
        reader.addsubstitutions(toxinidir=tmpdir, HELLO='mypath')
        x = reader.getpath('path1', tmpdir)
        @py_assert3 = tmpdir.join
        @py_assert5 = 'mypath'
        @py_assert7 = @py_assert3(@py_assert5)
        @py_assert1 = x == @py_assert7
        if not @py_assert1:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.join\n}(%(py6)s)\n}', ), (x, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_getbool(self, tmpdir, newconfig):
        config = newconfig('\n            [section]\n            key1=True\n            key2=False\n            key1a=true\n            key2a=falsE\n            key5=yes\n        ')
        reader = SectionReader('section', config._cfg)
        @py_assert1 = reader.getbool
        @py_assert3 = 'key1'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = True
        @py_assert7 = @py_assert5 is @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getbool\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = reader.getbool
        @py_assert3 = 'key1a'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = True
        @py_assert7 = @py_assert5 is @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getbool\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = reader.getbool
        @py_assert3 = 'key2'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = False
        @py_assert7 = @py_assert5 is @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getbool\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = reader.getbool
        @py_assert3 = 'key2a'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = False
        @py_assert7 = @py_assert5 is @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.getbool\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(reader) if 'reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reader) else 'reader',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        py.test.raises(KeyError, 'reader.getbool("key3")')
        py.test.raises(tox_plus.exception.ConfigError, 'reader.getbool("key5")')


class TestConfigTestEnv:

    def test_commentchars_issue33(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv] # hello\n            deps = http://abc#123\n            commands=\n                python -c "x ; y"\n        ')
        envconfig = config.envconfigs['python']
        @py_assert0 = envconfig.deps[0]
        @py_assert2 = @py_assert0.name
        @py_assert5 = 'http://abc#123'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = envconfig.commands[0]
        @py_assert3 = [
         'python', '-c', 'x ; y']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_defaults(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            commands=\n                xyz --abc\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.commands
        @py_assert4 = [
         [
          'xyz', '--abc']]
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.commands\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = envconfig.changedir
        @py_assert5 = config.setupdir
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.changedir\n} == %(py6)s\n{%(py6)s = %(py4)s.setupdir\n}', ), (@py_assert1, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = envconfig.sitepackages
        @py_assert4 = False
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sitepackages\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = envconfig.usedevelop
        @py_assert4 = False
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.usedevelop\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = envconfig.ignore_errors
        @py_assert4 = False
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ignore_errors\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = envconfig.envlogdir
        @py_assert5 = envconfig.envdir
        @py_assert7 = @py_assert5.join
        @py_assert9 = 'log'
        @py_assert11 = @py_assert7(@py_assert9)
        @py_assert3 = @py_assert1 == @py_assert11
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlogdir\n} == %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.envdir\n}.join\n}(%(py10)s)\n}', ), (@py_assert1, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
        @py_assert2 = envconfig.setenv
        @py_assert4 = @py_assert2.keys
        @py_assert6 = @py_assert4()
        @py_assert8 = list(@py_assert6)
        @py_assert11 = [
         'PYTHONHASHSEED']
        @py_assert10 = @py_assert8 == @py_assert11
        if not @py_assert10:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.setenv\n}.keys\n}()\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py9': @pytest_ar._saferepr(@py_assert8),  'py12': @pytest_ar._saferepr(@py_assert11),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
        hashseed = envconfig.setenv['PYTHONHASHSEED']
        @py_assert3 = isinstance(hashseed, str)
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(hashseed) if 'hashseed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hashseed) else 'hashseed',  'py2': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert3 = None
        int_hashseed = int(hashseed)
        @py_assert2 = 0
        @py_assert1 = int_hashseed > @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py3)s', ), (int_hashseed, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(int_hashseed) if 'int_hashseed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int_hashseed) else 'int_hashseed'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_sitepackages_switch(self, tmpdir, newconfig):
        config = newconfig(['--sitepackages'], '')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.sitepackages
        @py_assert4 = True
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sitepackages\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_installpkg_tops_develop(self, newconfig):
        config = newconfig(['--installpkg=abc'], '\n            [testenv]\n            usedevelop = True\n        ')
        @py_assert0 = config.envconfigs['python']
        @py_assert2 = @py_assert0.usedevelop
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py1)s.usedevelop\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    def test_specific_command_overrides(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            commands=xyz\n            [testenv:py]\n            commands=abc\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['py']
        @py_assert1 = envconfig.commands
        @py_assert4 = [
         [
          'abc']]
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.commands\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_whitelist_externals(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            whitelist_externals = xyz\n            commands=xyz\n            [testenv:x]\n\n            [testenv:py]\n            whitelist_externals = xyz2\n            commands=abc\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['py']
        @py_assert1 = envconfig.commands
        @py_assert4 = [
         [
          'abc']]
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.commands\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = envconfig.whitelist_externals
        @py_assert4 = [
         'xyz2']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.whitelist_externals\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        envconfig = config.envconfigs['x']
        @py_assert1 = envconfig.whitelist_externals
        @py_assert4 = [
         'xyz']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.whitelist_externals\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_changedir(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            changedir=xyz\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.changedir
        @py_assert3 = @py_assert1.basename
        @py_assert6 = 'xyz'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.changedir\n}.basename\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = envconfig.changedir
        @py_assert5 = config.toxinidir
        @py_assert7 = @py_assert5.join
        @py_assert9 = 'xyz'
        @py_assert11 = @py_assert7(@py_assert9)
        @py_assert3 = @py_assert1 == @py_assert11
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.changedir\n} == %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.toxinidir\n}.join\n}(%(py10)s)\n}', ), (@py_assert1, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None

    def test_ignore_errors(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            ignore_errors=True\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.ignore_errors
        @py_assert4 = True
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ignore_errors\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_envbindir(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            basepython=python\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.envpython
        @py_assert5 = envconfig.envbindir
        @py_assert7 = @py_assert5.join
        @py_assert9 = 'python'
        @py_assert11 = @py_assert7(@py_assert9)
        @py_assert3 = @py_assert1 == @py_assert11
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envpython\n} == %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.envbindir\n}.join\n}(%(py10)s)\n}', ), (@py_assert1, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None

    @pytest.mark.parametrize('bp', ['jython', 'pypy', 'pypy3'])
    def test_envbindir_jython(self, tmpdir, newconfig, bp):
        config = newconfig('\n            [testenv]\n            basepython=%s\n        ' % bp)
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s',), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.envbindir
        @py_assert3 = @py_assert1.basename
        @py_assert6 = 'bin'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.envbindir\n}.basename\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        if bp == 'jython':
            @py_assert1 = envconfig.envpython
            @py_assert5 = envconfig.envbindir
            @py_assert7 = @py_assert5.join
            @py_assert10 = @py_assert7(bp)
            @py_assert3 = @py_assert1 == @py_assert10
            if not @py_assert3:
                @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envpython\n} == %(py11)s\n{%(py11)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.envbindir\n}.join\n}(%(py9)s)\n}',), (@py_assert1, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py8': @pytest_ar._saferepr(@py_assert7),  'py9': @pytest_ar._saferepr(bp) if 'bp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bp) else 'bp',  'py11': @pytest_ar._saferepr(@py_assert10),  'py2': @pytest_ar._saferepr(@py_assert1)}
                @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
                raise AssertionError(@pytest_ar._format_explanation(@py_format14))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = None

    def test_setenv_overrides(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            setenv =\n                PYTHONPATH = something\n                ANOTHER_VAL=else\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        @py_assert0 = 'PYTHONPATH'
        @py_assert4 = envconfig.setenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.setenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'ANOTHER_VAL'
        @py_assert4 = envconfig.setenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.setenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = envconfig.setenv['PYTHONPATH']
        @py_assert3 = 'something'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = envconfig.setenv['ANOTHER_VAL']
        @py_assert3 = 'else'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    @pytest.mark.parametrize('plat', ['win32', 'linux2'])
    def test_passenv_as_multiline_list(self, tmpdir, newconfig, monkeypatch, plat):
        monkeypatch.setattr(sys, 'platform', plat)
        monkeypatch.setenv('A123A', 'a')
        monkeypatch.setenv('A123B', 'b')
        monkeypatch.setenv('BX23', '0')
        config = newconfig('\n            [testenv]\n            passenv =\n                      A123*\n                      # isolated comment\n                      B?23\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        if plat == 'win32':
            @py_assert0 = 'PATHEXT'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'SYSTEMDRIVE'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'SYSTEMROOT'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'TEMP'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'TMP'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
        else:
            @py_assert0 = 'TMPDIR'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'PATH'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'PIP_INDEX_URL'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'LANG'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'LD_LIBRARY_PATH'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'A123A'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'A123B'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    @pytest.mark.parametrize('plat', ['win32', 'linux2'])
    def test_passenv_as_space_separated_list(self, tmpdir, newconfig, monkeypatch, plat):
        monkeypatch.setattr(sys, 'platform', plat)
        monkeypatch.setenv('A123A', 'a')
        monkeypatch.setenv('A123B', 'b')
        monkeypatch.setenv('BX23', '0')
        config = newconfig('\n            [testenv]\n            passenv =\n                      # comment\n                      A123*  B?23\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        if plat == 'win32':
            @py_assert0 = 'PATHEXT'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'SYSTEMDRIVE'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'SYSTEMROOT'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'TEMP'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
            @py_assert0 = 'TMP'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
        else:
            @py_assert0 = 'TMPDIR'
            @py_assert4 = envconfig.passenv
            @py_assert2 = @py_assert0 in @py_assert4
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'PATH'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'PIP_INDEX_URL'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'LANG'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'A123A'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'A123B'
        @py_assert4 = envconfig.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    def test_passenv_with_factor(self, tmpdir, newconfig, monkeypatch):
        monkeypatch.setenv('A123A', 'a')
        monkeypatch.setenv('A123B', 'b')
        monkeypatch.setenv('A123C', 'c')
        monkeypatch.setenv('A123D', 'd')
        monkeypatch.setenv('BX23', '0')
        monkeypatch.setenv('CCA43', '3')
        monkeypatch.setenv('CB21', '4')
        config = newconfig('\n            [tox]\n            envlist = {x1,x2}\n            [testenv]\n            passenv =\n                x1: A123A CC*\n                x1: CB21\n                # passed to both environments\n                A123C\n                x2: A123B A123D\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert0 = 'A123A'
        @py_assert3 = config.envconfigs['x1']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'A123C'
        @py_assert3 = config.envconfigs['x1']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'CCA43'
        @py_assert3 = config.envconfigs['x1']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'CB21'
        @py_assert3 = config.envconfigs['x1']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'A123B'
        @py_assert3 = config.envconfigs['x1']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'A123D'
        @py_assert3 = config.envconfigs['x1']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'BX23'
        @py_assert3 = config.envconfigs['x1']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'A123B'
        @py_assert3 = config.envconfigs['x2']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'A123D'
        @py_assert3 = config.envconfigs['x2']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'A123A'
        @py_assert3 = config.envconfigs['x2']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'A123C'
        @py_assert3 = config.envconfigs['x2']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'CCA43'
        @py_assert3 = config.envconfigs['x2']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'CB21'
        @py_assert3 = config.envconfigs['x2']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'BX23'
        @py_assert3 = config.envconfigs['x2']
        @py_assert5 = @py_assert3.passenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.passenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None

    def test_passenv_from_global_env(self, tmpdir, newconfig, monkeypatch):
        monkeypatch.setenv('A1', 'a1')
        monkeypatch.setenv('A2', 'a2')
        monkeypatch.setenv('TOX_TESTENV_PASSENV', 'A1')
        config = newconfig('\n            [testenv]\n            passenv = A2\n        ')
        env = config.envconfigs['python']
        @py_assert0 = 'A1'
        @py_assert4 = env.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'A2'
        @py_assert4 = env.passenv
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.passenv\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    def test_changedir_override(self, tmpdir, newconfig):
        config = newconfig('\n            [testenv]\n            changedir=xyz\n            [testenv:python]\n            changedir=abc\n            basepython=python2.6\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.changedir
        @py_assert3 = @py_assert1.basename
        @py_assert6 = 'abc'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.changedir\n}.basename\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = envconfig.changedir
        @py_assert5 = config.setupdir
        @py_assert7 = @py_assert5.join
        @py_assert9 = 'abc'
        @py_assert11 = @py_assert7(@py_assert9)
        @py_assert3 = @py_assert1 == @py_assert11
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.changedir\n} == %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.setupdir\n}.join\n}(%(py10)s)\n}', ), (@py_assert1, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None

    def test_install_command_setting(self, newconfig):
        config = newconfig('\n            [testenv]\n            install_command=some_install {packages}\n        ')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.install_command
        @py_assert4 = [
         'some_install', '{packages}']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.install_command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_install_command_must_contain_packages(self, newconfig):
        py.test.raises(tox_plus.exception.ConfigError, newconfig, '\n            [testenv]\n            install_command=pip install\n        ')

    def test_install_command_substitutions(self, newconfig):
        config = newconfig('\n            [testenv]\n            install_command=some_install --arg={toxinidir}/foo                 {envname} {opts} {packages}\n        ')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.install_command
        @py_assert4 = [
         'some_install', '--arg=%s/foo' % config.toxinidir, 'python', '{opts}', '{packages}']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.install_command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_pip_pre(self, newconfig):
        config = newconfig('\n            [testenv]\n            pip_pre=true\n        ')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.pip_pre
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.pip_pre\n}') % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None

    def test_pip_pre_cmdline_override(self, newconfig):
        config = newconfig([
         '--pre'], '\n            [testenv]\n            pip_pre=false\n        ')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.pip_pre
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.pip_pre\n}') % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None

    def test_downloadcache(self, newconfig, monkeypatch):
        monkeypatch.delenv('PIP_DOWNLOAD_CACHE', raising=False)
        config = newconfig('\n            [testenv]\n            downloadcache=thecache\n        ')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.downloadcache
        @py_assert3 = @py_assert1.basename
        @py_assert6 = 'thecache'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.downloadcache\n}.basename\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_downloadcache_env_override(self, newconfig, monkeypatch):
        monkeypatch.setenv('PIP_DOWNLOAD_CACHE', 'fromenv')
        config = newconfig('\n            [testenv]\n            downloadcache=somepath\n        ')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.downloadcache
        @py_assert3 = @py_assert1.basename
        @py_assert6 = 'fromenv'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.downloadcache\n}.basename\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_downloadcache_only_if_in_config(self, newconfig, tmpdir, monkeypatch):
        monkeypatch.setenv('PIP_DOWNLOAD_CACHE', tmpdir)
        config = newconfig('')
        envconfig = config.envconfigs['python']
        @py_assert1 = envconfig.downloadcache
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.downloadcache\n}') % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None

    def test_simple(tmpdir, newconfig):
        config = newconfig('\n            [testenv:py26]\n            basepython=python2.6\n            [testenv:py27]\n            basepython=python2.7\n        ')
        @py_assert2 = config.envconfigs
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.envconfigs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert0 = 'py26'
        @py_assert4 = config.envconfigs
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.envconfigs\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'py27'
        @py_assert4 = config.envconfigs
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.envconfigs\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    def test_substitution_error(tmpdir, newconfig):
        py.test.raises(tox_plus.exception.ConfigError, newconfig, '\n            [testenv:py27]\n            basepython={xyz}\n        ')

    def test_substitution_defaults(tmpdir, newconfig):
        config = newconfig('\n            [testenv:py27]\n            commands =\n                {toxinidir}\n                {toxworkdir}\n                {envdir}\n                {envbindir}\n                {envtmpdir}\n                {envpython}\n                {homedir}\n                {distshare}\n                {envlogdir}\n        ')
        conf = config.envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0][0]
        @py_assert4 = config.toxinidir
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.toxinidir\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = argv[1][0]
        @py_assert4 = config.toxworkdir
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.toxworkdir\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = argv[2][0]
        @py_assert4 = conf.envdir
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.envdir\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(conf) if 'conf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf) else 'conf',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = argv[3][0]
        @py_assert4 = conf.envbindir
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.envbindir\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(conf) if 'conf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf) else 'conf',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = argv[4][0]
        @py_assert4 = conf.envtmpdir
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.envtmpdir\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(conf) if 'conf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf) else 'conf',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = argv[5][0]
        @py_assert4 = conf.envpython
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.envpython\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(conf) if 'conf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf) else 'conf',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = argv[6][0]
        @py_assert5 = config.homedir
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 == @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.homedir\n})\n}', ), (@py_assert0, @py_assert7)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py4': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None
        @py_assert0 = argv[7][0]
        @py_assert4 = config.homedir
        @py_assert6 = @py_assert4.join
        @py_assert8 = '.tox'
        @py_assert10 = 'distshare'
        @py_assert12 = @py_assert6(@py_assert8, @py_assert10)
        @py_assert2 = @py_assert0 == @py_assert12
        if not @py_assert2:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py13)s\n{%(py13)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.homedir\n}.join\n}(%(py9)s, %(py11)s)\n}', ), (@py_assert0, @py_assert12)) % {'py3': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py13': @pytest_ar._saferepr(@py_assert12),  'py1': @pytest_ar._saferepr(@py_assert0),  'py9': @pytest_ar._saferepr(@py_assert8),  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
        @py_assert0 = argv[8][0]
        @py_assert4 = conf.envlogdir
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.envlogdir\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(conf) if 'conf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf) else 'conf',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    def test_substitution_positional(self, newconfig):
        inisource = '\n            [testenv:py27]\n            commands =\n                cmd1 [hello]                      world\n                cmd1 {posargs:hello}                      world\n        '
        conf = newconfig([], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1', '[hello]', 'world']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = argv[1]
        @py_assert3 = [
         'cmd1', 'hello', 'world']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        conf = newconfig(['brave', 'new'], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1', '[hello]', 'world']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = argv[1]
        @py_assert3 = [
         'cmd1', 'brave', 'new', 'world']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_substitution_noargs_issue240(self, newconfig):
        inisource = '\n            [testenv]\n            commands = echo {posargs:foo}\n        '
        conf = newconfig([''], inisource).envconfigs['python']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'echo']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_posargs_backslashed_or_quoted(self, tmpdir, newconfig):
        inisource = '\n            [testenv:py27]\n            commands =\n                echo "\\{posargs\\}" = {posargs}\n                echo "posargs = " "{posargs}"\n        '
        conf = newconfig([], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'echo', '\\{posargs\\}', '=']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = argv[1]
        @py_assert3 = [
         'echo', 'posargs = ', '']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        conf = newconfig(['dog', 'cat'], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'echo', '\\{posargs\\}', '=', 'dog', 'cat']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = argv[1]
        @py_assert3 = [
         'echo', 'posargs = ', 'dog cat']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_rewrite_posargs(self, tmpdir, newconfig):
        inisource = '\n            [testenv:py27]\n            args_are_paths = True\n            changedir = tests\n            commands = cmd1 {posargs:hello}\n        '
        conf = newconfig([], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1', 'hello']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        conf = newconfig(['tests/hello'], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1', 'tests/hello']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        tmpdir.ensure('tests', 'hello')
        conf = newconfig(['tests/hello'], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1', 'hello']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_rewrite_simple_posargs(self, tmpdir, newconfig):
        inisource = '\n            [testenv:py27]\n            args_are_paths = True\n            changedir = tests\n            commands = cmd1 {posargs}\n        '
        conf = newconfig([], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        conf = newconfig(['tests/hello'], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1', 'tests/hello']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        tmpdir.ensure('tests', 'hello')
        conf = newconfig(['tests/hello'], inisource).envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0]
        @py_assert3 = [
         'cmd1', 'hello']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_take_dependencies_from_other_testenv(self, newconfig):
        inisource = '\n            [testenv]\n            deps=\n                pytest\n                pytest-cov\n            [testenv:py27]\n            deps=\n                {[testenv]deps}\n                fun\n        '
        conf = newconfig([], inisource).envconfigs['py27']
        packages = [dep.name for dep in conf.deps]
        @py_assert2 = ['pytest', 'pytest-cov', 'fun']
        @py_assert1 = packages == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (packages, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(packages) if 'packages' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(packages) else 'packages'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_take_dependencies_from_other_section(self, newconfig):
        inisource = '\n            [testing:pytest]\n            deps=\n                pytest\n                pytest-cov\n            [testing:mock]\n            deps=\n                mock\n            [testenv]\n            deps=\n                {[testing:pytest]deps}\n                {[testing:mock]deps}\n                fun\n        '
        conf = newconfig([], inisource)
        env = conf.envconfigs['python']
        packages = [dep.name for dep in env.deps]
        @py_assert2 = ['pytest', 'pytest-cov', 'mock', 'fun']
        @py_assert1 = packages == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (packages, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(packages) if 'packages' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(packages) else 'packages'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_multilevel_substitution(self, newconfig):
        inisource = '\n            [testing:pytest]\n            deps=\n                pytest\n                pytest-cov\n            [testing:mock]\n            deps=\n                mock\n\n            [testing]\n            deps=\n                {[testing:pytest]deps}\n                {[testing:mock]deps}\n\n            [testenv]\n            deps=\n                {[testing]deps}\n                fun\n        '
        conf = newconfig([], inisource)
        env = conf.envconfigs['python']
        packages = [dep.name for dep in env.deps]
        @py_assert2 = ['pytest', 'pytest-cov', 'mock', 'fun']
        @py_assert1 = packages == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (packages, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(packages) if 'packages' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(packages) else 'packages'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_recursive_substitution_cycle_fails(self, newconfig):
        inisource = '\n            [testing:pytest]\n            deps=\n                {[testing:mock]deps}\n            [testing:mock]\n            deps=\n                {[testing:pytest]deps}\n\n            [testenv]\n            deps=\n                {[testing:pytest]deps}\n        '
        py.test.raises(ValueError, newconfig, [], inisource)

    def test_single_value_from_other_secton(self, newconfig, tmpdir):
        inisource = '\n            [common]\n            changedir = testing\n            [testenv]\n            changedir = {[common]changedir}\n        '
        conf = newconfig([], inisource).envconfigs['python']
        @py_assert1 = conf.changedir
        @py_assert3 = @py_assert1.basename
        @py_assert6 = 'testing'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.changedir\n}.basename\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(conf) if 'conf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf) else 'conf',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = conf.changedir
        @py_assert3 = @py_assert1.dirpath
        @py_assert5 = @py_assert3()
        @py_assert7 = @py_assert5.realpath
        @py_assert9 = @py_assert7()
        @py_assert13 = tmpdir.realpath
        @py_assert15 = @py_assert13()
        @py_assert11 = @py_assert9 == @py_assert15
        if not @py_assert11:
            @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.changedir\n}.dirpath\n}()\n}.realpath\n}()\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py12)s.realpath\n}()\n}',), (@py_assert9, @py_assert15)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(conf) if 'conf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf) else 'conf',  'py4': @pytest_ar._saferepr(@py_assert3),  'py14': @pytest_ar._saferepr(@py_assert13),  'py8': @pytest_ar._saferepr(@py_assert7),  'py16': @pytest_ar._saferepr(@py_assert15),  'py12': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
            raise AssertionError(@pytest_ar._format_explanation(@py_format19))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None

    def test_factors(self, newconfig):
        inisource = '\n            [tox]\n            envlist = a-x,b\n\n            [testenv]\n            deps=\n                dep-all\n                a: dep-a\n                b: dep-b\n                x: dep-x\n        '
        conf = newconfig([], inisource)
        configs = conf.envconfigs
        @py_assert0 = [dep.name for dep in configs['a-x'].deps]
        @py_assert3 = [
         'dep-all', 'dep-a', 'dep-x']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = [dep.name for dep in configs['b'].deps]
        @py_assert3 = [
         'dep-all', 'dep-b']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_factor_ops(self, newconfig):
        inisource = '\n            [tox]\n            envlist = {a,b}-{x,y}\n\n            [testenv]\n            deps=\n                a,b: dep-a-or-b\n                a-x: dep-a-and-x\n                {a,b}-y: dep-ab-and-y\n        '
        configs = newconfig([], inisource).envconfigs
        get_deps = lambda env: [dep.name for dep in configs[env].deps]
        @py_assert1 = 'a-x'
        @py_assert3 = get_deps(@py_assert1)
        @py_assert6 = [
         'dep-a-or-b', 'dep-a-and-x']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(get_deps) if 'get_deps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_deps) else 'get_deps',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = 'a-y'
        @py_assert3 = get_deps(@py_assert1)
        @py_assert6 = [
         'dep-a-or-b', 'dep-ab-and-y']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(get_deps) if 'get_deps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_deps) else 'get_deps',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = 'b-x'
        @py_assert3 = get_deps(@py_assert1)
        @py_assert6 = [
         'dep-a-or-b']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(get_deps) if 'get_deps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_deps) else 'get_deps',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = 'b-y'
        @py_assert3 = get_deps(@py_assert1)
        @py_assert6 = [
         'dep-a-or-b', 'dep-ab-and-y']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(get_deps) if 'get_deps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_deps) else 'get_deps',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_default_factors(self, newconfig):
        inisource = '\n            [tox]\n            envlist = py{26,27,33,34}-dep\n\n            [testenv]\n            deps=\n                dep: dep\n        '
        conf = newconfig([], inisource)
        configs = conf.envconfigs
        for name, config in configs.items():
            @py_assert1 = config.basepython
            @py_assert4 = 'python%s.%s'
            @py_assert6 = (
             name[2], name[3])
            @py_assert8 = @py_assert4 % @py_assert6
            @py_assert3 = @py_assert1 == @py_assert8
            if not @py_assert3:
                @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.basepython\n} == (%(py5)s %% %(py7)s)', ), (@py_assert1, @py_assert8)) % {'py7': @pytest_ar._saferepr(@py_assert6),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None

    @pytest.mark.issue188
    def test_factors_in_boolean(self, newconfig):
        inisource = '\n            [tox]\n            envlist = py{27,33}\n\n            [testenv]\n            recreate =\n                py27: True\n        '
        configs = newconfig([], inisource).envconfigs
        @py_assert0 = configs['py27']
        @py_assert2 = @py_assert0.recreate
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py1)s.recreate\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = configs['py33']
        @py_assert2 = @py_assert0.recreate
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py1)s.recreate\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    @pytest.mark.issue190
    def test_factors_in_setenv(self, newconfig):
        inisource = '\n            [tox]\n            envlist = py27,py26\n\n            [testenv]\n            setenv =\n                py27: X = 1\n        '
        configs = newconfig([], inisource).envconfigs
        @py_assert0 = configs['py27'].setenv['X']
        @py_assert3 = '1'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 'X'
        @py_assert3 = configs['py26']
        @py_assert5 = @py_assert3.setenv
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py4)s.setenv\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None

    @pytest.mark.issue191
    def test_factor_use_not_checked(self, newconfig):
        inisource = '\n            [tox]\n            envlist = py27-{a,b}\n\n            [testenv]\n            deps = b: test\n        '
        configs = newconfig([], inisource).envconfigs
        @py_assert2 = configs.keys
        @py_assert4 = @py_assert2()
        @py_assert6 = set(@py_assert4)
        @py_assert10 = [
         'py27-a', 'py27-b']
        @py_assert12 = set(@py_assert10)
        @py_assert8 = @py_assert6 == @py_assert12
        if not @py_assert8:
            @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py13': @pytest_ar._saferepr(@py_assert12),  'py1': @pytest_ar._saferepr(configs) if 'configs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(configs) else 'configs',  'py9': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None

    @pytest.mark.issue198
    def test_factors_groups_touch(self, newconfig):
        inisource = '\n            [tox]\n            envlist = {a,b}{-x,}\n\n            [testenv]\n            deps=\n                a,b,x,y: dep\n        '
        configs = newconfig([], inisource).envconfigs
        @py_assert2 = configs.keys
        @py_assert4 = @py_assert2()
        @py_assert6 = set(@py_assert4)
        @py_assert10 = [
         'a', 'a-x', 'b', 'b-x']
        @py_assert12 = set(@py_assert10)
        @py_assert8 = @py_assert6 == @py_assert12
        if not @py_assert8:
            @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py13': @pytest_ar._saferepr(@py_assert12),  'py1': @pytest_ar._saferepr(configs) if 'configs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(configs) else 'configs',  'py9': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py11': @pytest_ar._saferepr(@py_assert10),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None

    def test_period_in_factor(self, newconfig):
        inisource = '\n            [tox]\n            envlist = py27-{django1.6,django1.7}\n\n            [testenv]\n            deps =\n                django1.6: Django==1.6\n                django1.7: Django==1.7\n        '
        configs = newconfig([], inisource).envconfigs
        @py_assert2 = sorted(configs)
        @py_assert5 = [
         'py27-django1.6', 'py27-django1.7']
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py1': @pytest_ar._saferepr(configs) if 'configs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(configs) else 'configs'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = [d.name for d in configs['py27-django1.6'].deps]
        @py_assert3 = [
         'Django==1.6']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


class TestGlobalOptions:

    def test_notest(self, newconfig):
        config = newconfig([], '')
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.notest
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.notest\n}') % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        config = newconfig(['--notest'], '')
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.notest
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.notest\n}') % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None

    def test_verbosity(self, newconfig):
        config = newconfig([], '')
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.verbosity
        @py_assert6 = 0
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.verbosity\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        config = newconfig(['-v'], '')
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.verbosity
        @py_assert6 = 1
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.verbosity\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        config = newconfig(['-vv'], '')
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.verbosity
        @py_assert6 = 2
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.verbosity\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_substitution_jenkins_default(self, tmpdir, monkeypatch, newconfig):
        monkeypatch.setenv('HUDSON_URL', 'xyz')
        config = newconfig('\n            [testenv:py27]\n            commands =\n                {distshare}\n        ')
        conf = config.envconfigs['py27']
        argv = conf.commands
        expect_path = config.toxworkdir.join('distshare')
        @py_assert0 = argv[0][0]
        @py_assert2 = @py_assert0 == expect_path
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expect_path)) % {'py3': @pytest_ar._saferepr(expect_path) if 'expect_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expect_path) else 'expect_path',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_substitution_jenkins_context(self, tmpdir, monkeypatch, newconfig):
        monkeypatch.setenv('HUDSON_URL', 'xyz')
        monkeypatch.setenv('WORKSPACE', tmpdir)
        config = newconfig('\n            [tox:jenkins]\n            distshare = {env:WORKSPACE}/hello\n            [testenv:py27]\n            commands =\n                {distshare}\n        ')
        conf = config.envconfigs['py27']
        argv = conf.commands
        @py_assert0 = argv[0][0]
        @py_assert4 = config.distshare
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.distshare\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert1 = config.distshare
        @py_assert5 = tmpdir.join
        @py_assert7 = 'hello'
        @py_assert9 = @py_assert5(@py_assert7)
        @py_assert3 = @py_assert1 == @py_assert9
        if not @py_assert3:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.distshare\n} == %(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s.join\n}(%(py8)s)\n}', ), (@py_assert1, @py_assert9)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir',  'py8': @pytest_ar._saferepr(@py_assert7),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None

    def test_sdist_specification(self, tmpdir, newconfig):
        config = newconfig('\n            [tox]\n            sdistsrc = {distshare}/xyz.zip\n        ')
        @py_assert1 = config.sdistsrc
        @py_assert5 = config.distshare
        @py_assert7 = @py_assert5.join
        @py_assert9 = 'xyz.zip'
        @py_assert11 = @py_assert7(@py_assert9)
        @py_assert3 = @py_assert1 == @py_assert11
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sdistsrc\n} == %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.distshare\n}.join\n}(%(py10)s)\n}', ), (@py_assert1, @py_assert11)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py10': @pytest_ar._saferepr(@py_assert9),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
        config = newconfig([], '')
        @py_assert1 = config.sdistsrc
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.sdistsrc\n}') % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None

    def test_env_selection(self, tmpdir, newconfig, monkeypatch):
        inisource = '\n            [tox]\n            envlist = py26\n            [testenv:py26]\n            basepython=python2.6\n            [testenv:py31]\n            basepython=python3.1\n            [testenv:py27]\n            basepython=python2.7\n        '
        config = newconfig([], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py26']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        config = newconfig(['-epy31'], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py31']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        monkeypatch.setenv('TOXENV', 'py31,py26')
        config = newconfig([], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py31', 'py26']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        monkeypatch.setenv('TOXENV', 'ALL')
        config = newconfig([], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py26', 'py27', 'py31']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        config = newconfig(['-eALL'], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py26', 'py27', 'py31']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_py_venv(self, tmpdir, newconfig, monkeypatch):
        config = newconfig(['-epy'], '')
        env = config.envconfigs['py']
        @py_assert2 = env.basepython
        @py_assert4 = str(@py_assert2)
        @py_assert8 = sys.executable
        @py_assert6 = @py_assert4 == @py_assert8
        if not @py_assert6:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.basepython\n})\n} == %(py9)s\n{%(py9)s = %(py7)s.executable\n}',), (@py_assert4, @py_assert8)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py9': @pytest_ar._saferepr(@py_assert8),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys'}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None

    def test_default_environments(self, tmpdir, newconfig, monkeypatch):
        envs = 'py26,py27,py32,py33,py34,py35,py36,jython,pypy,pypy3'
        inisource = '\n            [tox]\n            envlist = %s\n        ' % envs
        config = newconfig([], inisource)
        envlist = envs.split(',')
        @py_assert1 = config.envlist
        @py_assert3 = @py_assert1 == envlist
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py4)s', ), (@py_assert1, envlist)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(envlist) if 'envlist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envlist) else 'envlist',  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        for name in config.envlist:
            env = config.envconfigs[name]
            if name == 'jython':
                @py_assert1 = env.basepython
                @py_assert4 = 'jython'
                @py_assert3 = @py_assert1 == @py_assert4
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.basepython\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None
            elif name.startswith('pypy'):
                @py_assert1 = env.basepython
                @py_assert3 = @py_assert1 == name
                if not @py_assert3:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.basepython\n} == %(py4)s', ), (@py_assert1, name)) % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py4': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name',  'py2': @pytest_ar._saferepr(@py_assert1)}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = None
            else:
                @py_assert1 = name.startswith
                @py_assert3 = 'py'
                @py_assert5 = @py_assert1(@py_assert3)
                if not @py_assert5:
                    @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = @py_assert5 = None
                bp = 'python%s.%s' % (name[2], name[3])
                @py_assert1 = env.basepython
                @py_assert3 = @py_assert1 == bp
                if not @py_assert3:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.basepython\n} == %(py4)s', ), (@py_assert1, bp)) % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py4': @pytest_ar._saferepr(bp) if 'bp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bp) else 'bp',  'py2': @pytest_ar._saferepr(@py_assert1)}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = None

    def test_envlist_expansion(self, newconfig):
        inisource = '\n            [tox]\n            envlist = py{26,27},docs\n        '
        config = newconfig([], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py26', 'py27', 'docs']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_envlist_cross_product(self, newconfig):
        inisource = '\n            [tox]\n            envlist = py{26,27}-dep{1,2}\n        '
        config = newconfig([], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py26-dep1', 'py26-dep2', 'py27-dep1', 'py27-dep2']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_envlist_multiline(self, newconfig):
        inisource = '\n            [tox]\n            envlist =\n              py27\n              py34\n        '
        config = newconfig([], inisource)
        @py_assert1 = config.envlist
        @py_assert4 = [
         'py27', 'py34']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_minversion(self, tmpdir, newconfig, monkeypatch):
        inisource = '\n            [tox]\n            minversion = 3.0\n        '
        config = newconfig([], inisource)
        @py_assert1 = config.minversion
        @py_assert4 = '3.0'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.minversion\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_skip_missing_interpreters_true(self, tmpdir, newconfig, monkeypatch):
        inisource = '\n            [tox]\n            skip_missing_interpreters = True\n        '
        config = newconfig([], inisource)
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.skip_missing_interpreters
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.skip_missing_interpreters\n}') % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None

    def test_skip_missing_interpreters_false(self, tmpdir, newconfig, monkeypatch):
        inisource = '\n            [tox]\n            skip_missing_interpreters = False\n        '
        config = newconfig([], inisource)
        @py_assert1 = config.option
        @py_assert3 = @py_assert1.skip_missing_interpreters
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.option\n}.skip_missing_interpreters\n}') % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    def test_defaultenv_commandline(self, tmpdir, newconfig, monkeypatch):
        config = newconfig(['-epy27'], '')
        env = config.envconfigs['py27']
        @py_assert1 = env.basepython
        @py_assert4 = 'python2.7'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.basepython\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = env.commands
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.commands\n}') % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None

    def test_defaultenv_partial_override(self, tmpdir, newconfig, monkeypatch):
        inisource = '\n            [tox]\n            envlist = py27\n            [testenv:py27]\n            commands= xyz\n        '
        config = newconfig([], inisource)
        env = config.envconfigs['py27']
        @py_assert1 = env.basepython
        @py_assert4 = 'python2.7'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.basepython\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = env.commands
        @py_assert4 = [
         [
          'xyz']]
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.commands\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


class TestHashseedOption:

    def _get_envconfigs(self, newconfig, args=None, tox_ini=None, make_hashseed=None):
        if args is None:
            args = []
        if tox_ini is None:
            tox_ini = '\n                [testenv]\n            '
        if make_hashseed is None:
            make_hashseed = lambda : '123456789'
        original_make_hashseed = tox_plus.config.make_hashseed
        tox_plus.config.make_hashseed = make_hashseed
        try:
            config = newconfig(args, tox_ini)
        finally:
            tox_plus.config.make_hashseed = original_make_hashseed

        return config.envconfigs

    def _get_envconfig(self, newconfig, args=None, tox_ini=None):
        envconfigs = self._get_envconfigs(newconfig, args=args, tox_ini=tox_ini)
        return envconfigs['python']

    def _check_hashseed(self, envconfig, expected):
        @py_assert1 = envconfig.setenv
        @py_assert4 = {'PYTHONHASHSEED': expected}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.setenv\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def _check_testenv(self, newconfig, expected, args=None, tox_ini=None):
        envconfig = self._get_envconfig(newconfig, args=args, tox_ini=tox_ini)
        self._check_hashseed(envconfig, expected)

    def test_default(self, tmpdir, newconfig):
        self._check_testenv(newconfig, '123456789')

    def test_passing_integer(self, tmpdir, newconfig):
        args = [
         '--hashseed', '1']
        self._check_testenv(newconfig, '1', args=args)

    def test_passing_string(self, tmpdir, newconfig):
        args = [
         '--hashseed', 'random']
        self._check_testenv(newconfig, 'random', args=args)

    def test_passing_empty_string(self, tmpdir, newconfig):
        args = [
         '--hashseed', '']
        self._check_testenv(newconfig, '', args=args)

    @pytest.mark.xfail(sys.version_info >= (3, 2), reason='at least Debian python 3.2/3.3 have a bug: http://bugs.python.org/issue11884')
    def test_passing_no_argument(self, tmpdir, newconfig):
        """Test that passing no arguments to --hashseed is not allowed."""
        args = [
         '--hashseed']
        try:
            self._check_testenv(newconfig, '', args=args)
        except SystemExit:
            e = sys.exc_info()[1]
            @py_assert1 = e.code
            @py_assert4 = 2
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
            return

        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None

    def test_setenv(self, tmpdir, newconfig):
        """Check that setenv takes precedence."""
        tox_ini = '\n            [testenv]\n            setenv =\n                PYTHONHASHSEED = 2\n        '
        self._check_testenv(newconfig, '2', tox_ini=tox_ini)
        args = ['--hashseed', '1']
        self._check_testenv(newconfig, '2', args=args, tox_ini=tox_ini)

    def test_noset(self, tmpdir, newconfig):
        args = [
         '--hashseed', 'noset']
        envconfig = self._get_envconfig(newconfig, args=args)
        @py_assert1 = envconfig.setenv
        @py_assert4 = {}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.setenv\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(envconfig) if 'envconfig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envconfig) else 'envconfig',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_noset_with_setenv(self, tmpdir, newconfig):
        tox_ini = '\n            [testenv]\n            setenv =\n                PYTHONHASHSEED = 2\n        '
        args = ['--hashseed', 'noset']
        self._check_testenv(newconfig, '2', args=args, tox_ini=tox_ini)

    def test_one_random_hashseed(self, tmpdir, newconfig):
        """Check that different testenvs use the same random seed."""
        tox_ini = '\n            [testenv:hash1]\n            [testenv:hash2]\n        '
        next_seed = [1000]

        def make_hashseed():
            next_seed[0] += 1
            return str(next_seed[0])

        @py_assert1 = make_hashseed()
        @py_assert4 = '1001'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(make_hashseed) if 'make_hashseed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_hashseed) else 'make_hashseed',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        envconfigs = self._get_envconfigs(newconfig, tox_ini=tox_ini, make_hashseed=make_hashseed)
        self._check_hashseed(envconfigs['hash1'], '1002')
        self._check_hashseed(envconfigs['hash2'], '1002')

    def test_setenv_in_one_testenv(self, tmpdir, newconfig):
        """Check using setenv in one of multiple testenvs."""
        tox_ini = '\n            [testenv:hash1]\n            setenv =\n                PYTHONHASHSEED = 2\n            [testenv:hash2]\n        '
        envconfigs = self._get_envconfigs(newconfig, tox_ini=tox_ini)
        self._check_hashseed(envconfigs['hash1'], '2')
        self._check_hashseed(envconfigs['hash2'], '123456789')


class TestIndexServer:

    def test_indexserver(self, tmpdir, newconfig):
        config = newconfig('\n            [tox]\n            indexserver =\n                name1 = XYZ\n                name2 = ABC\n        ')
        @py_assert0 = config.indexserver['default']
        @py_assert2 = @py_assert0.url
        @py_assert5 = None
        @py_assert4 = @py_assert2 is @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = config.indexserver['name1']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'XYZ'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = config.indexserver['name2']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'ABC'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None

    def test_parse_indexserver(self, newconfig):
        inisource = '\n            [tox]\n            indexserver =\n                default = http://pypi.testrun.org\n                name1 = whatever\n        '
        config = newconfig([], inisource)
        @py_assert0 = config.indexserver['default']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'http://pypi.testrun.org'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = config.indexserver['name1']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'whatever'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        config = newconfig(['-i', 'qwe'], inisource)
        @py_assert0 = config.indexserver['default']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'qwe'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = config.indexserver['name1']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'whatever'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        config = newconfig(['-i', 'name1=abc', '-i', 'qwe2'], inisource)
        @py_assert0 = config.indexserver['default']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'qwe2'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = config.indexserver['name1']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'abc'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        config = newconfig(['-i', 'ALL=xzy'], inisource)
        @py_assert2 = config.indexserver
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.indexserver\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py8': @pytest_ar._saferepr(@py_assert7),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert0 = config.indexserver['default']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'xzy'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = config.indexserver['name1']
        @py_assert2 = @py_assert0.url
        @py_assert5 = 'xzy'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None

    def test_multiple_homedir_relative_local_indexservers(self, newconfig):
        inisource = '\n            [tox]\n            indexserver =\n                default = file://{homedir}/.pip/downloads/simple\n                local1  = file://{homedir}/.pip/downloads/simple\n                local2  = file://{toxinidir}/downloads/simple\n                pypi    = http://pypi.python.org/simple\n        '
        config = newconfig([], inisource)
        expected = 'file://%s/.pip/downloads/simple' % config.homedir
        @py_assert0 = config.indexserver['default']
        @py_assert2 = @py_assert0.url
        @py_assert4 = @py_assert2 == expected
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py5)s', ), (@py_assert2, expected)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py5': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = config.indexserver['local1']
        @py_assert2 = @py_assert0.url
        @py_assert5 = config.indexserver['default']
        @py_assert7 = @py_assert5.url
        @py_assert4 = @py_assert2 == @py_assert7
        if not @py_assert4:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.url\n} == %(py8)s\n{%(py8)s = %(py6)s.url\n}', ), (@py_assert2, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None


class TestParseEnv:

    def test_parse_recreate(self, newconfig):
        inisource = ''
        config = newconfig([], inisource)
        @py_assert0 = config.envconfigs['python']
        @py_assert2 = @py_assert0.recreate
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py1)s.recreate\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        config = newconfig(['--recreate'], inisource)
        @py_assert0 = config.envconfigs['python']
        @py_assert2 = @py_assert0.recreate
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py1)s.recreate\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert0 = @py_assert2 = None
        config = newconfig(['-r'], inisource)
        @py_assert0 = config.envconfigs['python']
        @py_assert2 = @py_assert0.recreate
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py1)s.recreate\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert0 = @py_assert2 = None
        inisource = '\n            [testenv:hello]\n            recreate = True\n        '
        config = newconfig([], inisource)
        @py_assert0 = config.envconfigs['hello']
        @py_assert2 = @py_assert0.recreate
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py1)s.recreate\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert0 = @py_assert2 = None


class TestCmdInvocation:

    def test_help(self, cmd):
        result = cmd.run('tox-plus', '-h')
        @py_assert1 = result.ret
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        result.stdout.fnmatch_lines([
         '*help*'])

    def test_version(self, cmd):
        result = cmd.run('tox-plus', '--version')
        @py_assert1 = result.ret
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        stdout = result.stdout.str()
        @py_assert1 = tox_plus.__version__
        @py_assert3 = @py_assert1 in stdout
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__version__\n} in %(py4)s', ), (@py_assert1, stdout)) % {'py0': @pytest_ar._saferepr(tox_plus) if 'tox_plus' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tox_plus) else 'tox_plus',  'py4': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout',  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert0 = 'imported from'
        @py_assert2 = @py_assert0 in stdout
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, stdout)) % {'py3': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_listenvs(self, cmd, initproj):
        initproj('listenvs', filedefs={'tox.ini': '\n            [tox]\n            envlist=py26,py27,py33,pypy,docs\n\n            [testenv:notincluded]\n            changedir = whatever\n\n            [testenv:docs]\n            changedir = docs\n            '})
        result = cmd.run('tox-plus', '-l')
        result.stdout.fnmatch_lines('\n            *py26*\n            *py27*\n            *py33*\n            *pypy*\n            *docs*\n        ')

    def test_config_specific_ini(self, tmpdir, cmd):
        ini = tmpdir.ensure('hello.ini')
        result = cmd.run('tox-plus', '-c', ini, '--showconfig')
        @py_assert1 = result.ret
        @py_assert3 = not @py_assert1
        if not @py_assert3:
            @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
        result.stdout.fnmatch_lines([
         '*config-file*hello.ini*'])

    def test_no_tox_ini(self, cmd, initproj):
        initproj('noini-0.5')
        result = cmd.run('tox-plus')
        @py_assert1 = result.ret
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ret\n}') % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
        result.stderr.fnmatch_lines([
         '*ERROR*tox.ini*not*found*'])

    def test_showconfig_with_force_dep_version(self, cmd, initproj):
        initproj('force_dep_version', filedefs={'tox.ini': '\n            [tox]\n\n            [testenv]\n            deps=\n                dep1==2.3\n                dep2\n            '})
        result = cmd.run('tox-plus', '--showconfig')
        @py_assert1 = result.ret
        @py_assert4 = 0
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        result.stdout.fnmatch_lines([
         '*deps*dep1==2.3, dep2*'])
        result = cmd.run('tox-plus', '--showconfig', '--force-dep=dep1', '--force-dep=dep2==5.0')
        @py_assert1 = result.ret
        @py_assert4 = 0
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ret\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        result.stdout.fnmatch_lines([
         '*deps*dep1, dep2==5.0*'])


@pytest.mark.parametrize('cmdline,envlist', [
 (
  '-e py26', ['py26']),
 (
  '-e py26,py33', ['py26', 'py33']),
 (
  '-e py26,py26', ['py26', 'py26']),
 (
  '-e py26,py33 -e py33,py27', ['py26', 'py33', 'py33', 'py27'])])
def test_env_spec(cmdline, envlist):
    args = cmdline.split()
    config = parseconfig(args)
    @py_assert1 = config.envlist
    @py_assert3 = @py_assert1 == envlist
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.envlist\n} == %(py4)s', ), (@py_assert1, envlist)) % {'py0': @pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py4': @pytest_ar._saferepr(envlist) if 'envlist' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(envlist) else 'envlist',  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


class TestCommandParser:

    def test_command_parser_for_word(self):
        p = CommandParser('word')
        @py_assert2 = p.words
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         'word']
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.words\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py10': @pytest_ar._saferepr(@py_assert9),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

    def test_command_parser_for_posargs(self):
        p = CommandParser('[]')
        @py_assert2 = p.words
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         '[]']
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.words\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py10': @pytest_ar._saferepr(@py_assert9),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

    def test_command_parser_for_multiple_words(self):
        p = CommandParser('w1 w2 w3 ')
        @py_assert2 = p.words
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         'w1', ' ', 'w2', ' ', 'w3']
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.words\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py10': @pytest_ar._saferepr(@py_assert9),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

    def test_command_parser_for_substitution_with_spaces(self):
        p = CommandParser('{sub:something with spaces}')
        @py_assert2 = p.words
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         '{sub:something with spaces}']
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.words\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py10': @pytest_ar._saferepr(@py_assert9),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

    def test_command_parser_with_complex_word_set(self):
        complex_case = 'word [] [literal] {something} {some:other thing} w{ord} w{or}d w{ord} w{o:rd} w{o:r}d {w:or}d w[]ord {posargs:{a key}}'
        p = CommandParser(complex_case)
        parsed = list(p.words())
        expected = [
         'word', ' ', '[]', ' ', '[literal]', ' ', '{something}', ' ', '{some:other thing}',
         ' ', 'w', '{ord}', ' ', 'w', '{or}', 'd', ' ', 'w', '{ord}', ' ', 'w', '{o:rd}', ' ',
         'w', '{o:r}', 'd', ' ', '{w:or}', 'd',
         ' ', 'w[]ord', ' ', '{posargs:{a key}}']
        @py_assert1 = parsed == expected
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (parsed, expected)) % {'py0': @pytest_ar._saferepr(parsed) if 'parsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed) else 'parsed',  'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_command_with_runs_of_whitespace(self):
        cmd = 'cmd1 {item1}\n  {item2}'
        p = CommandParser(cmd)
        parsed = list(p.words())
        @py_assert2 = ['cmd1', ' ', '{item1}', '\n  ', '{item2}']
        @py_assert1 = parsed == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (parsed, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(parsed) if 'parsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed) else 'parsed'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_command_with_split_line_in_subst_arguments(self):
        cmd = dedent(' cmd2 {posargs:{item2}\n                         other}')
        p = CommandParser(cmd)
        parsed = list(p.words())
        @py_assert2 = ['cmd2', ' ', '{posargs:{item2}\n                        other}']
        @py_assert1 = parsed == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (parsed, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(parsed) if 'parsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed) else 'parsed'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_command_parsing_for_issue_10(self):
        cmd = 'nosetests -v -a !deferred --with-doctest []'
        p = CommandParser(cmd)
        parsed = list(p.words())
        @py_assert2 = ['nosetests', ' ', '-v', ' ', '-a', ' ', '!deferred', ' ', '--with-doctest', ' ', '[]']
        @py_assert1 = parsed == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (parsed, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(parsed) if 'parsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed) else 'parsed'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    @pytest.mark.skipif("sys.platform != 'win32'")
    def test_commands_with_backslash(self, newconfig):
        config = newconfig(['hello\\world'], '\n            [testenv:py26]\n            commands = some {posargs}\n        ')
        envconfig = config.envconfigs['py26']
        @py_assert0 = envconfig.commands[0]
        @py_assert3 = [
         'some', 'hello\\world']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
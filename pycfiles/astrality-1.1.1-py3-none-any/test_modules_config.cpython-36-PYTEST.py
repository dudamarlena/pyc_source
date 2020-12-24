# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/config/test_modules_config.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 19303 bytes
"""Test module for global module configuration options."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging, time
from pathlib import Path
import pytest
from astrality.exceptions import NonExistentEnabledModule
from astrality.config import DirectoryModuleSource, EnabledModules, GithubModuleSource, GlobalModuleSource, GlobalModulesConfig, ModuleSource
from astrality.tests.utils import RegexCompare
from astrality.utils import run_shell

@pytest.fixture
def modules_application_config():
    return {'modules_directory':'test_modules', 
     'enabled_modules':[
      {'name':'oslo', 
       'safe':False},
      {'name': 'trondheim'}]}


def test_custom_modules_folder(conf_path):
    modules_config = GlobalModulesConfig(config={'modules_directory': 'test_modules'},
      config_directory=conf_path)
    @py_assert1 = modules_config.modules_directory
    @py_assert5 = 'test_modules'
    @py_assert7 = conf_path / @py_assert5
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.modules_directory\n} == (%(py4)s / %(py6)s)', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(modules_config) if 'modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modules_config) else 'modules_config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(conf_path) if 'conf_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf_path) else 'conf_path',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_enabled_modules(test_config_directory):
    modules_config = GlobalModulesConfig({'modules_directory':'test_modules', 
     'enabled_modules':[
      {'name':'oslo::*', 
       'safe':True},
      {'name': 'trondheim::*'}]},
      config_directory=test_config_directory)
    modules_directory_path = test_config_directory / 'test_modules'
    oslo = DirectoryModuleSource(enabling_statement={'name':'oslo::*', 
     'trusted':True},
      modules_directory=modules_directory_path)
    trondheim = DirectoryModuleSource(enabling_statement={'name':'trondheim::*', 
     'trusted':False},
      modules_directory=modules_directory_path)
    @py_assert3 = modules_config.external_module_sources
    @py_assert5 = tuple(@py_assert3)
    @py_assert7 = len(@py_assert5)
    @py_assert10 = 2
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py4)s\n{%(py4)s = %(py2)s.external_module_sources\n})\n})\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py2':@pytest_ar._saferepr(modules_config) if 'modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modules_config) else 'modules_config',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert4 = modules_config.external_module_sources
    @py_assert6 = tuple(@py_assert4)
    @py_assert1 = oslo in @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py7)s\n{%(py7)s = %(py2)s(%(py5)s\n{%(py5)s = %(py3)s.external_module_sources\n})\n}', ), (oslo, @py_assert6)) % {'py0':@pytest_ar._saferepr(oslo) if 'oslo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oslo) else 'oslo',  'py2':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py3':@pytest_ar._saferepr(modules_config) if 'modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modules_config) else 'modules_config',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert4 = modules_config.external_module_sources
    @py_assert6 = tuple(@py_assert4)
    @py_assert1 = trondheim in @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py7)s\n{%(py7)s = %(py2)s(%(py5)s\n{%(py5)s = %(py3)s.external_module_sources\n})\n}', ), (trondheim, @py_assert6)) % {'py0':@pytest_ar._saferepr(trondheim) if 'trondheim' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(trondheim) else 'trondheim',  'py2':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py3':@pytest_ar._saferepr(modules_config) if 'modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modules_config) else 'modules_config',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_external_module(test_config_directory):
    modules_directory_path = test_config_directory / 'test_modules'
    oslo = DirectoryModuleSource(enabling_statement={'name': 'oslo::*'},
      modules_directory=modules_directory_path)
    oslo_path = test_config_directory / 'test_modules' / 'oslo'
    @py_assert1 = oslo.directory
    @py_assert3 = @py_assert1 == oslo_path
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.directory\n} == %(py4)s', ), (@py_assert1, oslo_path)) % {'py0':@pytest_ar._saferepr(oslo) if 'oslo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oslo) else 'oslo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(oslo_path) if 'oslo_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oslo_path) else 'oslo_path'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = oslo.trusted
    @py_assert4 = True
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.trusted\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(oslo) if 'oslo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oslo) else 'oslo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = oslo.relative_directory_path
    @py_assert5 = 'oslo'
    @py_assert7 = Path(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.relative_directory_path\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(oslo) if 'oslo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oslo) else 'oslo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = oslo.modules_file
    @py_assert5 = 'modules.yml'
    @py_assert7 = oslo_path / @py_assert5
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.modules_file\n} == (%(py4)s / %(py6)s)', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(oslo) if 'oslo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oslo) else 'oslo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(oslo_path) if 'oslo_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oslo_path) else 'oslo_path',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_retrieval_of_external_module_config(test_config_directory):
    external_module_source_config = {'name': 'burma::*'}
    external_module_source = DirectoryModuleSource(enabling_statement=external_module_source_config,
      modules_directory=(test_config_directory / 'test_modules'))
    @py_assert1 = external_module_source.modules
    @py_assert3 = {}
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = {'burma::burma': {'enabled':True,  'safe':False}}
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.modules\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(external_module_source) if 'external_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(external_module_source) else 'external_module_source',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


class TestModuleSource:

    def test_finding_correct_module_source_type_from_name(self):
        @py_assert1 = ModuleSource.type
        @py_assert3 = 'name'
        @py_assert5 = @py_assert1(of=@py_assert3)
        @py_assert7 = @py_assert5 == GlobalModuleSource
        if not @py_assert7:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}(of=%(py4)s)\n} == %(py8)s', ), (@py_assert5, GlobalModuleSource)) % {'py0':@pytest_ar._saferepr(ModuleSource) if 'ModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ModuleSource) else 'ModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = ModuleSource.type
        @py_assert3 = 'category::name'
        @py_assert5 = @py_assert1(of=@py_assert3)
        @py_assert7 = @py_assert5 == DirectoryModuleSource
        if not @py_assert7:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}(of=%(py4)s)\n} == %(py8)s', ), (@py_assert5, DirectoryModuleSource)) % {'py0':@pytest_ar._saferepr(ModuleSource) if 'ModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ModuleSource) else 'ModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = ModuleSource.type
        @py_assert3 = 'github::user/repo'
        @py_assert5 = @py_assert1(of=@py_assert3)
        @py_assert7 = @py_assert5 == GithubModuleSource
        if not @py_assert7:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}(of=%(py4)s)\n} == %(py8)s', ), (@py_assert5, GithubModuleSource)) % {'py0':@pytest_ar._saferepr(ModuleSource) if 'ModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ModuleSource) else 'ModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = ModuleSource.type
        @py_assert3 = 'github::user/repo::module'
        @py_assert5 = @py_assert1(of=@py_assert3)
        @py_assert7 = @py_assert5 == GithubModuleSource
        if not @py_assert7:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}(of=%(py4)s)\n} == %(py8)s', ), (@py_assert5, GithubModuleSource)) % {'py0':@pytest_ar._saferepr(ModuleSource) if 'ModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ModuleSource) else 'ModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = ModuleSource.type
        @py_assert3 = 'github::user/repo::*'
        @py_assert5 = @py_assert1(of=@py_assert3)
        @py_assert7 = @py_assert5 == GithubModuleSource
        if not @py_assert7:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.type\n}(of=%(py4)s)\n} == %(py8)s', ), (@py_assert5, GithubModuleSource)) % {'py0':@pytest_ar._saferepr(ModuleSource) if 'ModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ModuleSource) else 'ModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource'}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_detection_of_all_module_directories_within_a_directory(self, test_config_directory):
        @py_assert3 = EnabledModules.module_directories
        @py_assert6 = 'freezed_modules'
        @py_assert8 = test_config_directory / @py_assert6
        @py_assert9 = @py_assert3(within=@py_assert8)
        @py_assert11 = tuple(@py_assert9)
        @py_assert13 = sorted(@py_assert11)
        @py_assert17 = (
         'north_america', 'south_america')
        @py_assert19 = sorted(@py_assert17)
        @py_assert15 = @py_assert13 == @py_assert19
        if not @py_assert15:
            @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py1)s(%(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py2)s.module_directories\n}(within=(%(py5)s / %(py7)s))\n})\n})\n} == %(py20)s\n{%(py20)s = %(py16)s(%(py18)s)\n}',), (@py_assert13, @py_assert19)) % {'py0':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py1':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py2':@pytest_ar._saferepr(EnabledModules) if 'EnabledModules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(EnabledModules) else 'EnabledModules',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19)}
            @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
            raise AssertionError(@pytest_ar._format_explanation(@py_format23))
        @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = None


class TestDirectoryModuleSource:
    __doc__ = 'Test of object responsible for module(s) defined in a directory.'

    def test_which_enabling_statements_represents_directory_module_sources(self):
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = 'category::name'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = 'category/recursive::name'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = 'category::*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = '*::*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = 'category::*not_valid'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = 'category::not_valid*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = 'name'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = DirectoryModuleSource.represented_by
        @py_assert3 = '*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(DirectoryModuleSource) if 'DirectoryModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DirectoryModuleSource) else 'DirectoryModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_error_on_enabling_non_existent_module(self, test_config_directory):
        enabling_statement = {'name': 'north_america::colombia'}
        with pytest.raises(NonExistentEnabledModule):
            directory_module = DirectoryModuleSource(enabling_statement=enabling_statement,
              modules_directory=(test_config_directory / 'freezed_modules'))
            directory_module.modules({})

    def test_recursive_module_directory(self, test_config_directory):
        enabling_statement = {'name': 'recursive/directory::bulgaria'}
        directory_module = DirectoryModuleSource(enabling_statement=enabling_statement,
          modules_directory=(test_config_directory / 'test_modules'))
        @py_assert1 = directory_module.modules
        @py_assert3 = {}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = {'recursive/directory::bulgaria': {'on_startup': {'run': "echo 'Greetings from Bulgaria!'"}}}
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.modules\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None

    def test_getting_config_dict_from_directory_module(self, test_config_directory):
        enabling_statement = {'name': 'north_america::USA'}
        directory_module = DirectoryModuleSource(enabling_statement=enabling_statement,
          modules_directory=(test_config_directory / 'freezed_modules'))
        @py_assert1 = directory_module.modules
        @py_assert3 = {}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = {'north_america::USA': {'on_startup': {'run': 'echo Greetings from the USA!'}}}
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.modules\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = directory_module.context
        @py_assert3 = {}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = {'geography': {'USA': {'capitol': 'Washington D.C.'}}}
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.context\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None

    def test_enabling_just_one_module_in_diretory(self, test_config_directory):
        enabling_statement = {'name': 'south_america::brazil'}
        directory_module = DirectoryModuleSource(enabling_statement=enabling_statement,
          modules_directory=(test_config_directory / 'freezed_modules'))
        @py_assert1 = directory_module.modules
        @py_assert3 = {}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = {'south_america::brazil': {'on_startup': {'run': 'echo Greetings from Brazil!'}}}
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.modules\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = directory_module.context
        @py_assert3 = {}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = {'geography': {'brazil':{'capitol': 'Brasilia'},  'argentina':{'capitol': 'Buenos Aires'}}}
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.context\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None

    def test_checking_if_directory_modules_contain_module_name(self, test_config_directory):
        enabling_statement = {'name': 'south_america::brazil'}
        directory_module = DirectoryModuleSource(enabling_statement=enabling_statement,
          modules_directory=(test_config_directory / 'freezed_modules'))
        directory_module.modules({})
        @py_assert0 = 'south_america::brazil'
        @py_assert2 = @py_assert0 in directory_module
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, directory_module)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'south_america::argentina'
        @py_assert2 = @py_assert0 not in directory_module
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, directory_module)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'brazil'
        @py_assert2 = @py_assert0 not in directory_module
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, directory_module)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'argentina'
        @py_assert2 = @py_assert0 not in directory_module
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, directory_module)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(directory_module) if 'directory_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory_module) else 'directory_module'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


class TestGlobalModuleSource:

    def test_valid_names_which_indicate_globally_defined_modules(self):
        @py_assert1 = GlobalModuleSource.represented_by
        @py_assert3 = 'module_name'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = GlobalModuleSource.represented_by
        @py_assert3 = '*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = GlobalModuleSource.represented_by
        @py_assert3 = 'w*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GlobalModuleSource.represented_by
        @py_assert3 = 'category::name'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GlobalModuleSource.represented_by
        @py_assert3 = 'category::*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GlobalModuleSource.represented_by
        @py_assert3 = '*::*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GlobalModuleSource.represented_by
        @py_assert3 = 'jakobgm/module'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GlobalModuleSource) if 'GlobalModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GlobalModuleSource) else 'GlobalModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_that_enabled_modules_are_detected_correctly(self):
        global_module_source = GlobalModuleSource(enabling_statement={'name': 'enabled_module'},
          modules_directory=(Path('/')))
        global_module_source.modules({})
        @py_assert0 = 'enabled_module'
        @py_assert2 = @py_assert0 in global_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, global_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_module_source) if 'global_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_module_source) else 'global_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'disabled_module'
        @py_assert2 = @py_assert0 not in global_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, global_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_module_source) if 'global_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_module_source) else 'global_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '*'
        @py_assert2 = @py_assert0 not in global_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, global_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_module_source) if 'global_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_module_source) else 'global_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_that_wildcard_global_enabling_enables_all_global_modules(self):
        global_module_source = GlobalModuleSource(enabling_statement={'name': '*'},
          modules_directory=(Path('/')))
        @py_assert0 = 'enabled_module1'
        @py_assert2 = @py_assert0 in global_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, global_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_module_source) if 'global_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_module_source) else 'global_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'enabled_module2'
        @py_assert2 = @py_assert0 in global_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, global_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_module_source) if 'global_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_module_source) else 'global_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'directory::module'
        @py_assert2 = @py_assert0 not in global_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, global_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_module_source) if 'global_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_module_source) else 'global_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'user/repo'
        @py_assert2 = @py_assert0 not in global_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, global_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_module_source) if 'global_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_module_source) else 'global_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


class TestGithubModuleSource:

    def test_valid_names_which_indicate_github_modules(self):
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'github::jakobgm/astrality'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'github::jakobgm/astrality::module'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'github::jakobgm/astrality::*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'github::user_name./repo-git.ast'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'w*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'category::name'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'category::*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = '*::*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = '*'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = GithubModuleSource.represented_by
        @py_assert3 = 'global_module'
        @py_assert5 = @py_assert1(module_name=@py_assert3)
        @py_assert7 = not @py_assert5
        if not @py_assert7:
            @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.represented_by\n}(module_name=%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(GithubModuleSource) if 'GithubModuleSource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(GithubModuleSource) else 'GithubModuleSource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    @pytest.mark.slow
    def test_that_username_and_repo_is_identified(self, tmpdir):
        modules_directory = Path(tmpdir)
        github_module_source = GithubModuleSource(enabling_statement={'name': 'github::jakobgm/astrality'},
          modules_directory=modules_directory)
        @py_assert1 = github_module_source.github_user
        @py_assert4 = 'jakobgm'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.github_user\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = github_module_source.github_repo
        @py_assert4 = 'astrality'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.github_repo\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    @pytest.mark.slow
    def test_that_enabled_repos_are_found(self, test_config_directory):
        github_module_source = GithubModuleSource(enabling_statement={'name': 'github::jakobgm/test-module.astrality'},
          modules_directory=(test_config_directory / 'test_modules'))
        github_module_source.config({})
        @py_assert0 = 'github::jakobgm/test-module.astrality::botswana'
        @py_assert2 = @py_assert0 in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::jakobgm/test-module.astrality::ghana'
        @py_assert2 = @py_assert0 in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::jakobgm/test-module.astrality::non_existent'
        @py_assert2 = @py_assert0 not in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::jakobgm/another_repo::ghana'
        @py_assert2 = @py_assert0 not in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'astrality'
        @py_assert2 = @py_assert0 not in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'jakobgm'
        @py_assert2 = @py_assert0 not in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    @pytest.mark.slow
    def test_specific_github_modules_enabled(self, test_config_directory):
        github_module_source = GithubModuleSource(enabling_statement={'name': 'github::jakobgm/test-module.astrality::botswana'},
          modules_directory=(test_config_directory / 'test_modules'))
        github_module_source.config({})
        @py_assert0 = 'github::jakobgm/test-module.astrality::botswana'
        @py_assert2 = @py_assert0 in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::jakobgm/test-module.astrality::ghana'
        @py_assert2 = @py_assert0 not in github_module_source
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, github_module_source)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    @pytest.mark.slow
    def test_that_all_modules_enabled_syntaxes_behave_identically(self, test_config_directory):
        github_module_source1 = GithubModuleSource(enabling_statement={'name': 'github::jakobgm/test-module.astrality'},
          modules_directory=(test_config_directory / 'test_modules'))
        github_module_source1.config({})
        time.sleep(1)
        github_module_source2 = GithubModuleSource(enabling_statement={'name': 'github::jakobgm/test-module.astrality::*'},
          modules_directory=(test_config_directory / 'test_modules'))
        github_module_source2.config({})
        @py_assert1 = github_module_source1 == github_module_source2
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (github_module_source1, github_module_source2)) % {'py0':@pytest_ar._saferepr(github_module_source1) if 'github_module_source1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source1) else 'github_module_source1',  'py2':@pytest_ar._saferepr(github_module_source2) if 'github_module_source2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source2) else 'github_module_source2'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    @pytest.mark.slow
    def test_automatical_retrival_of_github_module(self, tmpdir):
        modules_directory = Path(tmpdir)
        github_module_source = GithubModuleSource(enabling_statement={'name':'github::jakobgm/test-module.astrality::*', 
         'autoupdate':True},
          modules_directory=modules_directory)
        @py_assert1 = github_module_source.modules
        @py_assert3 = {}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = {'github::jakobgm/test-module.astrality::botswana':{'on_startup': {'run': "echo 'Greetings from Botswana!'"}}, 
         'github::jakobgm/test-module.astrality::ghana':{'on_startup': {'run': "echo 'Greetings from Ghana!'"}}}
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.modules\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = github_module_source.context
        @py_assert3 = {}
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = {'geography': {'botswana':{'capitol': 'Gaborone'},  'ghana':{'capitol': 'Accra'}}}
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.context\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(github_module_source) if 'github_module_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(github_module_source) else 'github_module_source',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None

    @pytest.mark.slow
    def test_use_of_autoupdating_github_source(self, patch_xdg_directory_standard):
        """When autoupdate is True, the latest revision should be pulled."""
        github_module_source = GithubModuleSource(enabling_statement={'name':'github::jakobgm/test-module.astrality', 
         'autoupdate':True},
          modules_directory=(Path('/what/ever')))
        github_module_source.modules({})
        repo_dir = patch_xdg_directory_standard / 'repositories/github/jakobgm/test-module.astrality'
        @py_assert1 = repo_dir.is_dir
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(repo_dir) if 'repo_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo_dir) else 'repo_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        result = run_shell(command='git reset --hard d4c9723',
          timeout=5,
          fallback=False,
          working_directory=repo_dir)
        @py_assert2 = False
        @py_assert1 = result is not @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        readme = repo_dir / 'README.rst'
        @py_assert1 = readme.is_file
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(readme) if 'readme' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(readme) else 'readme',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        del github_module_source
        github_module_source = GithubModuleSource(enabling_statement={'name':'github::jakobgm/test-module.astrality', 
         'autoupdate':True},
          modules_directory=(Path('/what/ever')))
        github_module_source.modules({})
        @py_assert1 = readme.is_file
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(readme) if 'readme' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(readme) else 'readme',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None


class TestEnabledModules:

    def test_processing_of_enabled_statements(self, test_config_directory):
        enabled_modules = EnabledModules([], Path('/'), Path('/'))
        enabled = sorted(map(lambda x: tuple(x.items()), enabled_modules.process_enabling_statements(enabling_statements=[
         {'name': '*::*'}],
          modules_directory=(test_config_directory / 'freezed_modules'))))
        expected = sorted(map(lambda x: tuple(x.items()), [
         {'name': 'north_america::*'}, {'name': 'south_america::*'}]))
        @py_assert1 = enabled == expected
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (enabled, expected)) % {'py0':@pytest_ar._saferepr(enabled) if 'enabled' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled) else 'enabled',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = enabled_modules.all_directory_modules_enabled
        @py_assert4 = True
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.all_directory_modules_enabled\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = enabled_modules.all_global_modules_enabled
        @py_assert4 = False
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.all_global_modules_enabled\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    @pytest.mark.slow
    def test_enabled_detection(self, test_config_directory, caplog):
        enabling_statements = [
         {'name': 'global'},
         {'name': 'south_america::*'},
         {'name': 'github::jakobgm/test-module.astrality'},
         {'name': 'invalid_syntax]][['}]
        enabled_modules = EnabledModules(enabling_statements=enabling_statements,
          config_directory=test_config_directory,
          modules_directory=(test_config_directory / 'freezed_modules'))
        for sources in enabled_modules.source_types.values():
            @py_assert2 = len(sources)
            @py_assert5 = 1
            @py_assert4 = @py_assert2 == @py_assert5
            if not @py_assert4:
                @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(sources) if 'sources' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sources) else 'sources',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
                @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert2 = @py_assert4 = @py_assert5 = None

        @py_assert0 = (
         'astrality.config', logging.ERROR, RegexCompare('Invalid module name syntax.+'))
        @py_assert4 = caplog.record_tuples
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        enabled_modules.compile_config_files({})
        @py_assert0 = 'global'
        @py_assert2 = @py_assert0 in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'south_america::brazil'
        @py_assert2 = @py_assert0 in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'south_america::argentina'
        @py_assert2 = @py_assert0 in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::jakobgm/test-module.astrality::botswana'
        @py_assert2 = @py_assert0 in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::jakobgm/test-module.astrality::ghana'
        @py_assert2 = @py_assert0 in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'not_enabled'
        @py_assert2 = @py_assert0 not in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'non_existing_folder::non_existing_module'
        @py_assert2 = @py_assert0 not in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::user/not_enabled'
        @py_assert2 = @py_assert0 not in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_enabled_detection_with_global_wildcard(self):
        enabling_statements = [
         {'name': '*'}]
        enabled_modules = EnabledModules(enabling_statements=enabling_statements,
          config_directory=(Path('/')),
          modules_directory=(Path('/')))
        @py_assert0 = 'global'
        @py_assert2 = @py_assert0 in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'whatever'
        @py_assert2 = @py_assert0 in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'south_america::brazil'
        @py_assert2 = @py_assert0 not in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'south_america::argentina'
        @py_assert2 = @py_assert0 not in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'github::jakobgm/color_schemes.astrality'
        @py_assert2 = @py_assert0 not in enabled_modules
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, enabled_modules)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(enabled_modules) if 'enabled_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(enabled_modules) else 'enabled_modules'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
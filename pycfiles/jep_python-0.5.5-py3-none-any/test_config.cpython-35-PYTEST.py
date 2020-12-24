# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\test_config.py
# Compiled at: 2016-01-04 11:02:19
# Size of source mod 2**32: 2642 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from jep_py.config import ServiceConfigProvider, ServiceConfig
from test.logconfig import configure_test_logger

def setup_function(function):
    configure_test_logger()
    os.chdir(os.path.join(os.path.dirname(__file__), 'input'))


def test_service_config_provider():
    provider = ServiceConfigProvider()
    sc = provider.provide_for('test/test.rb')
    @py_assert1 = sc.command
    @py_assert4 = 'ruby-command'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = sc.config_file_path
    @py_assert8 = @py_assert3(@py_assert6)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py7)s\n{%(py7)s = %(py5)s.config_file_path\n})\n}') % {'py5': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = sc.checksum
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.checksum\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    sc = provider.provide_for('test/test.ruby')
    @py_assert1 = sc.command
    @py_assert4 = 'ruby-command'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = sc.config_file_path
    @py_assert8 = @py_assert3(@py_assert6)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py7)s\n{%(py7)s = %(py5)s.config_file_path\n})\n}') % {'py5': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    sc = provider.provide_for('test/test.ruby2')
    @py_assert1 = sc.command
    @py_assert4 = 'ruby-command'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = sc.config_file_path
    @py_assert8 = @py_assert3(@py_assert6)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py7)s\n{%(py7)s = %(py5)s.config_file_path\n})\n}') % {'py5': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    sc = provider.provide_for('other-folder/test.c')
    @py_assert1 = sc.command
    @py_assert4 = 'c-command'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = sc.config_file_path
    @py_assert8 = @py_assert3(@py_assert6)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py7)s\n{%(py7)s = %(py5)s.config_file_path\n})\n}') % {'py5': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    sc = provider.provide_for('other-folder/fullname')
    @py_assert1 = sc.command
    @py_assert4 = 'fullname-command'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    sc = provider.provide_for('CMakeLists.txt')
    @py_assert1 = sc.command
    @py_assert4 = 'jep-cmake'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    sc = provider.provide_for('other-folder/CMakeLists.txt')
    @py_assert1 = sc.command
    @py_assert4 = 'jep-cmake'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.command\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_service_config_provider_failed_extension():
    provider = ServiceConfigProvider()
    sc = provider.provide_for('test/test.unknown')
    @py_assert2 = None
    @py_assert1 = sc is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (sc, @py_assert2)) % {'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_service_config_provider_failed_config_file():
    os.chdir('..')
    provider = ServiceConfigProvider()
    sc = provider.provide_for('test/test.rb')
    @py_assert2 = None
    @py_assert1 = sc is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (sc, @py_assert2)) % {'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_service_config_provider_from_subfolders():
    os.chdir('sub1')
    provider = ServiceConfigProvider()
    @py_assert1 = provider.provide_for
    @py_assert3 = 'test/test.rb'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.provide_for\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(provider) if 'provider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(provider) else 'provider', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    os.chdir('sub2')
    @py_assert1 = provider.provide_for
    @py_assert3 = 'test/test.rb'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.provide_for\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(provider) if 'provider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(provider) else 'provider', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_service_config_selector():
    sc1 = ServiceConfig('path1', ['*.txt'], 'doit.exe', '1234')
    sc2 = ServiceConfig('path1', ['*.txt'], 'doit.exe', '1234')
    sc3 = ServiceConfig('path2', ['*.txt'], 'doit.exe', '1234')
    sc4 = ServiceConfig('path1', ['*.doc'], 'doit.exe', '1234')
    @py_assert1 = sc1.selector
    @py_assert5 = sc2.selector
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.selector\n} == %(py6)s\n{%(py6)s = %(py4)s.selector\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc1) if 'sc1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc1) else 'sc1', 'py4': @pytest_ar._saferepr(sc2) if 'sc2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc2) else 'sc2', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = sc1.selector
    @py_assert5 = sc3.selector
    @py_assert3 = @py_assert1 == @py_assert5
    @py_assert9 = not @py_assert3
    if not @py_assert9:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.selector\n} == %(py6)s\n{%(py6)s = %(py4)s.selector\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc1) if 'sc1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc1) else 'sc1', 'py4': @pytest_ar._saferepr(sc3) if 'sc3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc3) else 'sc3', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format10 = 'assert not %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert9 = None
    @py_assert1 = sc2.selector
    @py_assert5 = sc4.selector
    @py_assert3 = @py_assert1 == @py_assert5
    @py_assert9 = not @py_assert3
    if not @py_assert9:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.selector\n} == %(py6)s\n{%(py6)s = %(py4)s.selector\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc2) if 'sc2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc2) else 'sc2', 'py4': @pytest_ar._saferepr(sc4) if 'sc4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc4) else 'sc4', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format10 = 'assert not %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert9 = None


def test_service_config_provider_checksum():
    provider = ServiceConfigProvider()
    sc = provider.provide_for('test/test.rb')
    @py_assert1 = sc.checksum
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.checksum\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = provider.checksum
    @py_assert3 = '.jep'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = sc.checksum
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.checksum\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.checksum\n}', ), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(provider) if 'provider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(provider) else 'provider', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = provider.checksum
    @py_assert3 = 'other-jep'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = sc.checksum
    @py_assert7 = @py_assert5 == @py_assert9
    @py_assert13 = not @py_assert7
    if not @py_assert13:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.checksum\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.checksum\n}', ), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(provider) if 'provider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(provider) else 'provider', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(sc) if 'sc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sc) else 'sc', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert not %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = None
    @py_assert1 = provider.checksum
    @py_assert3 = 'not-existing-file'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = None
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.checksum\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(provider) if 'provider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(provider) else 'provider', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
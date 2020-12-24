# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Edd\Workspace\python\ethronsoft\gcspypi\test\package_manager_test.py
# Compiled at: 2018-07-15 07:17:56
# Size of source mod 2**32: 11734 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from .mocks.mock_repository import MockRepository as Repository
from .mocks.mock_installer import MockInstaller as Installer
from ethronsoft.gcspypi.package.package_manager import PackageManager, Package
from ethronsoft.gcspypi.exceptions import InvalidParameter, InvalidState
from ethronsoft.gcspypi.utilities.console import Console
from pkg_resources import resource_filename
import pytest, tempfile, shutil, os, hashlib

def test_init():
    pm = PackageManager(repo=(Repository()), installer=(Installer()), console=Console(exit_on_error=False))
    @py_assert0 = [x for x in pm.list_items()]
    @py_assert3 = []
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_upload_download():
    pm = PackageManager(repo=(Repository()), installer=(Installer()), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    wrong = Package(name='test_package', version='')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    with pytest.raises(InvalidParameter):
        pm.upload(wrong, filename)
    pm.upload(pkg, filename)
    pm.list_items() == [Package.repo_name(pkg, filename)]
    pm.list_items(from_cache=True) == [Package.repo_name(pkg, filename)]
    with pytest.raises(InvalidState):
        pm.upload(pkg, filename)
    try:
        tdir = tempfile.mkdtemp()
        @py_assert1 = pm.download_by_name
        @py_assert3 = 'fake'
        @py_assert6 = @py_assert1(@py_assert3, tdir)
        @py_assert8 = not @py_assert6
        if not @py_assert8:
            @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.download_by_name\n}(%(py4)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(tdir) if 'tdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tdir) else 'tdir',  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
        @py_assert1 = pm.download_by_name
        @py_assert4 = Package.repo_name
        @py_assert7 = 'test_package'
        @py_assert9 = '2.0.0'
        @py_assert11 = 'SOURCE'
        @py_assert13 = Package(name=@py_assert7, version=@py_assert9, type=@py_assert11)
        @py_assert16 = @py_assert4(@py_assert13, filename)
        @py_assert19 = @py_assert1(@py_assert16, tdir)
        @py_assert21 = not @py_assert19
        if not @py_assert21:
            @py_format22 = ('' + 'assert not %(py20)s\n{%(py20)s = %(py2)s\n{%(py2)s = %(py0)s.download_by_name\n}(%(py17)s\n{%(py17)s = %(py5)s\n{%(py5)s = %(py3)s.repo_name\n}(%(py14)s\n{%(py14)s = %(py6)s(name=%(py8)s, version=%(py10)s, type=%(py12)s)\n}, %(py15)s)\n}, %(py18)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py15':@pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename',  'py17':@pytest_ar._saferepr(@py_assert16),  'py18':@pytest_ar._saferepr(tdir) if 'tdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tdir) else 'tdir',  'py20':@pytest_ar._saferepr(@py_assert19)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format22))
        @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert16 = @py_assert19 = @py_assert21 = None
        dest = pm.download_by_name(Package.repo_name(pkg, filename), tdir)
        source_md5 = hashlib.md5()
        with open(filename, 'rb') as (f):
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, 'rb') as (f):
            dest_md5.update(f.read())
        @py_assert1 = source_md5.hexdigest
        @py_assert3 = @py_assert1()
        @py_assert7 = dest_md5.hexdigest
        @py_assert9 = @py_assert7()
        @py_assert5 = @py_assert3 == @py_assert9
        if not @py_assert5:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.hexdigest\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.hexdigest\n}()\n}',), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(source_md5) if 'source_md5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_md5) else 'source_md5',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(dest_md5) if 'dest_md5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_md5) else 'dest_md5',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    finally:
        shutil.rmtree(tdir)

    try:
        tdir = tempfile.mkdtemp()
        @py_assert1 = pm.download
        @py_assert4 = 'fake'
        @py_assert6 = ''
        @py_assert8 = 'SOURCE'
        @py_assert10 = Package(name=@py_assert4, version=@py_assert6, type=@py_assert8)
        @py_assert13 = 'SOURCE'
        @py_assert15 = @py_assert1(@py_assert10, tdir, preferred_type=@py_assert13)
        @py_assert17 = not @py_assert15
        if not @py_assert17:
            @py_format18 = ('' + 'assert not %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.download\n}(%(py11)s\n{%(py11)s = %(py3)s(name=%(py5)s, version=%(py7)s, type=%(py9)s)\n}, %(py12)s, preferred_type=%(py14)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py12':@pytest_ar._saferepr(tdir) if 'tdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tdir) else 'tdir',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = @py_assert17 = None
        @py_assert1 = pm.download
        @py_assert4 = 'test_package'
        @py_assert6 = '2.0.0'
        @py_assert8 = 'SOURCE'
        @py_assert10 = Package(name=@py_assert4, version=@py_assert6, type=@py_assert8)
        @py_assert13 = 'SOURCE'
        @py_assert15 = @py_assert1(@py_assert10, tdir, preferred_type=@py_assert13)
        @py_assert17 = not @py_assert15
        if not @py_assert17:
            @py_format18 = ('' + 'assert not %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.download\n}(%(py11)s\n{%(py11)s = %(py3)s(name=%(py5)s, version=%(py7)s, type=%(py9)s)\n}, %(py12)s, preferred_type=%(py14)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py12':@pytest_ar._saferepr(tdir) if 'tdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tdir) else 'tdir',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = @py_assert17 = None
        dest = pm.download(pkg, tdir, preferred_type='SOURCE')
        source_md5 = hashlib.md5()
        with open(filename, 'rb') as (f):
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, 'rb') as (f):
            dest_md5.update(f.read())
        @py_assert1 = source_md5.hexdigest
        @py_assert3 = @py_assert1()
        @py_assert7 = dest_md5.hexdigest
        @py_assert9 = @py_assert7()
        @py_assert5 = @py_assert3 == @py_assert9
        if not @py_assert5:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.hexdigest\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.hexdigest\n}()\n}',), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(source_md5) if 'source_md5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_md5) else 'source_md5',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(dest_md5) if 'dest_md5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_md5) else 'dest_md5',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    finally:
        shutil.rmtree(tdir)

    try:
        tdir = tempfile.mkdtemp()
        dest = pm.download(Package(name='test_package', version='', type='SOURCE'), tdir, preferred_type='SOURCE')
        source_md5 = hashlib.md5()
        with open(filename, 'rb') as (f):
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, 'rb') as (f):
            dest_md5.update(f.read())
        @py_assert1 = source_md5.hexdigest
        @py_assert3 = @py_assert1()
        @py_assert7 = dest_md5.hexdigest
        @py_assert9 = @py_assert7()
        @py_assert5 = @py_assert3 == @py_assert9
        if not @py_assert5:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.hexdigest\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.hexdigest\n}()\n}',), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(source_md5) if 'source_md5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_md5) else 'source_md5',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(dest_md5) if 'dest_md5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_md5) else 'dest_md5',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    finally:
        shutil.rmtree(tdir)


def test_search():
    pm = PackageManager(repo=(Repository()), installer=(Installer()), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    @py_assert1 = pm.search
    @py_assert3 = 'test_package'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == pkg
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, pkg)) % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = pm.search
    @py_assert3 = 'test_package==1.0.0'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == pkg
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, pkg)) % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = pm.search
    @py_assert3 = 'test_package>0.9.9'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == pkg
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, pkg)) % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = pm.search
    @py_assert3 = 'test_package<1.9.9'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == pkg
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, pkg)) % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = pm.search
    @py_assert3 = 'fake'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = None
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    with pytest.raises(InvalidParameter):
        pm.search('')
    with pytest.raises(InvalidParameter):
        pm.search('1.0.0')


def test_remove():
    pm = PackageManager(repo=(Repository()), installer=(Installer()), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.list_items() == [Package.repo_name(pkg, filename)]
    @py_assert1 = pm.remove
    @py_assert4 = False
    @py_assert6 = @py_assert1(pkg, interactive=@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.remove\n}(%(py3)s, interactive=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    pm.list_items() == []
    pm.list_items(from_cache=True) == []
    @py_assert1 = pm.remove
    @py_assert4 = False
    @py_assert6 = @py_assert1(pkg, interactive=@py_assert4)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.remove\n}(%(py3)s, interactive=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = pm.remove
    @py_assert4 = 'some'
    @py_assert6 = '1.0.0'
    @py_assert8 = Package(@py_assert4, @py_assert6)
    @py_assert10 = False
    @py_assert12 = @py_assert1(@py_assert8, interactive=@py_assert10)
    @py_assert14 = not @py_assert12
    if not @py_assert14:
        @py_format15 = ('' + 'assert not %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.remove\n}(%(py9)s\n{%(py9)s = %(py3)s(%(py5)s, %(py7)s)\n}, interactive=%(py11)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_remove_with_repo_error():
    repo = Repository()

    def problem(x):
        raise Exception()

    repo.delete = problem
    pm = PackageManager(repo=repo, installer=(Installer()), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    @py_assert1 = pm.remove
    @py_assert4 = False
    @py_assert6 = @py_assert1(pkg, interactive=@py_assert4)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.remove\n}(%(py3)s, interactive=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None


def check_if_installed(installer, resource):
    return len([(k, v) for k, v in installer.installed.items() if resource in k if v > 0]) > 0


def check_if_uninstalled(installer, resource):
    return len([(k, v) for k, v in installer.uninstalled.items() if resource in k if v > 0]) > 0


def test_install_user():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('test_package==1.0.0', 'WHEEL', no_user=True)
    @py_assert2 = 'test_package-1.0.0'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None


def test_install_no_user():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('test_package==1.0.0', 'SOURCE', no_user=False)
    @py_assert2 = 'test_package-1.0.0'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None


def test_install_public_no_mirror():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, mirroring=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('some_public==1.0.0', 'SOURCE', no_user=False)
    @py_assert2 = 'some_public-1.0.0'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    @py_assert6 = not @py_assert4
    if not @py_assert6:
        @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert6 = None


def test_install_public_mirror():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, mirroring=True, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('some_public==1.0.0', 'SOURCE', no_user=False)
    @py_assert2 = 'some_public==1.0.0'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None


def test_install_recursive_internal_packages():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, mirroring=True, console=Console(exit_on_error=False))
    pkg1 = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename1 = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pkg2 = Package(name='other_package', version='1.0.0', type='SOURCE')
    filename2 = resource_filename(__name__, 'data/other_package-1.0.0.tar.gz')
    pm.upload(pkg1, filename1)
    pm.upload(pkg2, filename2)
    pm.install('other_package==1.0.0', 'SOURCE', no_user=False)
    @py_assert2 = 'test-dep1'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = 'test-dep2'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = 'other_package-1.0.0'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = 'test_package-1.0.0'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None


def test_without_deps():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, mirroring=True, install_deps=False, console=Console(exit_on_error=False))
    pkg1 = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename1 = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pkg2 = Package(name='other_package', version='1.0.0', type='SOURCE')
    filename2 = resource_filename(__name__, 'data/other_package-1.0.0.tar.gz')
    pm.upload(pkg1, filename1)
    pm.upload(pkg2, filename2)
    pm.install('other_package==1.0.0', 'SOURCE', no_user=False)
    @py_assert2 = 'other_package-1.0.0'
    @py_assert4 = check_if_installed(installer, @py_assert2)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(check_if_installed) if 'check_if_installed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_installed) else 'check_if_installed',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None


def test_uninstall():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('test_package==1.0.0', 'WHEEL', no_user=True)
    pm.uninstall(pkg)
    @py_assert3 = pkg.name
    @py_assert5 = check_if_uninstalled(installer, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py1)s, %(py4)s\n{%(py4)s = %(py2)s.name\n})\n}') % {'py0':@pytest_ar._saferepr(check_if_uninstalled) if 'check_if_uninstalled' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_if_uninstalled) else 'check_if_uninstalled',  'py1':@pytest_ar._saferepr(installer) if 'installer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(installer) else 'installer',  'py2':@pytest_ar._saferepr(pkg) if 'pkg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkg) else 'pkg',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert3 = @py_assert5 = None


def test_cloning_no_overwrite():
    repo1 = Repository()
    pm = PackageManager(repo=repo1, installer=(Installer()), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    try:
        tdir = tempfile.mkdtemp()
        pm.clone(tdir)
        @py_assert1 = os.listdir
        @py_assert4 = @py_assert1(tdir)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tdir) if 'tdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tdir) else 'tdir',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        cloned_zip = os.path.join(tdir, os.listdir(tdir)[0])
        @py_assert1 = pm.restore
        @py_assert4 = False
        @py_assert6 = @py_assert1(cloned_zip, interactive=@py_assert4)
        @py_assert8 = not @py_assert6
        if not @py_assert8:
            @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.restore\n}(%(py3)s, interactive=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(cloned_zip) if 'cloned_zip' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cloned_zip) else 'cloned_zip',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
        dest_pm = PackageManager(repo=(Repository()), installer=(Installer()), console=Console(exit_on_error=False))
        @py_assert1 = dest_pm.list_items
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.list_items\n}()\n}') % {'py0':@pytest_ar._saferepr(dest_pm) if 'dest_pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_pm) else 'dest_pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        dest_pm.restore(cloned_zip, interactive=False)
        @py_assert1 = dest_pm.list_items
        @py_assert3 = @py_assert1()
        @py_assert7 = pm.list_items
        @py_assert9 = @py_assert7()
        @py_assert5 = @py_assert3 == @py_assert9
        if not @py_assert5:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.list_items\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.list_items\n}()\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(dest_pm) if 'dest_pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_pm) else 'dest_pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    finally:
        shutil.rmtree(tdir)


def test_cloning_overwrite():
    repo1 = Repository()
    pm = PackageManager(repo=repo1, installer=(Installer()), overwrite=True, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    try:
        tdir = tempfile.mkdtemp()
        pm.clone(tdir)
        @py_assert1 = os.listdir
        @py_assert4 = @py_assert1(tdir)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tdir) if 'tdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tdir) else 'tdir',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        cloned_zip = os.path.join(tdir, os.listdir(tdir)[0])
        @py_assert1 = pm.restore
        @py_assert4 = False
        @py_assert6 = @py_assert1(cloned_zip, interactive=@py_assert4)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.restore\n}(%(py3)s, interactive=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(pm) if 'pm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pm) else 'pm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(cloned_zip) if 'cloned_zip' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cloned_zip) else 'cloned_zip',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert4 = @py_assert6 = None
    finally:
        shutil.rmtree(tdir)
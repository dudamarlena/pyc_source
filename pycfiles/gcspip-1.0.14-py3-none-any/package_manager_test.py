# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manuel/gcspypi/test/package_manager_test.py
# Compiled at: 2018-11-22 07:00:57
from .mocks.mock_repository import MockRepository as Repository
from .mocks.mock_installer import MockInstaller as Installer
from ethronsoft.gcspypi.package.package_manager import PackageManager, Package
from ethronsoft.gcspypi.exceptions import InvalidParameter, InvalidState
from ethronsoft.gcspypi.utilities.console import Console
from pkg_resources import resource_filename
import pytest, tempfile, shutil, os, hashlib

def test_init():
    pm = PackageManager(repo=Repository(), installer=Installer(), console=Console(exit_on_error=False))
    assert [ x for x in pm.list_items() ] == []


def test_upload_download():
    pm = PackageManager(repo=Repository(), installer=Installer(), overwrite=False, console=Console(exit_on_error=False))
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
        assert not pm.download_by_name('fake', tdir)
        assert not pm.download_by_name(Package.repo_name(Package(name='test_package', version='2.0.0', type='SOURCE'), filename), tdir)
        dest = pm.download_by_name(Package.repo_name(pkg, filename), tdir)
        source_md5 = hashlib.md5()
        with open(filename, 'rb') as (f):
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, 'rb') as (f):
            dest_md5.update(f.read())
        assert source_md5.hexdigest() == dest_md5.hexdigest()
    finally:
        shutil.rmtree(tdir)

    try:
        tdir = tempfile.mkdtemp()
        assert not pm.download(Package(name='fake', version='', type='SOURCE'), tdir, preferred_type='SOURCE')
        assert not pm.download(Package(name='test_package', version='2.0.0', type='SOURCE'), tdir, preferred_type='SOURCE')
        dest = pm.download(pkg, tdir, preferred_type='SOURCE')
        source_md5 = hashlib.md5()
        with open(filename, 'rb') as (f):
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, 'rb') as (f):
            dest_md5.update(f.read())
        assert source_md5.hexdigest() == dest_md5.hexdigest()
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
        assert source_md5.hexdigest() == dest_md5.hexdigest()
    finally:
        shutil.rmtree(tdir)


def test_search():
    pm = PackageManager(repo=Repository(), installer=Installer(), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    assert pm.search('test_package') == pkg
    assert pm.search('test_package==1.0.0') == pkg
    assert pm.search('test_package>0.9.9') == pkg
    assert pm.search('test_package<1.9.9') == pkg
    assert pm.search('fake') == None
    with pytest.raises(InvalidParameter):
        pm.search('')
    with pytest.raises(InvalidParameter):
        pm.search('1.0.0')
    return


def test_remove():
    pm = PackageManager(repo=Repository(), installer=Installer(), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.list_items() == [Package.repo_name(pkg, filename)]
    assert pm.remove(pkg, interactive=False)
    pm.list_items() == []
    pm.list_items(from_cache=True) == []
    assert not pm.remove(pkg, interactive=False)
    assert not pm.remove(Package('some', '1.0.0'), interactive=False)


def test_remove_with_repo_error():
    repo = Repository()

    def problem(x):
        raise Exception()

    repo.delete = problem
    pm = PackageManager(repo=repo, installer=Installer(), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    assert not pm.remove(pkg, interactive=False)


def check_if_installed(installer, resource):
    return len([ (k, v) for k, v in installer.installed.items() if resource in k and v > 0 ]) > 0


def check_if_uninstalled(installer, resource):
    return len([ (k, v) for k, v in installer.uninstalled.items() if resource in k and v > 0 ]) > 0


def test_install_user():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('test_package==1.0.0', 'WHEEL', no_user=True)
    assert check_if_installed(installer, 'test_package-1.0.0')


def test_install_no_user():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('test_package==1.0.0', 'SOURCE', no_user=False)
    assert check_if_installed(installer, 'test_package-1.0.0')


def test_install_public_no_mirror():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, mirroring=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('some_public==1.0.0', 'SOURCE', no_user=False)
    assert not check_if_installed(installer, 'some_public-1.0.0')


def test_install_public_mirror():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, mirroring=True, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('some_public==1.0.0', 'SOURCE', no_user=False)
    assert check_if_installed(installer, 'some_public==1.0.0')


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
    assert check_if_installed(installer, 'test-dep1')
    assert check_if_installed(installer, 'test-dep2')
    assert check_if_installed(installer, 'other_package-1.0.0')
    assert check_if_installed(installer, 'test_package-1.0.0')


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
    assert check_if_installed(installer, 'other_package-1.0.0')


def test_uninstall():
    repo = Repository()
    installer = Installer()
    pm = PackageManager(repo=repo, installer=installer, overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    pm.install('test_package==1.0.0', 'WHEEL', no_user=True)
    pm.uninstall(pkg)
    assert check_if_uninstalled(installer, pkg.name)


def test_cloning_no_overwrite():
    repo1 = Repository()
    pm = PackageManager(repo=repo1, installer=Installer(), overwrite=False, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    try:
        tdir = tempfile.mkdtemp()
        pm.clone(tdir)
        assert os.listdir(tdir)
        cloned_zip = os.path.join(tdir, os.listdir(tdir)[0])
        assert not pm.restore(cloned_zip, interactive=False)
        dest_pm = PackageManager(repo=Repository(), installer=Installer(), console=Console(exit_on_error=False))
        assert not dest_pm.list_items()
        dest_pm.restore(cloned_zip, interactive=False)
        assert dest_pm.list_items() == pm.list_items()
    finally:
        shutil.rmtree(tdir)


def test_cloning_overwrite():
    repo1 = Repository()
    pm = PackageManager(repo=repo1, installer=Installer(), overwrite=True, console=Console(exit_on_error=False))
    pkg = Package(name='test_package', version='1.0.0', type='SOURCE')
    filename = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pm.upload(pkg, filename)
    try:
        tdir = tempfile.mkdtemp()
        pm.clone(tdir)
        assert os.listdir(tdir)
        cloned_zip = os.path.join(tdir, os.listdir(tdir)[0])
        assert pm.restore(cloned_zip, interactive=False)
    finally:
        shutil.rmtree(tdir)
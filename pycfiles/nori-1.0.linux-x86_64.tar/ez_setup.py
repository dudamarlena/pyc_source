# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nori/ez_setup.py
# Compiled at: 2013-12-11 11:11:41
"""Bootstrap setuptools installation

To use setuptools in your package's setup.py, include this
file in the same directory and add this to the top of your setup.py::

    from ez_setup import use_setuptools
    use_setuptools()

To require a specific version of setuptools, set a download
mirror, or use an alternate download directory, simply supply
the appropriate options to ``use_setuptools()``.

This file can also be run as a script to install or upgrade setuptools.
"""
import os, shutil, sys, tempfile, tarfile, optparse, subprocess, platform, textwrap
from distutils import log
try:
    from site import USER_SITE
except ImportError:
    USER_SITE = None

DEFAULT_VERSION = '2.0'
DEFAULT_URL = 'https://pypi.python.org/packages/source/s/setuptools/'

def _python_cmd(*args):
    args = (
     sys.executable,) + args
    return subprocess.call(args) == 0


def _install(tarball, install_args=()):
    tmpdir = tempfile.mkdtemp()
    log.warn('Extracting in %s', tmpdir)
    old_wd = os.getcwd()
    try:
        os.chdir(tmpdir)
        tar = tarfile.open(tarball)
        _extractall(tar)
        tar.close()
        subdir = os.path.join(tmpdir, os.listdir(tmpdir)[0])
        os.chdir(subdir)
        log.warn('Now working in %s', subdir)
        log.warn('Installing Setuptools')
        if not _python_cmd('setup.py', 'install', *install_args):
            log.warn('Something went wrong during the installation.')
            log.warn('See the error message above.')
            return 2
    finally:
        os.chdir(old_wd)
        shutil.rmtree(tmpdir)


def _build_egg(egg, tarball, to_dir):
    tmpdir = tempfile.mkdtemp()
    log.warn('Extracting in %s', tmpdir)
    old_wd = os.getcwd()
    try:
        os.chdir(tmpdir)
        tar = tarfile.open(tarball)
        _extractall(tar)
        tar.close()
        subdir = os.path.join(tmpdir, os.listdir(tmpdir)[0])
        os.chdir(subdir)
        log.warn('Now working in %s', subdir)
        log.warn('Building a Setuptools egg in %s', to_dir)
        _python_cmd('setup.py', '-q', 'bdist_egg', '--dist-dir', to_dir)
    finally:
        os.chdir(old_wd)
        shutil.rmtree(tmpdir)

    log.warn(egg)
    if not os.path.exists(egg):
        raise IOError('Could not build the egg.')


def _do_download(version, download_base, to_dir, download_delay):
    egg = os.path.join(to_dir, 'setuptools-%s-py%d.%d.egg' % (
     version, sys.version_info[0], sys.version_info[1]))
    if not os.path.exists(egg):
        tarball = download_setuptools(version, download_base, to_dir, download_delay)
        _build_egg(egg, tarball, to_dir)
    sys.path.insert(0, egg)
    if 'pkg_resources' in sys.modules:
        del sys.modules['pkg_resources']
    import setuptools
    setuptools.bootstrap_install_from = egg


def use_setuptools(version=DEFAULT_VERSION, download_base=DEFAULT_URL, to_dir=os.curdir, download_delay=15):
    to_dir = os.path.abspath(to_dir)
    rep_modules = ('pkg_resources', 'setuptools')
    imported = set(sys.modules).intersection(rep_modules)
    try:
        import pkg_resources
    except ImportError:
        return _do_download(version, download_base, to_dir, download_delay)

    try:
        pkg_resources.require('setuptools>=' + version)
        return
    except pkg_resources.DistributionNotFound:
        return _do_download(version, download_base, to_dir, download_delay)
    except pkg_resources.VersionConflict as VC_err:
        if imported:
            msg = textwrap.dedent("\n                The required version of setuptools (>={version}) is not available,\n                and can't be installed while this script is running. Please\n                install a more recent version first, using\n                'easy_install -U setuptools'.\n\n                (Currently using {VC_err.args[0]!r})\n                ").format(VC_err=VC_err, version=version)
            sys.stderr.write(msg)
            sys.exit(2)
        del pkg_resources
        del sys.modules['pkg_resources']
        return _do_download(version, download_base, to_dir, download_delay)


def _clean_check(cmd, target):
    """
    Run the command to download target. If the command fails, clean up before
    re-raising the error.
    """
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        if os.access(target, os.F_OK):
            os.unlink(target)
        raise


def download_file_powershell(url, target):
    """
    Download the file at url to target using Powershell (which will validate
    trust). Raise an exception if the command cannot complete.
    """
    target = os.path.abspath(target)
    cmd = [
     'powershell',
     '-Command',
     '(new-object System.Net.WebClient).DownloadFile(%(url)r, %(target)r)' % vars()]
    _clean_check(cmd, target)


def has_powershell():
    if platform.system() != 'Windows':
        return False
    cmd = [
     'powershell', '-Command', 'echo test']
    devnull = open(os.path.devnull, 'wb')
    try:
        try:
            subprocess.check_call(cmd, stdout=devnull, stderr=devnull)
        except:
            return False

    finally:
        devnull.close()

    return True


download_file_powershell.viable = has_powershell

def download_file_curl(url, target):
    cmd = [
     'curl', url, '--silent', '--output', target]
    _clean_check(cmd, target)


def has_curl():
    cmd = [
     'curl', '--version']
    devnull = open(os.path.devnull, 'wb')
    try:
        try:
            subprocess.check_call(cmd, stdout=devnull, stderr=devnull)
        except:
            return False

    finally:
        devnull.close()

    return True


download_file_curl.viable = has_curl

def download_file_wget(url, target):
    cmd = [
     'wget', url, '--quiet', '--output-document', target]
    _clean_check(cmd, target)


def has_wget():
    cmd = [
     'wget', '--version']
    devnull = open(os.path.devnull, 'wb')
    try:
        try:
            subprocess.check_call(cmd, stdout=devnull, stderr=devnull)
        except:
            return False

    finally:
        devnull.close()

    return True


download_file_wget.viable = has_wget

def download_file_insecure(url, target):
    """
    Use Python to download the file, even though it cannot authenticate the
    connection.
    """
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen

    src = dst = None
    try:
        src = urlopen(url)
        data = src.read()
        dst = open(target, 'wb')
        dst.write(data)
    finally:
        if src:
            src.close()
        if dst:
            dst.close()

    return


download_file_insecure.viable = lambda : True

def get_best_downloader():
    downloaders = [
     download_file_powershell,
     download_file_curl,
     download_file_wget,
     download_file_insecure]
    for dl in downloaders:
        if dl.viable():
            return dl


def download_setuptools(version=DEFAULT_VERSION, download_base=DEFAULT_URL, to_dir=os.curdir, delay=15, downloader_factory=get_best_downloader):
    """Download setuptools from a specified location and return its filename

    `version` should be a valid setuptools version number that is available
    as an egg for download under the `download_base` URL (which should end
    with a '/'). `to_dir` is the directory where the egg will be downloaded.
    `delay` is the number of seconds to pause before an actual download
    attempt.

    ``downloader_factory`` should be a function taking no arguments and
    returning a function for downloading a URL to a target.
    """
    to_dir = os.path.abspath(to_dir)
    tgz_name = 'setuptools-%s.tar.gz' % version
    url = download_base + tgz_name
    saveto = os.path.join(to_dir, tgz_name)
    if not os.path.exists(saveto):
        log.warn('Downloading %s', url)
        downloader = downloader_factory()
        downloader(url, saveto)
    return os.path.realpath(saveto)


def _extractall(self, path='.', members=None):
    """Extract all members from the archive to the current working
       directory and set owner, modification time and permissions on
       directories afterwards. `path' specifies a different directory
       to extract to. `members' is optional and must be a subset of the
       list returned by getmembers().
    """
    import copy, operator
    from tarfile import ExtractError
    directories = []
    if members is None:
        members = self
    for tarinfo in members:
        if tarinfo.isdir():
            directories.append(tarinfo)
            tarinfo = copy.copy(tarinfo)
            tarinfo.mode = 448
        self.extract(tarinfo, path)

    directories.sort(key=operator.attrgetter('name'), reverse=True)
    for tarinfo in directories:
        dirpath = os.path.join(path, tarinfo.name)
        try:
            self.chown(tarinfo, dirpath)
            self.utime(tarinfo, dirpath)
            self.chmod(tarinfo, dirpath)
        except ExtractError as e:
            if self.errorlevel > 1:
                raise
            else:
                self._dbg(1, 'tarfile: %s' % e)

    return


def _build_install_args(options):
    """
    Build the arguments to 'python setup.py install' on the setuptools package
    """
    if options.user_install:
        return ['--user']
    return []


def _parse_args():
    """
    Parse the command line for options
    """
    parser = optparse.OptionParser()
    parser.add_option('--user', dest='user_install', action='store_true', default=False, help='install in user site package (requires Python 2.6 or later)')
    parser.add_option('--download-base', dest='download_base', metavar='URL', default=DEFAULT_URL, help='alternative URL from where to download the setuptools package')
    parser.add_option('--insecure', dest='downloader_factory', action='store_const', const=lambda : download_file_insecure, default=get_best_downloader, help='Use internal, non-validating downloader')
    options, args = parser.parse_args()
    return options


def main(version=DEFAULT_VERSION):
    """Install or upgrade setuptools and EasyInstall"""
    options = _parse_args()
    tarball = download_setuptools(download_base=options.download_base, downloader_factory=options.downloader_factory)
    return _install(tarball, _build_install_args(options))


if __name__ == '__main__':
    sys.exit(main())
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/perl.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 4128 bytes
import errno, multiprocessing, os, re, socket, subprocess, tempfile
from pkgcore.restrictions import packages, values
from snakeoil.osutils import pjoin
from .. import const, results, sources
from . import Check, SkipOptionalCheck

class MismatchedPerlVersion(results.VersionResult, results.Warning):
    __doc__ = "A package's normalized perl module version doesn't match its $PV."

    def __init__(self, dist_version, normalized, **kwargs):
        (super().__init__)(**kwargs)
        self.dist_version = dist_version
        self.normalized = normalized

    @property
    def desc(self):
        return f"DIST_VERSION={self.dist_version} normalizes to {self.normalized}"


class _PerlConnection:
    __doc__ = 'Connection to perl script the check is going to communicate with.'

    def __init__(self, options):
        self.connection = None
        self.perl_client = None
        self.process_lock = multiprocessing.Lock()
        self.socket_dir = tempfile.TemporaryDirectory(prefix='pkgcheck-')
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        socket_path = os.path.join(self.socket_dir.name, 'perl.socket')
        try:
            sock.bind(socket_path)
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                return
            raise

        sock.listen()
        perl_script = pjoin(const.DATA_PATH, 'perl-version.pl')
        try:
            self.perl_client = subprocess.Popen([
             'perl', perl_script, socket_path],
              stderr=(subprocess.PIPE))
        except FileNotFoundError:
            raise SkipOptionalCheck(self, 'perl not installed on system')

        sock.settimeout(1)
        try:
            self.connection, _address = sock.accept()
        except socket.timeout:
            err_msg = 'failed to connect to perl client'
            if options.verbosity > 0:
                stderr = self.perl_client.stderr.read().decode().strip()
                err_msg += f": {stderr}"
            raise SkipOptionalCheck(self, err_msg)

    def normalize(self, version):
        """Normalize a given version number to its perl equivalent."""
        with self.process_lock:
            self.connection.send(version.encode() + b'\n')
            size = int(self.connection.recv(2))
            return self.connection.recv(size).decode('utf-8', 'replace')

    def __del__(self):
        if self.connection is not None:
            self.connection.close()
        self.socket_dir.cleanup()
        if self.perl_client is not None:
            self.perl_client.kill()


class PerlCheck(Check):
    __doc__ = 'Perl ebuild related checks.'
    _restricted_source = (
     sources.RestrictionRepoSource,
     (
      packages.PackageRestriction('inherited', values.ContainmentMatch2('perl-module')),))
    _source = (sources.EbuildFileRepoSource, (), (('source', _restricted_source),))
    known_results = frozenset([MismatchedPerlVersion])

    def __init__(self, *args):
        (super().__init__)(*args)
        self.dist_version_re = re.compile('DIST_VERSION=(?P<dist_version>\\d+(\\.\\d+)*)\\s*\n')
        self.perl = _PerlConnection(self.options)

    def feed(self, pkg):
        match = self.dist_version_re.search(''.join(pkg.lines))
        if match is not None:
            dist_version = match.group('dist_version')
            normalized = self.perl.normalize(dist_version)
            if normalized != pkg.version:
                yield MismatchedPerlVersion(dist_version, normalized, pkg=pkg)
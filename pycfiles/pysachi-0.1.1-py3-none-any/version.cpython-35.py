# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/stuart/Git/SWAT/pysac/astropy_helpers/astropy_helpers/version.py
# Compiled at: 2015-11-25 06:17:20
# Size of source mod 2**32: 5392 bytes
import locale, os, subprocess, warnings

def _decode_stdio(stream):
    try:
        stdio_encoding = locale.getdefaultlocale()[1] or 'utf-8'
    except ValueError:
        stdio_encoding = 'utf-8'

    try:
        text = stream.decode(stdio_encoding)
    except UnicodeDecodeError:
        text = stream.decode('latin1')

    return text


def update_git_devstr(version, path=None):
    """
    Updates the git revision string if and only if the path is being imported
    directly from a git working copy.  This ensures that the revision number in
    the version string is accurate.
    """
    try:
        devstr = get_git_devstr(sha=True, show_warning=False, path=path)
    except OSError:
        return version

    if not devstr:
        return version
    else:
        if 'dev' in version:
            version_base = version.split('.dev', 1)[0]
            devstr = get_git_devstr(sha=False, show_warning=False, path=path)
            return version_base + '.dev' + devstr
        return version


def get_git_devstr(sha=False, show_warning=True, path=None):
    """
    Determines the number of revisions in this repository.

    Parameters
    ----------
    sha : bool
        If True, the full SHA1 hash will be returned. Otherwise, the total
        count of commits in the repository will be used as a "revision
        number".

    show_warning : bool
        If True, issue a warning if git returns an error code, otherwise errors
        pass silently.

    path : str or None
        If a string, specifies the directory to look in to find the git
        repository.  If `None`, the current working directory is used.
        If given a filename it uses the directory containing that file.

    Returns
    -------
    devversion : str
        Either a string with the revision number (if `sha` is False), the
        SHA1 hash of the current commit (if `sha` is True), or an empty string
        if git version info could not be identified.

    """
    if path is None:
        path = os.getcwd()
    if not os.path.isdir(path):
        path = os.path.abspath(os.path.dirname(path))
    if not os.path.exists(os.path.join(path, '.git')):
        return ''
    if sha:
        cmd = ['rev-parse', 'HEAD']
    else:
        cmd = [
         'rev-list', '--count', 'HEAD']

    def run_git(cmd):
        try:
            p = subprocess.Popen(['git'] + cmd, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except OSError as e:
            if show_warning:
                warnings.warn('Error running git: ' + str(e))
            return (None, '', '')

        if p.returncode == 128:
            if show_warning:
                warnings.warn('No git repository present at {0!r}! Using default dev version.'.format(path))
            return (p.returncode, '', '')
        if p.returncode == 129:
            if show_warning:
                warnings.warn('Your git looks old (does it support {0}?); consider upgrading to v1.7.2 or later.'.format(cmd[0]))
            return (p.returncode, stdout, stderr)
        if p.returncode != 0:
            if show_warning:
                warnings.warn('Git failed while determining revision count: {0}'.format(_decode_stdio(stderr)))
            return (p.returncode, stdout, stderr)
        return (
         p.returncode, stdout, stderr)

    returncode, stdout, stderr = run_git(cmd)
    if not sha and returncode == 129:
        cmd = [
         'rev-list', '--abbrev-commit', '--abbrev=0', 'HEAD']
        returncode, stdout, stderr = run_git(cmd)
        if returncode == 0:
            return str(stdout.count('\n'))
        else:
            return ''
    else:
        if sha:
            return _decode_stdio(stdout)[:40]
        else:
            return _decode_stdio(stdout).strip()


_last_generated_version = '0.4.4'
_last_githash = 'ca3953a76d40fd16a0fe5a01b76ee526bb9a69b1'
version = update_git_devstr(_last_generated_version)
githash = get_git_devstr(sha=True, show_warning=False, path=__file__) or _last_githash
major = 0
minor = 4
bugfix = 4
release = True
debug = False
try:
    from ._compiler import compiler
except ImportError:
    compiler = 'unknown'

try:
    from .cython_version import cython_version
except ImportError:
    cython_version = 'unknown'
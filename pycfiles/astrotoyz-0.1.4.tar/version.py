# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/astro-toyz/astrotoyz/version.py
# Compiled at: 2015-09-05 20:32:39
from __future__ import unicode_literals
import datetime, locale, os, subprocess, warnings

def _decode_stdio(stream):
    try:
        stdio_encoding = locale.getdefaultlocale()[1] or b'utf-8'
    except ValueError:
        stdio_encoding = b'utf-8'

    try:
        text = stream.decode(stdio_encoding)
    except UnicodeDecodeError:
        text = stream.decode(b'latin1')

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
        if b'dev' in version:
            version_base = version.split(b'.dev', 1)[0]
            devstr = get_git_devstr(sha=False, show_warning=False, path=path)
            return version_base + b'.dev' + devstr
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
        repository.  If `None`, the current working directory is used, and must
        be the root of the git repository.
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
        if not _get_repo_path(path, levels=0):
            return b''
    if not os.path.isdir(path):
        path = os.path.abspath(os.path.dirname(path))
    if sha:
        cmd = [b'rev-parse', b'HEAD']
    else:
        cmd = [
         b'rev-list', b'--count', b'HEAD']

    def run_git(cmd):
        try:
            p = subprocess.Popen([b'git'] + cmd, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except OSError as e:
            if show_warning:
                warnings.warn(b'Error running git: ' + str(e))
            return (None, '', '')

        if p.returncode == 128:
            if show_warning:
                warnings.warn((b'No git repository present at {0!r}! Using default dev version.').format(path))
            return (p.returncode, b'', b'')
        else:
            if p.returncode == 129:
                if show_warning:
                    warnings.warn((b'Your git looks old (does it support {0}?); consider upgrading to v1.7.2 or later.').format(cmd[0]))
                return (p.returncode, stdout, stderr)
            if p.returncode != 0:
                if show_warning:
                    warnings.warn((b'Git failed while determining revision count: {0}').format(_decode_stdio(stderr)))
                return (p.returncode, stdout, stderr)
            return (p.returncode, stdout, stderr)

    returncode, stdout, stderr = run_git(cmd)
    if not sha and returncode == 129:
        cmd = [
         b'rev-list', b'--abbrev-commit', b'--abbrev=0', b'HEAD']
        returncode, stdout, stderr = run_git(cmd)
        if returncode == 0:
            return str(stdout.count(b'\n'))
        return b''
    else:
        if sha:
            return _decode_stdio(stdout)[:40]
        else:
            return _decode_stdio(stdout).strip()

    return


def _get_repo_path(pathname, levels=None):
    """
    Given a file or directory name, determine the root of the git repository
    this path is under.  If given, this won't look any higher than ``levels``
    (that is, if ``levels=0`` then the given path must be the root of the git
    repository and is returned if so.

    Returns `None` if the given path could not be determined to belong to a git
    repo.
    """
    if os.path.isfile(pathname):
        current_dir = os.path.abspath(os.path.dirname(pathname))
    else:
        if os.path.isdir(pathname):
            current_dir = os.path.abspath(pathname)
        else:
            return
        current_level = 0
        while levels is None or current_level <= levels:
            if os.path.exists(os.path.join(current_dir, b'.git')):
                return current_dir
            current_level += 1
            if current_dir == os.path.dirname(current_dir):
                break
            current_dir = os.path.dirname(current_dir)

    return


_packagename = b'astrotoyz'
_last_generated_version = b'0.1.4'
_last_githash = b'71967363abcef68f1b0ce10c6f43fdd478368072'
if _get_repo_path(__file__, levels=len(_packagename.split(b'.'))):
    version = update_git_devstr(_last_generated_version, path=__file__)
    githash = get_git_devstr(sha=True, show_warning=False, path=__file__) or _last_githash
else:
    version = _last_generated_version
    githash = _last_githash
major = 0
minor = 1
bugfix = 4
release = True
timestamp = datetime.datetime(2015, 9, 5, 20, 32, 39, 428011)
debug = False
try:
    from ._compiler import compiler
except ImportError:
    compiler = b'unknown'

try:
    from .cython_version import cython_version
except ImportError:
    cython_version = b'unknown'
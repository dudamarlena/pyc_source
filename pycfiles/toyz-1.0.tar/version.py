# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/toyz/toyz/version.py
# Compiled at: 2015-06-30 23:44:06
import os, subprocess, warnings

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
        Either a string with the revsion number (if `sha` is False), the
        SHA1 hash of the current commit (if `sha` is True), or an empty string
        if git version info could not be identified.

    """
    if path is None:
        path = os.getcwd()
    if not os.path.isdir(path):
        path = os.path.abspath(os.path.dirname(path))
    if not os.path.exists(os.path.join(path, '.git')):
        return ''
    else:
        if sha:
            cmd = [
             'rev-parse']
        else:
            cmd = [
             'rev-list', '--count']
        try:
            p = subprocess.Popen(['git'] + cmd + ['HEAD'], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except OSError as e:
            if show_warning:
                warnings.warn('Error running git: ' + str(e))
            return ''

        if p.returncode == 128:
            if show_warning:
                warnings.warn(('No git repository present at {0!r}! Using default dev version.').format(path))
            return ''
        if p.returncode != 0:
            if show_warning:
                warnings.warn('Git failed while determining revision count: ' + stderr)
            return ''
        if sha:
            return stdout.decode('utf-8')[:40]
        return stdout.decode('utf-8').strip()
        return


_last_generated_version = '0.0.dev146'
version = update_git_devstr(_last_generated_version)
githash = get_git_devstr(sha=True, show_warning=False)
major = 0
minor = 0
bugfix = 0
release = False
debug = False
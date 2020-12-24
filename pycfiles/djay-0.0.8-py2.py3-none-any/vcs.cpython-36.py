# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/main/vcs.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 1241 bytes
"""Module containing some of the logic for our VCS installation logic."""
from flake8 import exceptions as exc
from flake8.main import git
from flake8.main import mercurial
_INSTALLERS = {'git':git.install, 
 'mercurial':mercurial.install}

def install(option, option_string, value, parser):
    """Determine which version control hook to install.

    For more information about the callback signature, see:
    https://docs.python.org/3/library/optparse.html#optparse-option-callbacks
    """
    installer = _INSTALLERS[value]
    errored = False
    successful = False
    try:
        successful = installer()
    except exc.HookInstallationError as hook_error:
        print(str(hook_error))
        errored = True

    if not successful:
        print('Could not find the {0} directory'.format(value))
    raise SystemExit(not successful and errored)


def choices():
    """Return the list of VCS choices."""
    return list(_INSTALLERS)
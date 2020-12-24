# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/utils/outdated.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 6292 bytes
from __future__ import absolute_import
import datetime, json, logging, os.path, sys
from pip._vendor import lockfile, pkg_resources
from pip._vendor.packaging import version as packaging_version
from pip._internal.cli.cmdoptions import make_search_scope
from pip._internal.index import PackageFinder
from pip._internal.models.selection_prefs import SelectionPreferences
from pip._internal.utils.compat import WINDOWS
from pip._internal.utils.filesystem import check_path_owner
from pip._internal.utils.misc import ensure_dir, get_installed_version
from pip._internal.utils.packaging import get_installer
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    import optparse
    from typing import Any, Dict
    from pip._internal.download import PipSession
SELFCHECK_DATE_FMT = '%Y-%m-%dT%H:%M:%SZ'
logger = logging.getLogger(__name__)

class SelfCheckState(object):

    def __init__(self, cache_dir):
        self.state = {}
        self.statefile_path = None
        if cache_dir:
            self.statefile_path = os.path.join(cache_dir, 'selfcheck.json')
            try:
                with open(self.statefile_path) as (statefile):
                    self.state = json.load(statefile)[sys.prefix]
            except (IOError, ValueError, KeyError):
                pass

    def save(self, pypi_version, current_time):
        if not self.statefile_path:
            return
        if not check_path_owner(os.path.dirname(self.statefile_path)):
            return
        ensure_dir(os.path.dirname(self.statefile_path))
        with lockfile.LockFile(self.statefile_path):
            if os.path.exists(self.statefile_path):
                with open(self.statefile_path) as (statefile):
                    state = json.load(statefile)
            else:
                state = {}
            state[sys.prefix] = {'last_check':current_time.strftime(SELFCHECK_DATE_FMT), 
             'pypi_version':pypi_version}
            with open(self.statefile_path, 'w') as (statefile):
                json.dump(state, statefile, sort_keys=True, separators=(',', ':'))


def was_installed_by_pip(pkg):
    """Checks whether pkg was installed by pip

    This is used not to display the upgrade message when pip is in fact
    installed by system package manager, such as dnf on Fedora.
    """
    try:
        dist = pkg_resources.get_distribution(pkg)
        return 'pip' == get_installer(dist)
    except pkg_resources.DistributionNotFound:
        return False


def pip_version_check(session, options):
    """Check for an update for pip.

    Limit the frequency of checks to once per week. State is stored either in
    the active virtualenv or in the user's USER_CACHE_DIR keyed off the prefix
    of the pip script path.
    """
    installed_version = get_installed_version('pip')
    if not installed_version:
        return
    pip_version = packaging_version.parse(installed_version)
    pypi_version = None
    try:
        state = SelfCheckState(cache_dir=(options.cache_dir))
        current_time = datetime.datetime.utcnow()
        if 'last_check' in state.state:
            if 'pypi_version' in state.state:
                last_check = datetime.datetime.strptime(state.state['last_check'], SELFCHECK_DATE_FMT)
                if (current_time - last_check).total_seconds() < 604800:
                    pypi_version = state.state['pypi_version']
        if pypi_version is None:
            search_scope = make_search_scope(options, suppress_no_index=True)
            selection_prefs = SelectionPreferences(allow_yanked=False,
              allow_all_prereleases=False)
            finder = PackageFinder.create(search_scope=search_scope,
              selection_prefs=selection_prefs,
              trusted_hosts=(options.trusted_hosts),
              session=session)
            candidate = finder.find_candidates('pip').get_best()
            if candidate is None:
                return
            pypi_version = str(candidate.version)
            state.save(pypi_version, current_time)
        remote_version = packaging_version.parse(pypi_version)
        local_version_is_older = pip_version < remote_version and pip_version.base_version != remote_version.base_version and was_installed_by_pip('pip')
        if not local_version_is_older:
            return
        if WINDOWS:
            pip_cmd = 'python -m pip'
        else:
            pip_cmd = 'pip'
        logger.warning("You are using pip version %s, however version %s is available.\nYou should consider upgrading via the '%s install --upgrade pip' command.", pip_version, pypi_version, pip_cmd)
    except Exception:
        logger.debug('There was an error checking the latest version of pip',
          exc_info=True)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\version_checks\github_commit.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 2320 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'Gina Häußge <osd@foosel.net>'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License'
import requests, logging
BRANCH_HEAD_URL = 'https://api.github.com/repos/{user}/{repo}/git/refs/heads/{branch}'
logger = logging.getLogger('octoprint.plugins.softwareupdate.version_checks.github_commit')

def _get_latest_commit(user, repo, branch):
    from ..exceptions import NetworkError
    try:
        r = requests.get(BRANCH_HEAD_URL.format(user=user, repo=repo, branch=branch), timeout=(3.05,
                                                                                               30))
    except requests.ConnectionError as exc:
        try:
            raise NetworkError(cause=exc)
        finally:
            exc = None
            del exc

    from . import log_github_ratelimit
    log_github_ratelimit(logger, r)
    if not r.status_code == requests.codes.ok:
        return
    reference = r.json()
    if 'object' not in reference or 'sha' not in reference['object']:
        return
    return reference['object']['sha']


def get_latest(target, check, online=True):
    from ..exceptions import ConfigurationInvalid
    user = check.get('user')
    repo = check.get('repo')
    if user is None or repo is None:
        raise ConfigurationInvalid('Update configuration for {} of type github_commit needs user and repo set and not None'.format(target))
    branch = 'master'
    if 'branch' in check:
        if check['branch'] is not None:
            branch = check['branch']
    current = check.get('current')
    information = dict(local=dict(name='Commit {commit}'.format(commit=(current if current is not None else '?')), value=current), remote=dict(name='?', value='?'),
      needs_online=(not check.get('offline', False)))
    if not online:
        if information['needs_online']:
            return (
             information, True)
    remote_commit = _get_latest_commit(check['user'], check['repo'], branch)
    remote_name = 'Commit {commit}'.format(commit=remote_commit) if remote_commit is not None else '-'
    information['remote'] = dict(name=remote_name, value=remote_commit)
    is_current = current is not None and current == remote_commit or remote_commit is None
    logger.debug('Target: %s, local: %s, remote: %s' % (target, current, remote_commit))
    return (
     information, is_current)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\version_checks\bitbucket_commit.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 2483 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2017 The OctoPrint Project - Released under terms of the AGPLv3 License'
import requests, logging, base64
BRANCH_HEAD_URL = 'https://api.bitbucket.org/2.0/repositories/{user}/{repo}/commit/{branch}'
logger = logging.getLogger('octoprint.plugins.softwareupdate.version_checks.bitbucket_commit')

def _get_latest_commit(user, repo, branch, api_user=None, api_password=None):
    from ..exceptions import NetworkError
    url = BRANCH_HEAD_URL.format(user=user, repo=repo, branch=branch)
    headers = {}
    if api_user is not None:
        if api_password is not None:
            auth_value = base64.b64encode((b'{user}:{pw}').format(user=api_user, pw=api_password))
            headers['authorization'] = 'Basic {}'.format(auth_value)
    else:
        try:
            r = requests.get(url, headers=headers, timeout=(3.05, 30))
        except requests.ConnectionError as exc:
            try:
                raise NetworkError(cause=exc)
            finally:
                exc = None
                del exc

        return r.status_code == requests.codes.ok or None
    reference = r.json()
    if 'hash' not in reference:
        return
    return reference['hash']


def get_latest(target, check, online=True):
    from ..exceptions import ConfigurationInvalid
    if 'user' not in check or 'repo' not in check:
        raise ConfigurationInvalid('Update configuration for %s of type bitbucket_commit needs all of user and repo' % target)
    branch = 'master'
    if 'branch' in check:
        if check['branch'] is not None:
            branch = check['branch']
    api_user = check.get('api_user')
    api_password = check.get('api_password')
    current = check.get('current')
    information = dict(local=dict(name='Commit {commit}'.format(commit=(current if current is not None else 'unknown')), value=current),
      remote=dict(name='?', value='?'),
      needs_online=(not check.get('offline', False)))
    if not online:
        if information['needs_online']:
            return (
             information, True)
    remote_commit = _get_latest_commit(check['user'], check['repo'], branch, api_user, api_password)
    remote_name = 'Commit {commit}'.format(commit=remote_commit) if remote_commit is not None else '-'
    information['remote'] = dict(name=remote_name, value=remote_commit)
    is_current = current is not None and current == remote_commit or remote_commit is None
    logger.debug('Target: %s, local: %s, remote: %s' % (target, current, remote_commit))
    return (
     information, is_current)
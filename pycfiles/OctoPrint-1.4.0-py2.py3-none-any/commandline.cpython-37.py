# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\version_checks\commandline.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 2026 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'Gina Häußge <osd@foosel.net>'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License'
import logging
from ..exceptions import ConfigurationInvalid, CannotCheckOffline
from ..util import execute

def get_latest(target, check, online=True):
    command = check.get('command')
    if command is None:
        raise ConfigurationInvalid('Update configuration for {} of type commandline needs command set and not None'.format(target))
    if not online:
        if not check.get('offline', False):
            raise CannotCheckOffline("{} isn't marked as 'offline' capable, but we are apparently offline right now".format(target))
    returncode, stdout, stderr = execute(command, evaluate_returncode=False)
    stdout_lines = list(filter(lambda x: len(x.strip()), stdout.splitlines()))
    local_name = stdout_lines[(-2)] if len(stdout_lines) >= 2 else 'unknown'
    remote_name = stdout_lines[(-1)] if len(stdout_lines) >= 1 else 'unknown'
    is_current = returncode != 0
    information = dict(local=dict(name=local_name,
      value=local_name),
      remote=dict(name=remote_name,
      value=remote_name))
    logger = logging.getLogger('octoprint.plugins.softwareupdate.version_checks.github_commit')
    logger.debug('Target: %s, local: %s, remote: %s' % (target, local_name, remote_name))
    return (
     information, is_current)
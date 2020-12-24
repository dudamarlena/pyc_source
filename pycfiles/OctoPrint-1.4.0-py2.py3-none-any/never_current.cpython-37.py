# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\version_checks\never_current.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 631 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2018 The OctoPrint Project - Released under terms of the AGPLv3 License'

def get_latest(target, check, online=True):
    local_version = check.get('local_version', '1.0.0')
    remote_version = check.get('remote_version', '1.0.1')
    information = dict(local=dict(name=local_version, value=local_version), remote=dict(name=remote_version, value=remote_version))
    return (
     information, False)
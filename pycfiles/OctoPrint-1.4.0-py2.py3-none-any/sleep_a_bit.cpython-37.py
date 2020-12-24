# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\updaters\sleep_a_bit.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 719 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2018 The OctoPrint Project - Released under terms of the AGPLv3 License'
import time
from octoprint.util import monotonic_time

def can_perform_update(target, check, online=True):
    return True


def perform_update(target, check, target_version, log_cb=None, online=True):
    duration = check.get('duration', 30)
    now = monotonic_time()
    end = now + duration
    while now < end:
        log_cb(['{}s left...'.format(end - now)], prefix='>', stream='output')
        time.sleep(5)
        now = monotonic_time()
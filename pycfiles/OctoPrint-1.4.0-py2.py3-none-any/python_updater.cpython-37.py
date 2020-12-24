# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\updaters\python_updater.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 1244 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'Gina Häußge <osd@foosel.net>'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License'

def can_perform_update(target, check, online=True):
    return 'python_updater' in check and check['python_updater'] is not None and hasattr(check['python_updater'], 'perform_update') and (online or check.get('offline', False))


def perform_update(target, check, target_version, log_cb=None, online=True):
    from ..exceptions import CannotUpdateOffline
    if not online:
        if not check('offline', False):
            raise CannotUpdateOffline()
    try:
        return check['python_updater'].perform_update(target, check, target_version, log_cb=log_cb, online=online)
    except Exception:
        import inspect
        args, _, _, _ = inspect.getargspec(check['python_updater'].perform_update)
        if 'online' not in args:
            return check['python_updater'].perform_update(target, check, target_version, log_cb=log_cb)
        raise
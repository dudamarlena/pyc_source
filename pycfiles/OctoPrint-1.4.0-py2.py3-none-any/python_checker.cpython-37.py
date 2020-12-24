# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\version_checks\python_checker.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 1369 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'Gina Häußge <osd@foosel.net>'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License'
from ..exceptions import ConfigurationInvalid, CannotCheckOffline

def get_latest(target, check, full_data=False, online=True):
    python_checker = check.get('python_checker')
    if not (python_checker is None or hasattr(python_checker, 'get_latest')):
        raise ConfigurationInvalid('Update configuration for {} of type python_checker needs python_checker defined and have an attribute "get_latest"'.format(target))
    if not online:
        if not check.get('offline', False):
            raise CannotCheckOffline("{} isn't marked as 'offline' capable, but we are apparently offline right now".format(target))
    try:
        return check['python_checker'].get_latest(target, check, full_data=full_data, online=online)
    except Exception:
        import inspect
        args, _, _, _ = inspect.getargspec(check['python_checker'].get_latest)
        if 'online' not in args:
            return check['python_checker'].get_latest(target, check, full_data=full_data)
        raise
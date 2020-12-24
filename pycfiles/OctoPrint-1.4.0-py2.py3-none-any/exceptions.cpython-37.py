# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\exceptions.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 1314 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'Gina Häußge <osd@foosel.net>'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License'

class NoUpdateAvailable(Exception):
    pass


class UpdateAlreadyInProgress(Exception):
    pass


class UnknownUpdateType(Exception):
    pass


class UnknownCheckType(Exception):
    pass


class NetworkError(Exception):

    def __init__(self, message=None, cause=None):
        Exception.__init__(self)
        self.message = message
        self.cause = cause

    def __str__(self):
        if self.message is not None:
            return self.message
        if self.cause is not None:
            return 'NetworkError caused by {}'.format(self.cause)
        return 'NetworkError'


class UpdateError(Exception):

    def __init__(self, message, data):
        self.message = message
        self.data = data


class ScriptError(Exception):

    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class RestartFailed(Exception):
    pass


class ConfigurationInvalid(Exception):
    pass


class CannotCheckOffline(Exception):
    pass


class CannotUpdateOffline(Exception):
    pass
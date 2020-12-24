# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/blackdog/exception.py
# Compiled at: 2014-07-24 13:44:28
# Size of source mod 2**32: 1490 bytes
"""
BlackDog

Copyright (C) 2014 Snaipe, Ojukashi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from string import Template

class BlackDogException(Exception):

    def __init__(self, message, *args, **kargs):
        super().__init__(*args)
        self.message = Template(message).substitute(**kargs)


class ServerAlreadyRunningException(BlackDogException):

    def __init__(self):
        super().__init__('Server is already running')


class ServerNotRunningException(BlackDogException):

    def __init__(self):
        super().__init__('Server is not running')


class NoSuchPluginException(BlackDogException):

    def __init__(self, plugin):
        super().__init__('Plugin ${name} could not be found', plugin, name=plugin.name)


class NoSuchPluginVersionException(BlackDogException):

    def __init__(self, version):
        super().__init__('Version ${version} could not be found', version, version=version)
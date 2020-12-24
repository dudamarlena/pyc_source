# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/blackdog/__init__.py
# Compiled at: 2014-07-29 14:17:50
# Size of source mod 2**32: 2064 bytes
"""
BlackDog

Copyright (C) 2014 Snaipe, Therozin

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
import errno, logging, os
from os.path import exists, expanduser, join
from baker import run
from blackdog.exception import *
from blackdog.bukkitdev import BukkitDev, PluginStage, Plugin, PluginVersion
from blackdog.server import HTTPServer

class BlackDog(object):
    instance = None

    def __init__(self):
        BlackDog.instance = self
        logging.basicConfig(level='INFO', format='[%(name)s] %(message)s')
        logging.getLogger('requests.packages.urllib3.connectionpool').disabled = True
        self.logger = logging.getLogger('BlackDog')
        self.directory = expanduser('~/.blackdog/')
        os.makedirs(self.directory, mode=493, exist_ok=True)
        self.bukkitdev = BukkitDev(self.directory)
        self.pidfile = join(self.directory, '.pid')

    def main(self):
        try:
            run()
        except BlackDogException as ex:
            self.logger.error(ex.message)

    @staticmethod
    def checkpid(pid):
        try:
            os.kill(pid, 0)
        except OSError as e:
            if e.errno == errno.ESRCH:
                return False

        return True

    def get_server_pid(self):
        if exists(self.pidfile):
            with open(self.pidfile, 'r') as (f):
                return int(f.read())

    def is_server_running(self):
        pid = self.get_server_pid()
        if pid:
            return self.checkpid(pid)
        return False
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/resolvers/aptresolver.py
# Compiled at: 2018-06-20 18:06:03
# Size of source mod 2**32: 796 bytes
from irk.installers.aptinstall import AptInstaller
from .common import Resolver
from ..util.proc import run

class AptResolver(Resolver):

    def __init__(self, config_content, data):
        super().__init__(config_content, data)
        self.name = config_content.splitlines(False)[1]
        self.executable = config_content.splitlines(False)[2]

    def provides(self, package_name):
        return True

    def get_resolver_name(self):
        return self.name

    def resolve_to_installer(self, package_name):
        return AptInstaller(package_name, self.executable)

    @classmethod
    def get_check_line(cls):
        return 'APT'

    def update_resolver(self):
        print('Updating apt cache')
        run([self.executable, 'update'])
        print('Done updating apt cache')
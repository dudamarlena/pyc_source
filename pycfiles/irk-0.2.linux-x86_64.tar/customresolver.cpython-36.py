# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/resolvers/customresolver.py
# Compiled at: 2018-06-20 22:05:50
# Size of source mod 2**32: 746 bytes
import re
from irk.installers.script import ScriptInstaller
from .common import Resolver

class RegexResolver(Resolver):

    def __init__(self, config_content, data):
        super().__init__(config_content, data)
        self.name = config_content.splitlines(False)[1]
        self.regex = re.compile(config_content.splitlines(False)[2])
        self.script = data

    def provides(self, package_name):
        return bool(self.regex.fullmatch(package_name))

    def get_resolver_name(self):
        return self.name

    def resolve_to_installer(self, package_name):
        return ScriptInstaller(self.script, package_name)

    @classmethod
    def get_check_line(cls):
        return 'CREGX'

    def update_resolver(self):
        pass
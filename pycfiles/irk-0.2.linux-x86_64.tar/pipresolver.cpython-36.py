# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/resolvers/pipresolver.py
# Compiled at: 2018-06-20 15:57:29
# Size of source mod 2**32: 759 bytes
from ..installers.pipinstall import PipInstaller
from .common import Resolver
import re
matcher = re.compile('python(\\d(\\.\\d)*)?-([\\w\\-_]+)')

class PipResolver(Resolver):

    def __init__(self, config_content, data):
        super().__init__(config_content, data)
        self.name = config_content.splitlines(False)[1]

    def provides(self, package_name):
        return bool(matcher.fullmatch(package_name))

    def get_resolver_name(self):
        return self.name

    def resolve_to_installer(self, package_name):
        match = matcher.match(package_name)
        return PipInstaller(match.group(3), match.group(1))

    @classmethod
    def get_check_line(cls):
        return 'PIP'
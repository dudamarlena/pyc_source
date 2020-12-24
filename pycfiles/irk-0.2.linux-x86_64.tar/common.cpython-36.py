# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/resolvers/common.py
# Compiled at: 2018-06-20 17:41:41
# Size of source mod 2**32: 368 bytes


class Resolver:

    def __init__(self, config_content, data):
        pass

    def provides(self, package_name):
        return False

    def get_resolver_name(self):
        return ''

    def resolve_to_installer(self, package_name):
        pass

    @classmethod
    def get_check_line(cls):
        return ''

    def update_resolver(self):
        pass
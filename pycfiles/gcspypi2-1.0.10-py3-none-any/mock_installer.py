# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manuel/gcspypi/test/mocks/mock_installer.py
# Compiled at: 2018-11-22 07:00:57


class MockInstaller(object):

    def __init__(self):
        self.installed = {}
        self.uninstalled = {}

    def install(self, resource, flags=[]):
        self.installed[resource] = self.installed.get('resource', 0) + 1

    def uninstall(self, pkg):
        self.uninstalled[pkg.full_name] = self.uninstalled.get(pkg.full_name, 0) + 1
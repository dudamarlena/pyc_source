# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/permission.py
# Compiled at: 2015-12-14 14:05:17


class Permission:
    flags = {}

    def __init__(self, permission_xml=None):
        self.permission = 0
        self.init_permission_flags()
        if permission_xml is not None:
            self.parse_xml(permission_xml)
        return

    def parse_xml(self, permission_xml):
        for i in permission_xml.xpath('permission'):
            self.add_permission(i.xpath('./text()')[0])

    def init_permission_flags(self):
        if self.flags:
            return
        self.flags['Read'] = 1
        self.flags['Update'] = 2
        self.flags['Create'] = 4
        self.flags['Delete'] = 8

    def add_permission(self, permission):
        self.permission |= self.flags[permission]

    def __str__(self):
        return str(self.permission)
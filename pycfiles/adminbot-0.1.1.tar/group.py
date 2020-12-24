# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/access/group.py
# Compiled at: 2018-01-31 14:44:08


class IamGroup(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.name = None
        self.id = None
        self.path = None
        self.arn = None
        self.createdate = None
        return

    def __repr__(self):
        return str(self.__class__.__name__) + ':' + str(self.name)

    def startElement(self, name, value, connection):
        pass

    def endElement(self, name, value, connection):
        ename = name.lower().replace('euca:', '')
        if ename:
            if ename == 'groupid':
                self.id = value
            if ename == 'groupname':
                self.name = value
            setattr(self, ename.lower(), value)
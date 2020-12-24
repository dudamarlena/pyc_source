# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
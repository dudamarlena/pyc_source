# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/group.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1559 bytes


class Group(object):

    def __init__(self, parent=None):
        self.id = None
        self.name = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'groupId':
            self.id = value
        else:
            if name == 'groupName':
                self.name = value
            else:
                setattr(self, name, value)
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
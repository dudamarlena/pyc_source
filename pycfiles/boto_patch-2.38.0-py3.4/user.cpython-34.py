# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/user.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1968 bytes


class User(object):

    def __init__(self, parent=None, id='', display_name=''):
        if parent:
            parent.owner = self
        self.type = None
        self.id = id
        self.display_name = display_name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'DisplayName':
            self.display_name = value
        else:
            if name == 'ID':
                self.id = value
            else:
                setattr(self, name, value)

    def to_xml(self, element_name='Owner'):
        if self.type:
            s = '<%s xsi:type="%s">' % (element_name, self.type)
        else:
            s = '<%s>' % element_name
        s += '<ID>%s</ID>' % self.id
        s += '<DisplayName>%s</DisplayName>' % self.display_name
        s += '</%s>' % element_name
        return s
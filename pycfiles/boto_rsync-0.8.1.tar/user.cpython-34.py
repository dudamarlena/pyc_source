# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
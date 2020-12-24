# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/tag.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3076 bytes


class TagSet(dict):
    """TagSet"""

    def __init__(self, connection=None):
        self.connection = connection
        self._current_key = None
        self._current_value = None

    def startElement(self, name, attrs, connection):
        if name == 'item':
            self._current_key = None
            self._current_value = None

    def endElement(self, name, value, connection):
        if name == 'key':
            self._current_key = value
        else:
            if name == 'value':
                self._current_value = value
            elif name == 'item':
                self[self._current_key] = self._current_value


class Tag(object):
    """Tag"""

    def __init__(self, connection=None, res_id=None, res_type=None, name=None, value=None):
        self.connection = connection
        self.res_id = res_id
        self.res_type = res_type
        self.name = name
        self.value = value

    def __repr__(self):
        return 'Tag:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'resourceId':
            self.res_id = value
        else:
            if name == 'resourceType':
                self.res_type = value
            else:
                if name == 'key':
                    self.name = value
                else:
                    if name == 'value':
                        self.value = value
                    else:
                        setattr(self, name, value)
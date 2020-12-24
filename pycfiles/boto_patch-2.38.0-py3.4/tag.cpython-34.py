# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/tag.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3076 bytes


class TagSet(dict):
    __doc__ = '\n    A TagSet is used to collect the tags associated with a particular\n    EC2 resource.  Not all resources can be tagged but for those that\n    can, this dict object will be used to collect those values.  See\n    :class:`boto.ec2.ec2object.TaggedEC2Object` for more details.\n    '

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
    __doc__ = '\n    A Tag is used when creating or listing all tags related to\n    an AWS account.  It records not only the key and value but\n    also the ID of the resource to which the tag is attached\n    as well as the type of the resource.\n    '

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
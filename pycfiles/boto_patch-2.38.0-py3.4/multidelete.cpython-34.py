# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/multidelete.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4757 bytes
from boto import handler
import xml.sax

class Deleted(object):
    __doc__ = '\n    A successfully deleted object in a multi-object delete request.\n\n    :ivar key: Key name of the object that was deleted.\n    \n    :ivar version_id: Version id of the object that was deleted.\n    \n    :ivar delete_marker: If True, indicates the object deleted\n        was a DeleteMarker.\n        \n    :ivar delete_marker_version_id: Version ID of the delete marker\n        deleted.\n    '

    def __init__(self, key=None, version_id=None, delete_marker=False, delete_marker_version_id=None):
        self.key = key
        self.version_id = version_id
        self.delete_marker = delete_marker
        self.delete_marker_version_id = delete_marker_version_id

    def __repr__(self):
        if self.version_id:
            return '<Deleted: %s.%s>' % (self.key, self.version_id)
        else:
            return '<Deleted: %s>' % self.key

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Key':
            self.key = value
        else:
            if name == 'VersionId':
                self.version_id = value
            else:
                if name == 'DeleteMarker':
                    if value.lower() == 'true':
                        self.delete_marker = True
                else:
                    if name == 'DeleteMarkerVersionId':
                        self.delete_marker_version_id = value
                    else:
                        setattr(self, name, value)


class Error(object):
    __doc__ = '\n    An unsuccessful deleted object in a multi-object delete request.\n\n    :ivar key: Key name of the object that was not deleted.\n    \n    :ivar version_id: Version id of the object that was not deleted.\n    \n    :ivar code: Status code of the failed delete operation.\n        \n    :ivar message: Status message of the failed delete operation.\n    '

    def __init__(self, key=None, version_id=None, code=None, message=None):
        self.key = key
        self.version_id = version_id
        self.code = code
        self.message = message

    def __repr__(self):
        if self.version_id:
            return '<Error: %s.%s(%s)>' % (self.key, self.version_id,
             self.code)
        else:
            return '<Error: %s(%s)>' % (self.key, self.code)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Key':
            self.key = value
        else:
            if name == 'VersionId':
                self.version_id = value
            else:
                if name == 'Code':
                    self.code = value
                else:
                    if name == 'Message':
                        self.message = value
                    else:
                        setattr(self, name, value)


class MultiDeleteResult(object):
    __doc__ = '\n    The status returned from a MultiObject Delete request.\n\n    :ivar deleted: A list of successfully deleted objects.  Note that if\n        the quiet flag was specified in the request, this list will\n        be empty because only error responses would be returned.\n\n    :ivar errors: A list of unsuccessfully deleted objects.\n    '

    def __init__(self, bucket=None):
        self.bucket = None
        self.deleted = []
        self.errors = []

    def startElement(self, name, attrs, connection):
        if name == 'Deleted':
            d = Deleted()
            self.deleted.append(d)
            return d
        if name == 'Error':
            e = Error()
            self.errors.append(e)
            return e

    def endElement(self, name, value, connection):
        setattr(self, name, value)
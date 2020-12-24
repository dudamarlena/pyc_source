# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/multidelete.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4757 bytes
from boto import handler
import xml.sax

class Deleted(object):
    """Deleted"""

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
    """Error"""

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
    """MultiDeleteResult"""

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
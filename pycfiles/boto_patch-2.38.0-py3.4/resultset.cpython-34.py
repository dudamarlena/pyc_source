# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/resultset.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6556 bytes
from boto.s3.user import User

class ResultSet(list):
    __doc__ = "\n    The ResultSet is used to pass results back from the Amazon services\n    to the client. It is light wrapper around Python's :py:class:`list` class,\n    with some additional methods for parsing XML results from AWS.\n    Because I don't really want any dependencies on external libraries,\n    I'm using the standard SAX parser that comes with Python. The good news is\n    that it's quite fast and efficient but it makes some things rather\n    difficult.\n\n    You can pass in, as the marker_elem parameter, a list of tuples.\n    Each tuple contains a string as the first element which represents\n    the XML element that the resultset needs to be on the lookout for\n    and a Python class as the second element of the tuple. Each time the\n    specified element is found in the XML, a new instance of the class\n    will be created and popped onto the stack.\n\n    :ivar str next_token: A hash used to assist in paging through very long\n        result sets. In most cases, passing this value to certain methods\n        will give you another 'page' of results.\n    "

    def __init__(self, marker_elem=None):
        list.__init__(self)
        if isinstance(marker_elem, list):
            self.markers = marker_elem
        else:
            self.markers = []
        self.marker = None
        self.key_marker = None
        self.next_marker = None
        self.next_key_marker = None
        self.next_upload_id_marker = None
        self.next_version_id_marker = None
        self.next_generation_marker = None
        self.version_id_marker = None
        self.is_truncated = False
        self.next_token = None
        self.status = True

    def startElement(self, name, attrs, connection):
        for t in self.markers:
            if name == t[0]:
                obj = t[1](connection)
                self.append(obj)
                return obj

        if name == 'Owner':
            self.owner = User()
            return self.owner

    def to_boolean(self, value, true_value='true'):
        if value == true_value:
            return True
        else:
            return False

    def endElement(self, name, value, connection):
        if name == 'IsTruncated':
            self.is_truncated = self.to_boolean(value)
        else:
            if name == 'Marker':
                self.marker = value
            else:
                if name == 'KeyMarker':
                    self.key_marker = value
                else:
                    if name == 'NextMarker':
                        self.next_marker = value
                    else:
                        if name == 'NextKeyMarker':
                            self.next_key_marker = value
                        else:
                            if name == 'VersionIdMarker':
                                self.version_id_marker = value
                            else:
                                if name == 'NextVersionIdMarker':
                                    self.next_version_id_marker = value
                                else:
                                    if name == 'NextGenerationMarker':
                                        self.next_generation_marker = value
                                    else:
                                        if name == 'UploadIdMarker':
                                            self.upload_id_marker = value
                                        else:
                                            if name == 'NextUploadIdMarker':
                                                self.next_upload_id_marker = value
                                            else:
                                                if name == 'Bucket':
                                                    self.bucket = value
                                                else:
                                                    if name == 'MaxUploads':
                                                        self.max_uploads = int(value)
                                                    else:
                                                        if name == 'MaxItems':
                                                            self.max_items = int(value)
                                                        else:
                                                            if name == 'Prefix':
                                                                self.prefix = value
                                                            else:
                                                                if name == 'return':
                                                                    self.status = self.to_boolean(value)
                                                                else:
                                                                    if name == 'StatusCode':
                                                                        self.status = self.to_boolean(value, 'Success')
                                                                    else:
                                                                        if name == 'ItemName':
                                                                            self.append(value)
                                                                        else:
                                                                            if name == 'NextToken':
                                                                                self.next_token = value
                                                                            else:
                                                                                if name == 'nextToken':
                                                                                    self.next_token = value
                                                                                    self.nextToken = value
                                                                                elif name == 'BoxUsage':
                                                                                    try:
                                                                                        connection.box_usage += float(value)
                                                                                    except:
                                                                                        pass

                                                                                else:
                                                                                    if name == 'IsValid':
                                                                                        self.status = self.to_boolean(value, 'True')
                                                                                    else:
                                                                                        setattr(self, name, value)


class BooleanResult(object):

    def __init__(self, marker_elem=None):
        self.status = True
        self.request_id = None
        self.box_usage = None

    def __repr__(self):
        if self.status:
            return 'True'
        else:
            return 'False'

    def __nonzero__(self):
        return self.status

    def startElement(self, name, attrs, connection):
        pass

    def to_boolean(self, value, true_value='true'):
        if value == true_value:
            return True
        else:
            return False

    def endElement(self, name, value, connection):
        if name == 'return':
            self.status = self.to_boolean(value)
        else:
            if name == 'StatusCode':
                self.status = self.to_boolean(value, 'Success')
            else:
                if name == 'IsValid':
                    self.status = self.to_boolean(value, 'True')
                else:
                    if name == 'RequestId':
                        self.request_id = value
                    else:
                        if name == 'requestId':
                            self.request_id = value
                        else:
                            if name == 'BoxUsage':
                                self.request_id = value
                            else:
                                setattr(self, name, value)
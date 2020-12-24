# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/resultset.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6556 bytes
from boto.s3.user import User

class ResultSet(list):
    """ResultSet"""

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
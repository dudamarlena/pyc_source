# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/exception.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 17106 bytes
"""
Exception classes - Subclassing allows you to check for specific errors
"""
import base64, xml.sax, boto
from boto import handler
from boto.compat import json, StandardError
from boto.resultset import ResultSet

class BotoClientError(StandardError):
    __doc__ = '\n    General Boto Client error (error accessing AWS)\n    '

    def __init__(self, reason, *args):
        super(BotoClientError, self).__init__(reason, *args)
        self.reason = reason

    def __repr__(self):
        return 'BotoClientError: %s' % self.reason

    def __str__(self):
        return 'BotoClientError: %s' % self.reason


class SDBPersistenceError(StandardError):
    pass


class StoragePermissionsError(BotoClientError):
    __doc__ = '\n    Permissions error when accessing a bucket or key on a storage service.\n    '


class S3PermissionsError(StoragePermissionsError):
    __doc__ = '\n    Permissions error when accessing a bucket or key on S3.\n    '


class GSPermissionsError(StoragePermissionsError):
    __doc__ = '\n    Permissions error when accessing a bucket or key on GS.\n    '


class BotoServerError(StandardError):

    def __init__(self, status, reason, body=None, *args):
        super(BotoServerError, self).__init__(status, reason, body, *args)
        self.status = status
        self.reason = reason
        self.body = body or ''
        self.request_id = None
        self.error_code = None
        self._error_message = None
        self.message = ''
        self.box_usage = None
        if isinstance(self.body, bytes):
            try:
                self.body = self.body.decode('utf-8')
            except UnicodeDecodeError:
                boto.log.debug('Unable to decode body from bytes!')

        if self.body:
            if hasattr(self.body, 'items'):
                self.request_id = self.body.get('RequestId', None)
                if 'Error' in self.body:
                    error = self.body.get('Error', {})
                    self.error_code = error.get('Code', None)
                    self.message = error.get('Message', None)
                else:
                    self.message = self.body.get('message', None)
            else:
                try:
                    h = handler.XmlHandlerWrapper(self, self)
                    h.parseString(self.body)
                except (TypeError, xml.sax.SAXParseException):
                    try:
                        parsed = json.loads(self.body)
                        if 'RequestId' in parsed:
                            self.request_id = parsed['RequestId']
                        if 'Error' in parsed:
                            if 'Code' in parsed['Error']:
                                self.error_code = parsed['Error']['Code']
                            if 'Message' in parsed['Error']:
                                self.message = parsed['Error']['Message']
                    except (TypeError, ValueError):
                        self.message = self.body
                        self.body = None

    def __getattr__(self, name):
        if name == 'error_message':
            return self.message
        if name == 'code':
            return self.error_code
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'error_message':
            self.message = value
        else:
            super(BotoServerError, self).__setattr__(name, value)

    def __repr__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__,
         self.status, self.reason, self.body)

    def __str__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__,
         self.status, self.reason, self.body)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name in ('RequestId', 'RequestID'):
            self.request_id = value
        else:
            if name == 'Code':
                self.error_code = value
            else:
                if name == 'Message':
                    self.message = value
                elif name == 'BoxUsage':
                    self.box_usage = value

    def _cleanupParsedProperties(self):
        self.request_id = None
        self.error_code = None
        self.message = None
        self.box_usage = None


class ConsoleOutput(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.instance_id = None
        self.timestamp = None
        self.comment = None
        self.output = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'instanceId':
            self.instance_id = value
        else:
            if name == 'output':
                self.output = base64.b64decode(value)
            else:
                setattr(self, name, value)


class StorageCreateError(BotoServerError):
    __doc__ = '\n    Error creating a bucket or key on a storage service.\n    '

    def __init__(self, status, reason, body=None):
        self.bucket = None
        super(StorageCreateError, self).__init__(status, reason, body)

    def endElement(self, name, value, connection):
        if name == 'BucketName':
            self.bucket = value
        else:
            return super(StorageCreateError, self).endElement(name, value, connection)


class S3CreateError(StorageCreateError):
    __doc__ = '\n    Error creating a bucket or key on S3.\n    '


class GSCreateError(StorageCreateError):
    __doc__ = '\n    Error creating a bucket or key on GS.\n    '


class StorageCopyError(BotoServerError):
    __doc__ = '\n    Error copying a key on a storage service.\n    '


class S3CopyError(StorageCopyError):
    __doc__ = '\n    Error copying a key on S3.\n    '


class GSCopyError(StorageCopyError):
    __doc__ = '\n    Error copying a key on GS.\n    '


class SQSError(BotoServerError):
    __doc__ = '\n    General Error on Simple Queue Service.\n    '

    def __init__(self, status, reason, body=None):
        self.detail = None
        self.type = None
        super(SQSError, self).__init__(status, reason, body)

    def startElement(self, name, attrs, connection):
        return super(SQSError, self).startElement(name, attrs, connection)

    def endElement(self, name, value, connection):
        if name == 'Detail':
            self.detail = value
        else:
            if name == 'Type':
                self.type = value
            else:
                return super(SQSError, self).endElement(name, value, connection)

    def _cleanupParsedProperties(self):
        super(SQSError, self)._cleanupParsedProperties()
        for p in ('detail', 'type'):
            setattr(self, p, None)


class SQSDecodeError(BotoClientError):
    __doc__ = '\n    Error when decoding an SQS message.\n    '

    def __init__(self, reason, message):
        super(SQSDecodeError, self).__init__(reason, message)
        self.message = message

    def __repr__(self):
        return 'SQSDecodeError: %s' % self.reason

    def __str__(self):
        return 'SQSDecodeError: %s' % self.reason


class StorageResponseError(BotoServerError):
    __doc__ = '\n    Error in response from a storage service.\n    '

    def __init__(self, status, reason, body=None):
        self.resource = None
        super(StorageResponseError, self).__init__(status, reason, body)

    def startElement(self, name, attrs, connection):
        return super(StorageResponseError, self).startElement(name, attrs, connection)

    def endElement(self, name, value, connection):
        if name == 'Resource':
            self.resource = value
        else:
            return super(StorageResponseError, self).endElement(name, value, connection)

    def _cleanupParsedProperties(self):
        super(StorageResponseError, self)._cleanupParsedProperties()
        for p in 'resource':
            setattr(self, p, None)


class S3ResponseError(StorageResponseError):
    __doc__ = '\n    Error in response from S3.\n    '


class GSResponseError(StorageResponseError):
    __doc__ = '\n    Error in response from GS.\n    '


class EC2ResponseError(BotoServerError):
    __doc__ = '\n    Error in response from EC2.\n    '

    def __init__(self, status, reason, body=None):
        self.errors = None
        self._errorResultSet = []
        super(EC2ResponseError, self).__init__(status, reason, body)
        self.errors = [(e.error_code, e.error_message) for e in self._errorResultSet]
        if len(self.errors):
            self.error_code, self.error_message = self.errors[0]

    def startElement(self, name, attrs, connection):
        if name == 'Errors':
            self._errorResultSet = ResultSet([('Error', _EC2Error)])
            return self._errorResultSet
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'RequestID':
            self.request_id = value
        else:
            return

    def _cleanupParsedProperties(self):
        super(EC2ResponseError, self)._cleanupParsedProperties()
        self._errorResultSet = []
        for p in 'errors':
            setattr(self, p, None)


class JSONResponseError(BotoServerError):
    __doc__ = '\n    This exception expects the fully parsed and decoded JSON response\n    body to be passed as the body parameter.\n\n    :ivar status: The HTTP status code.\n    :ivar reason: The HTTP reason message.\n    :ivar body: The Python dict that represents the decoded JSON\n        response body.\n    :ivar error_message: The full description of the AWS error encountered.\n    :ivar error_code: A short string that identifies the AWS error\n        (e.g. ConditionalCheckFailedException)\n    '

    def __init__(self, status, reason, body=None, *args):
        self.status = status
        self.reason = reason
        self.body = body
        if self.body:
            self.error_message = self.body.get('message', None)
            self.error_code = self.body.get('__type', None)
            if self.error_code:
                self.error_code = self.error_code.split('#')[(-1)]


class DynamoDBResponseError(JSONResponseError):
    pass


class SWFResponseError(JSONResponseError):
    pass


class EmrResponseError(BotoServerError):
    __doc__ = '\n    Error in response from EMR\n    '


class _EC2Error(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.error_code = None
        self.error_message = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Code':
            self.error_code = value
        else:
            if name == 'Message':
                self.error_message = value
            else:
                return


class SDBResponseError(BotoServerError):
    __doc__ = '\n    Error in responses from SDB.\n    '


class AWSConnectionError(BotoClientError):
    __doc__ = '\n    General error connecting to Amazon Web Services.\n    '


class StorageDataError(BotoClientError):
    __doc__ = '\n    Error receiving data from a storage service.\n    '


class S3DataError(StorageDataError):
    __doc__ = '\n    Error receiving data from S3.\n    '


class GSDataError(StorageDataError):
    __doc__ = '\n    Error receiving data from GS.\n    '


class InvalidUriError(Exception):
    __doc__ = 'Exception raised when URI is invalid.'

    def __init__(self, message):
        super(InvalidUriError, self).__init__(message)
        self.message = message


class InvalidAclError(Exception):
    __doc__ = 'Exception raised when ACL XML is invalid.'

    def __init__(self, message):
        super(InvalidAclError, self).__init__(message)
        self.message = message


class InvalidCorsError(Exception):
    __doc__ = 'Exception raised when CORS XML is invalid.'

    def __init__(self, message):
        super(InvalidCorsError, self).__init__(message)
        self.message = message


class NoAuthHandlerFound(Exception):
    __doc__ = 'Is raised when no auth handlers were found ready to authenticate.'


class InvalidLifecycleConfigError(Exception):
    __doc__ = 'Exception raised when GCS lifecycle configuration XML is invalid.'

    def __init__(self, message):
        super(InvalidLifecycleConfigError, self).__init__(message)
        self.message = message


class ResumableTransferDisposition(object):
    START_OVER = 'START_OVER'
    WAIT_BEFORE_RETRY = 'WAIT_BEFORE_RETRY'
    ABORT_CUR_PROCESS = 'ABORT_CUR_PROCESS'
    ABORT = 'ABORT'


class ResumableUploadException(Exception):
    __doc__ = '\n    Exception raised for various resumable upload problems.\n\n    self.disposition is of type ResumableTransferDisposition.\n    '

    def __init__(self, message, disposition):
        super(ResumableUploadException, self).__init__(message, disposition)
        self.message = message
        self.disposition = disposition

    def __repr__(self):
        return 'ResumableUploadException("%s", %s)' % (
         self.message, self.disposition)


class ResumableDownloadException(Exception):
    __doc__ = '\n    Exception raised for various resumable download problems.\n\n    self.disposition is of type ResumableTransferDisposition.\n    '

    def __init__(self, message, disposition):
        super(ResumableDownloadException, self).__init__(message, disposition)
        self.message = message
        self.disposition = disposition

    def __repr__(self):
        return 'ResumableDownloadException("%s", %s)' % (
         self.message, self.disposition)


class TooManyRecordsException(Exception):
    __doc__ = '\n    Exception raised when a search of Route53 records returns more\n    records than requested.\n    '

    def __init__(self, message):
        super(TooManyRecordsException, self).__init__(message)
        self.message = message


class PleaseRetryException(Exception):
    __doc__ = '\n    Indicates a request should be retried.\n    '

    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __repr__(self):
        return 'PleaseRetryException("%s", %s)' % (
         self.message,
         self.response)
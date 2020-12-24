# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/exception.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 17106 bytes
__doc__ = '\nException classes - Subclassing allows you to check for specific errors\n'
import base64, xml.sax, boto
from boto import handler
from boto.compat import json, StandardError
from boto.resultset import ResultSet

class BotoClientError(StandardError):
    """BotoClientError"""

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
    """StoragePermissionsError"""
    pass


class S3PermissionsError(StoragePermissionsError):
    """S3PermissionsError"""
    pass


class GSPermissionsError(StoragePermissionsError):
    """GSPermissionsError"""
    pass


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
    """StorageCreateError"""

    def __init__(self, status, reason, body=None):
        self.bucket = None
        super(StorageCreateError, self).__init__(status, reason, body)

    def endElement(self, name, value, connection):
        if name == 'BucketName':
            self.bucket = value
        else:
            return super(StorageCreateError, self).endElement(name, value, connection)


class S3CreateError(StorageCreateError):
    """S3CreateError"""
    pass


class GSCreateError(StorageCreateError):
    """GSCreateError"""
    pass


class StorageCopyError(BotoServerError):
    """StorageCopyError"""
    pass


class S3CopyError(StorageCopyError):
    """S3CopyError"""
    pass


class GSCopyError(StorageCopyError):
    """GSCopyError"""
    pass


class SQSError(BotoServerError):
    """SQSError"""

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
    """SQSDecodeError"""

    def __init__(self, reason, message):
        super(SQSDecodeError, self).__init__(reason, message)
        self.message = message

    def __repr__(self):
        return 'SQSDecodeError: %s' % self.reason

    def __str__(self):
        return 'SQSDecodeError: %s' % self.reason


class StorageResponseError(BotoServerError):
    """StorageResponseError"""

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
    """S3ResponseError"""
    pass


class GSResponseError(StorageResponseError):
    """GSResponseError"""
    pass


class EC2ResponseError(BotoServerError):
    """EC2ResponseError"""

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
    """JSONResponseError"""

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
    """EmrResponseError"""
    pass


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
    """SDBResponseError"""
    pass


class AWSConnectionError(BotoClientError):
    """AWSConnectionError"""
    pass


class StorageDataError(BotoClientError):
    """StorageDataError"""
    pass


class S3DataError(StorageDataError):
    """S3DataError"""
    pass


class GSDataError(StorageDataError):
    """GSDataError"""
    pass


class InvalidUriError(Exception):
    """InvalidUriError"""

    def __init__(self, message):
        super(InvalidUriError, self).__init__(message)
        self.message = message


class InvalidAclError(Exception):
    """InvalidAclError"""

    def __init__(self, message):
        super(InvalidAclError, self).__init__(message)
        self.message = message


class InvalidCorsError(Exception):
    """InvalidCorsError"""

    def __init__(self, message):
        super(InvalidCorsError, self).__init__(message)
        self.message = message


class NoAuthHandlerFound(Exception):
    """NoAuthHandlerFound"""
    pass


class InvalidLifecycleConfigError(Exception):
    """InvalidLifecycleConfigError"""

    def __init__(self, message):
        super(InvalidLifecycleConfigError, self).__init__(message)
        self.message = message


class ResumableTransferDisposition(object):
    START_OVER = 'START_OVER'
    WAIT_BEFORE_RETRY = 'WAIT_BEFORE_RETRY'
    ABORT_CUR_PROCESS = 'ABORT_CUR_PROCESS'
    ABORT = 'ABORT'


class ResumableUploadException(Exception):
    """ResumableUploadException"""

    def __init__(self, message, disposition):
        super(ResumableUploadException, self).__init__(message, disposition)
        self.message = message
        self.disposition = disposition

    def __repr__(self):
        return 'ResumableUploadException("%s", %s)' % (
         self.message, self.disposition)


class ResumableDownloadException(Exception):
    """ResumableDownloadException"""

    def __init__(self, message, disposition):
        super(ResumableDownloadException, self).__init__(message, disposition)
        self.message = message
        self.disposition = disposition

    def __repr__(self):
        return 'ResumableDownloadException("%s", %s)' % (
         self.message, self.disposition)


class TooManyRecordsException(Exception):
    """TooManyRecordsException"""

    def __init__(self, message):
        super(TooManyRecordsException, self).__init__(message)
        self.message = message


class PleaseRetryException(Exception):
    """PleaseRetryException"""

    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __repr__(self):
        return 'PleaseRetryException("%s", %s)' % (
         self.message,
         self.response)
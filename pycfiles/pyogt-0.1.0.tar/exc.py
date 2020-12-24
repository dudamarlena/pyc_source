# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/exc.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'

class Error(Exception):
    """base exception for all pyogp related exceptions"""
    __module__ = __name__


class AgentError(Error):
    """ general Agent exception """
    __module__ = __name__


class LoginError(Error):
    """ raised if there is an error in login """
    __module__ = __name__

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'Agent login error: %s' % self.error


class ParseStartLocError(LoginError):
    """ raised when the is an error in parsing the user specified start location """
    __module__ = __name__

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'Invalid start location specified, using defaults in settings'


class NetworkError(Error):
    """general network exception"""
    __module__ = __name__


class HTTPError(NetworkError):
    """an HTTP error"""
    __module__ = __name__

    def __init__(self, code, msg, fp, details=''):
        """initialize this exception"""
        self.code = code
        self.msg = msg
        self.details = details
        self.fp = fp

    def __str__(self):
        """return a string representation"""
        return '%s %s' % (self.code, self.msg)


class ResourceNotFound(NetworkError):
    """raised if a resource couldn't be found

    the URL to that resource is stored inside a ``url`` attribute.

    """
    __module__ = __name__

    def __init__(self, url=''):
        self.url = url

    def __str__(self):
        return self.url


class ResourceError(NetworkError):
    """raised if any other error occurred (usually a 500)

    contains ``url`` to the resource and ``code`` and ``message`` and ``body``

    """
    __module__ = __name__

    def __init__(self, url='', code='', message='', body='', method='GET'):
        self.url = url
        self.code = code
        self.message = message
        self.body = body
        self.method = method

    def __str__(self):
        """return a printable version"""
        return "Error using '%s' on resource '%s': %s (%s)" % (self.method, self.url, self.message, self.code)


class SerializationError(Error):
    """serialization related exceptions"""
    __module__ = __name__


class DeserializationError(Error):
    """deserialization related exception"""
    __module__ = __name__


class DeserializerNotFound(DeserializationError):
    """raised if a deserializer for a certain content type couldn't be found

    stores the content type inside a ``content_type`` attribute.
    """
    __module__ = __name__

    def __init__(self, content_type=''):
        self.content_type = content_type

    def __str__(self):
        return "deserialization for '%s' not supported" % self.content_type


class CredentialDeserializerNotFound(DeserializationError):
    """raised if a deserializer for a certain content type couldn't be found

    stores the content type inside a ``content_type`` attribute.
    """
    __module__ = __name__

    def __init__(self, payload=''):
        self.payload = payload

    def __str__(self):
        return "deserialization for payload '%s' not supported" % self.payload


class DeserializationFailed(DeserializationError):
    """raised if a deserializer couldn't deserialize a payload

    stores the payload inside a ``payload`` attribute and the error message
    inside a ``reason`` attribute.
    """
    __module__ = __name__

    def __init__(self, payload='', reason=''):
        self.payload = payload
        self.reason = reason

    def __str__(self):
        return "deserialization failed for '%s', reason: '%s'" % (self.payload, self.reason)


class MessageSystemError(Error):
    """message system related exception"""
    __module__ = __name__


class MessageTemplateNotFound(MessageSystemError):
    """ message template file not found

    stores the context in a ``context`` attribute
    """
    __module__ = __name__

    def __init__(self, context='', template=''):
        self.context = context
        self.template = template

    def __str__(self):
        return "No message template found, context: '%s'" % self.context


class MessageTemplateParsingError(MessageSystemError):
    """ message template parsing error

    stores the context in a ``context`` attribute
    """
    __module__ = __name__

    def __init__(self, context='', template=''):
        self.context = context
        self.template = template

    def __str__(self):
        return "Error parsing message template, context: '%s'" % self.context


class CircuitNotFound(MessageSystemError):
    """ circuit to host could not be found

    stores the host missing a circuit in a ``host`` attribute
    """
    __module__ = __name__

    def __init__(self, host='', reason=''):
        self.host = host
        self.reason = reason

    def __str__(self):
        return "No circuit to '%s' found, reason: '%s'" % (self.host, self.reason)


class MessageBuildingError(MessageSystemError):
    """ problem serializing packet data

    stores the label and reason in ``label`` and ``reason`` attributes
    """
    __module__ = __name__

    def __init__(self, label='', reason=''):
        self.label = label
        self.reason = reason

    def __str__(self):
        return "Error serializing '%s' due to reason: '%s'" % (self.label, self.reason)


class MessageSerializationError(MessageSystemError):
    """ problem serializing packet data

    stores the label and reason in ``label`` and ``reason`` attributes
    """
    __module__ = __name__

    def __init__(self, label='', reason=''):
        self.label = label
        self.reason = reason

    def __str__(self):
        return "Error serializing '%s' due to reason: '%s'" % (self.label, self.reason)


class MessageDeserializationError(MessageSystemError):
    """ problem deserializing packet data

    stores the label and reason in ``label`` and ``reason`` attributes
    """
    __module__ = __name__

    def __init__(self, label='', reason=''):
        self.label = label
        self.reason = reason

    def __str__(self):
        return "Error deserializing '%s' due to reason: '%s'" % (self.label, self.reason)


class DataUnpackingError(MessageSystemError):
    """ problem deserializing packet data

    stores the label and reason in ``label`` and ``reason`` attributes
    """
    __module__ = __name__

    def __init__(self, data='', reason=''):
        self.data = data
        self.reason = reason

    def __str__(self):
        return "Error serializing '%s' due to reason: '%s'" % (self.data, self.reason)


class AgentDomainError(Error):
    """base exception for all errors which can occur on an agent domain"""
    __module__ = __name__


class UserNotFound(AgentDomainError):
    """user couldn't be found

    This exception stores the credentials used inside a ``credentials`` attribute
    """
    __module__ = __name__

    def __init__(self, credentials=None):
        """initialize this exception"""
        self.credentials = credentials


class UserNotAuthorized(AgentDomainError):
    """an error raised in case a user couldn't be authorized

    stores the credentials used inside a ``credentials`` attribute

    """
    __module__ = __name__

    def __init__(self, credentials=None):
        """initialize this exception"""
        self.credentials = credentials


class UserRezFailed(AgentDomainError):
    """an error raised in case a user couldn't rez on a sim

    stores the region used inside a ``region`` attribute

    """
    __module__ = __name__

    def __init__(self, region=None):
        """initialize this exception"""
        self.region = region


class RegionDomainError(Error):
    """base exception for all errors which can occur on an region domain"""
    __module__ = __name__


class RegionSeedCapNotAvailable(RegionDomainError):
    """an error raised in case a user couldn't be authorized

    stores the cap used inside a ``cap`` attribute

    """
    __module__ = __name__

    def __init__(self, reason=None):
        """initialize this exception"""
        self.reason = reason

    def __str__(self):
        return "Region seed capability not found when %s'" % self.reason


class RegionCapNotAvailable(RegionDomainError):
    """an error raised in case a user couldn't be authorized

    stores the cap used inside a ``cap`` attribute

    """
    __module__ = __name__

    def __init__(self, cap=None):
        """initialize this exception"""
        self.cap = cap


class RegionMessageError(RegionDomainError):
    """ an error raised when a region does not have a connection
    over which it can send UDP messages 

    accepts a region object as an attribute

    """
    __module__ = __name__

    def __init__(self, region=None):
        """initialize this exception"""
        self.region = region

    def __str__(self):
        return "Agent has no udp connection enabled for: %s'" % self.region


class DataParsingError(Error):
    """ an error raised data parsing fails

    """
    __module__ = __name__

    def __init__(self, error=None):
        """initialize this exception"""
        self.error = error

    def __str__(self):
        return "Data parsing error: %s'" % self.error


class NotImplemented(Error):
    """ an error raised when method is not implemented """
    __module__ = __name__

    def __init__(self, error=None):
        """ initialize this exception """
        self.error = error

    def __str__(self):
        return 'This method has to be implemented here: %s' % self.error


class Deprecated(Error):
    """ an error raised when method is not implemented """
    __module__ = __name__

    def __init__(self, thing=None):
        """ initialize this exception """
        self.thing = thing

    def __str__(self):
        return 'This thing is deprecated: %s' % self.thing
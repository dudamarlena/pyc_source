# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/matanui/request.py
# Compiled at: 2011-01-17 15:28:14
"""Provides a structure for container objects of a request."""
__author__ = 'Guy K. Kloss <Guy.Kloss@aut.ac.nz>'
import urllib, json
from matanui import API_VERSION
from matanui.exceptions import MataNuiServiceException
CONTENT = 'content'
INFO = 'info'
METADATA = 'metadata'
LIST = 'list'

class Request(object):
    """
    Provides a parser structure for processing the server request.
    """
    SWITCH_INDICATOR = '$'
    OBJECT_ID_SWITCH = 'id_'
    SWITCHES = [OBJECT_ID_SWITCH]
    ACCEPT_HEADER_BASE = 'application/x.matanui.'
    DEFAULT_ACCEPT_HEADER = ACCEPT_HEADER_BASE + 'content-v' + API_VERSION

    def __init__(self, environment):
        """
        Constructor.
        
        @param environment: The WSGI environment.
        @type environment: C{dict}
        """
        self.environment = environment
        self.path = None
        self.object_id = None
        self.content_request = CONTENT
        self.query = None
        self.content_type = None
        self.encoding = None
        self.version = None
        self.username = None
        if self.environment:
            self._parse()
        return

    def _parse(self):
        """
        Parses the request, extracts vital information for the service.
        """
        self._parse_accept_headers()
        self._parse_query_parameters()
        self._parse_path()
        self.username = self.environment.get('SSL_CLIENT_I_DN', None)
        return

    def _split_accept_header(self):
        """
        Splits the fields in the accept header, and returns a list of accepted
        types sorted by the given C{q} values.
        
        @return: Accepted types.
        @rtype: C{list}
        """
        accept_header = self.environment.get('HTTP_ACCEPT', '*/*')
        if not accept_header:
            accept_header = '*/*'
        parts = [ x.strip().split(';') for x in accept_header.split(',') ]
        for part in parts:
            if len(part) == 1:
                part.append(1.0)
            elif len(part) == 2:
                part[1] = float(part[1][2:])
            else:
                status = (
                 400,
                 '"Funky" declaration in accept header: %s' % accept_header)
                raise MataNuiServiceException("Can't parse accept header: %s" % status, status)

        parts.sort(reverse=True, key=lambda x: x[1])
        return [ item[0] for item in parts ]

    def _parse_accept_type(self, accept_type):
        """
        Parse the "Accept" header type, which defines what the client accepts,
        and therefore determines what we need to deliver here.
        
        @param accept_type: The type to parse for acceptability.
        @type accept_type: C{str}
        
        @return: Parse result (kind, encoding, API) and status (code, message).
        @rtype: C{tupel}
        """
        status = (200, '')
        if accept_type == '*/*':
            accept_type = self.DEFAULT_ACCEPT_HEADER
        if not accept_type.startswith(self.ACCEPT_HEADER_BASE):
            status = (
             406,
             'Unsupported type in accept header: %s' % accept_type)
        accept_type = accept_type[len(self.ACCEPT_HEADER_BASE):]
        parts = accept_type.split('+')
        accept_encoding = None
        if len(parts) == 2:
            accept_encoding = parts[1]
        elif len(parts) > 2:
            status = (
             406,
             'Ambiguous specification for encoding: "%s"' % ('+').join(parts[1:]))
        if accept_encoding is not None and accept_encoding.lower() != 'json':
            status = (
             406, 'Encoding "%s" not supported.' % accept_encoding)
        parts = parts[0].split('-')
        api_version = 'v' + API_VERSION
        if len(parts) == 2:
            api_version = parts[1]
        elif len(parts) > 2:
            status = (
             406,
             'Ambiguous specification of version: "%s"' % ('-').join(parts[1:]))
        if api_version == 'v' + API_VERSION:
            api_version = api_version[1:]
        else:
            status = (
             406, 'API version "%s" not supported' % api_version)
        content_switch = parts[0]
        content_request = None
        if content_switch == INFO:
            content_request = content_switch
        elif content_switch in ('metadata', 'list'):
            content_request = content_switch
            if accept_encoding is None or accept_encoding.lower() != 'json':
                message = 'Encoding "%s" not supported for meta-data or listing.' % accept_encoding
                status = (406, message)
        elif content_switch == CONTENT:
            content_request = content_switch
        else:
            status = (
             406,
             'Content request "%s" not supported' % content_switch)
        return ((content_request, accept_encoding, api_version), status)

    def _parse_accept_headers(self):
        """
        Determine all the accept types (in order of desirability), and try them
        one by one until we find one that suits our purpose.
        """
        accept_types = self._split_accept_header()
        status = None
        while status != (200, ''):
            if accept_types:
                accept_type = accept_types.pop(0)
            else:
                status = (406, 'No suitable accept header type found.')
            (parse_result, status) = self._parse_accept_type(accept_type)

        if status[0] != 200:
            raise MataNuiServiceException('HTTP error (for last accept header type) %s: %s' % status, status)
        (content_request, accept_encoding, api_version) = parse_result
        self.content_request = content_request
        self.encoding = accept_encoding
        self.version = api_version
        return

    def _parse_query_parameters(self):
        """Parses all query parameters (in the URI after the '?')."""
        query_string = self.environment['QUERY_STRING']
        if query_string:
            self.query = dict(x.split('=') for x in query_string.split('&'))
        else:
            return
        try:
            for (key, value) in self.query.items():
                value_string = urllib.unquote_plus(value)
                self.query[key] = json.loads(value_string)

        except ValueError:
            message = 'Error parsing query'
            status = (400, message)
            raise MataNuiServiceException('Incorrect URL encoded JSON data structure', status)

    def _parse_path(self):
        """Parses the URI's path."""
        http_path = self.environment['PATH_INFO']
        if self.SWITCH_INDICATOR in http_path:
            switch_indicator_index = http_path.index(self.SWITCH_INDICATOR)
            switches = http_path[switch_indicator_index + 1:]
            http_path = http_path[:switch_indicator_index]
            indicators = switches.split(self.SWITCH_INDICATOR)
            i = 0
            object_ids = []
            while i < len(indicators):
                if indicators[i].startswith(self.OBJECT_ID_SWITCH):
                    object_ids.append(indicators.pop(i)[3:])

            if len(object_ids) > 1:
                status = (400, 'Only one object ID allowed.')
                raise MataNuiServiceException('HTTP error %s: %s' % status, status)
            elif len(object_ids) == 1:
                self.object_id = object_ids[0]
            if indicators:
                status = (
                 400,
                 'Unknown switches: %s' % str(indicators))
                raise MataNuiServiceException('HTTP error %s: %s' % status, status)
        self.path = http_path

    def __repr__(self):
        res = []
        for (attribute, value) in self.__dict__.items():
            if not attribute.startswith('_'):
                res.append('%s=%s' % (attribute, value.__repr__()))

        return '%s(%s)' % (self.__class__.__name__, (', ').join(res))
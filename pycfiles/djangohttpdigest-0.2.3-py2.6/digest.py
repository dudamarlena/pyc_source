# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djangohttpdigest/digest.py
# Compiled at: 2011-04-16 15:59:35
"""
Helper functions and algorithms for computing HTTP digest thingies.
"""
from time import time
import urllib2
from md5 import md5
__all__ = ('Digestor', 'parse_authorization_header', 'check_credentials', 'check_hardcoded_authentication')

def parse_authorization_header(header):
    """ Parse requests authorization header into list.
    Raise ValueError if some problem occurs. """
    if not header.startswith('Digest '):
        raise ValueError('Header do not start with Digest')
    header = header[len('Digest '):]
    items = urllib2.parse_http_list(header)
    params = urllib2.parse_keqv_list(items)
    required = [
     'username', 'realm', 'nonce', 'uri', 'response']
    for field in required:
        if not params.has_key(field):
            raise ValueError('Required field %s not found' % field)

    if params.has_key('qop') and not params.has_key('cnonce') and params.has_key('cn'):
        raise ValueError('qop sent without cnonce and cn')
    return params


class Digestor(object):
    """ Main class for handling digest algorithms as described in RFC 2617 """
    algorithm_implementation_map = {'md5': md5}

    def __init__(self, method, path, realm=None, qop=None, opaque=None, algorithm=None, username=None, password=None):
        object.__init__(self)
        self.method = method
        self.path = path
        self.algorithm = algorithm or 'md5'
        self.opaque = opaque or 'ToDoMoveThisToSettings'
        self.qop = qop or 'auth'
        self.realm = realm or None
        self.parsed_header = None
        assert self.algorithm in self.algorithm_implementation_map
        return

    def get_a1(self, realm, username, password):
        return self.algorithm_implementation_map[self.algorithm]('%s:%s:%s' % (username, realm, password)).hexdigest()

    def get_digest_challenge(self):
        """ Return HTTP digest challenge, which has to be placed into www-authenticate header"""
        nonce = self.algorithm_implementation_map[self.algorithm]('%s:%s' % (time(), self.realm)).hexdigest()
        return 'Digest realm="%(realm)s", qop="%(qop)s", nonce="%(nonce)s", opaque="%(opaque)s"' % {'realm': self.realm, 
           'qop': self.qop, 
           'nonce': nonce, 
           'opaque': self.opaque}

    def get_client_secret(self):
        """ Get secret as computed by client """
        return self.parsed_header['response']

    def get_server_secret(self, a1):
        """ Compute server secret from provided, partially computed values """
        assert 'auth' == self.parsed_header['qop']
        a2 = self.algorithm_implementation_map[self.algorithm]('%s:%s' % (self.method, self.path)).hexdigest()
        request_digest = '%s:%s:%s:%s:%s' % (
         self.parsed_header['nonce'],
         self.parsed_header['nc'],
         self.parsed_header['cnonce'],
         self.parsed_header['qop'],
         a2)
        return self.algorithm_implementation_map[self.algorithm]('%s:%s' % (a1, request_digest)).hexdigest()

    def parse_authorization_header(self, header):
        """ Provide wrap around parse_authorization_header function for those who like to have
        everything with digest.
        This also stores parsed header in instvar, so we must not passing it around.
        """
        self.parsed_header = parse_authorization_header(header)
        return self.parsed_header

    def get_client_username(self):
        return self.parsed_header['username']
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/entity_statement/collect_old.py
# Compiled at: 2019-09-23 08:35:48
# Size of source mod 2**32: 3681 bytes
import json, logging
from urllib.parse import urlencode, urlparse
import requests
from cryptojwt.jws.jws import factory
REL = 'http://oauth.net/specs/federation/1.0/entity'
logger = logging.getLogger(__name__)

class HTTPError(Exception):
    pass


class Issuer(object):

    def __init__(self, jws):
        self.jws = jws
        self.superior = []

    def paths(self):
        res = []
        if not self.superior:
            return [
             [
              self.jws]]
        for sup in self.superior:
            for p in sup.paths():
                l = [
                 self.jws]
                l.extend(p)
                res.append(l)

        return res

    def __iter__(self):
        for path in self.paths():
            yield path

    def is_leaf(self):
        for sup in self.superior:
            if 'sub_is_leaf' in sup.jws:
                return True

        return False


class Collector(object):

    def __init__(self, httpd=None, trusted_roots=None):
        self.seen = []
        self.httpd = httpd or requests.request
        self.trusted_roots = trusted_roots

    def load_entity_statements(self, iss, sub, op='', aud='', prefetch=False):
        """
        Fetches an entity statement from a metadata API endpoint according to
        section 4.2.1

        :param iss: The issuer of the signed information
        :param sub: The subject about which the information is wanted
        :param op: The operation that should be performed.
        :param aud: The entity identifier of the requester
        :param prefetch: If set to "true", it indicates that the requester would
            like the API to prefetch entity statements that may be relevant.
        :return: A JSON encoded list of signed entity statements
        """
        qpart = {'iss':iss, 
         'sub':sub}
        if aud:
            qpart['aud'] = aud
        if prefetch:
            qpart['prefetch'] = prefetch
        p = urlparse(iss)
        _qurl = '{}://{}/.well-known/openid-federation?{}'.format(p.scheme, p.netloc, urlencode(qpart))
        logger.debug('metadata API url:{}'.format(_qurl))
        hres = self.httpd('GET', _qurl, verify=False)
        if hres.status_code >= 400:
            raise HTTPError(hres.text)
        _msg = hres.text.strip('"')
        if _msg.startswith('['):
            return json.loads(_msg)
        return _msg

    def follow_path(self, iss, sub):
        """
        Unravel a branch

        :param iss: The issuer I want to ask
        :param sub: The entity I want to ask about
        :return: An Issuer instance
        """
        _jarr = self.load_entity_statements(iss, sub)
        if _jarr:
            return self.collect_entity_statements(_jarr)

    def collect_entity_statements(self, jarr):
        """
        Collect information from the immediate superiors

        :param jarr: Array of Signed JSON Web Token
        :return: A tree of entity statements
        """
        if isinstance(jarr, list):
            _token = jarr[0]
        else:
            _token = jarr
        _jwt = factory(_token)
        if _jwt:
            entity_statement = _jwt.jwt.payload()
        else:
            return
            node = Issuer(_token)
            if 'authority_hints' not in entity_statement:
                return node
            for authority in entity_statement['authority_hints']:
                if authority in self.seen:
                    node.superior.append(self.seen[authority])
                else:
                    _node = self.follow_path(authority, entity_statement['iss'])
                if _node:
                    node.superior.append(_node)

            return node
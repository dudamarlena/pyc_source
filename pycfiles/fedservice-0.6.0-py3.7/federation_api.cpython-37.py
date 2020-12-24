# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/federation_api.py
# Compiled at: 2019-04-17 09:29:37
# Size of source mod 2**32: 4034 bytes
import json, logging, os
from urllib.parse import unquote_plus
from fedservice.exception import FederationAPIError
from fedservice.metadata_api.db import db_make_entity_statement
from fedservice.metadata_api.fs import make_entity_statement
from fedservice.metadata_api.fs import mk_path
logger = logging.getLogger(__name__)

class FederationAPI(object):

    def __init__(self, static_dir='static'):
        self.static_dir = static_dir

    def resolve_metadata(self, respondent, peer, type, anchor):
        """
        Evaluate a trust path of another entity

        :param respondent: The entity ID of the entity's who's metadata
            is requested.
        :param peer: The entity identifier of the entity the information is
            requested for. This must be a leaf entity.
        :param type: The metadata type to resolve.
        :param anchor: The trust anchor the remote peer MUST use when resolving
            the metadata.
        :return:
        """
        return 'OK'

    def listing(self, **kwargs):
        raise NotImplementedError()

    def entity_statement(self, **kwargs):
        raise NotImplementedError()

    def __call__(self, **kwargs):
        try:
            _operation = kwargs['op']
        except KeyError:
            _operation = 'fetch'

        if _operation == 'fetch':
            return (self.entity_statement)(**kwargs)
        if _operation == 'resolve_metadata':
            return (self.resolve_metadata)(**kwargs)
        if _operation == 'listing':
            return (self.listing)(**kwargs)
        raise FederationAPIError('Unknown operation')


class FederationAPIFS(FederationAPI):

    def __init__(self, base_url, data_dir='.', static_dir='static'):
        FederationAPI.__init__(self, static_dir)
        self.base_url = base_url
        self.data_dir = data_dir

    def entity_statement(self, **kwargs):
        jws = make_entity_statement((self.base_url), (self.data_dir), **kwargs)
        return jws

    def _list(self, dir, path=''):
        res = []
        for s in os.listdir(dir):
            _sub = os.path.join(dir, s)
            if os.path.isdir(_sub):
                if s.startswith('http'):
                    res.append(unquote_plus(s))
                else:
                    if path:
                        res.append('{}/{}/{}'.format(self.base_url, path, s))
                    else:
                        res.append('{}/{}'.format(self.base_url, s))
                res.extend(self._list(_sub, s))

        return res

    def listing(self, **kwargs):
        """
        List the subordinates of this intermediate

        :param kwargs:
        :return:
        """
        try:
            iss = kwargs['iss']
        except KeyError:
            raise FederationAPIError('Missing required argument')

        _iss_dir = mk_path(self.data_dir, iss)
        if not os.path.isdir(_iss_dir):
            raise FederationAPIError('No such issuer')
        return json.dumps(self._list(_iss_dir))


class FederationAPIDb(FederationAPI):

    def __init__(self, authn_info, db_uri, key_jar, issuer, static_dir='static', lifetime=14400, sign_alg='ES256'):
        FederationAPI.__init__(self, static_dir)
        self.authn_info = authn_info
        self.db_uri = db_uri
        self.key_jar = key_jar
        self.issuer = issuer
        self.lifetime = lifetime
        self.sign_alg = sign_alg

    def entity_statement(self, **kwargs):
        if 'iss' in kwargs:
            if kwargs['iss'] != self.issuer:
                raise FederationAPIError('Not prepared to sign as "{}"'.format(kwargs['iss']))
        else:
            kwargs['iss'] = self.issuer
        jws = db_make_entity_statement(self.db_uri, key_jar=self.key_jar, lifetime=self.lifetime, 
         sign_alg=self.sign_alg, 
         authn_info=self.authn_info, **kwargs)
        return json.dumps(jws)
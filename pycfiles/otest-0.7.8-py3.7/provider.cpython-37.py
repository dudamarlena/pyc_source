# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/rp/provider.py
# Compiled at: 2019-04-05 15:39:26
# Size of source mod 2**32: 9071 bytes
import json, time
from future.backports.urllib.parse import parse_qs
from Cryptodome.PublicKey import RSA
from jwkest.ecc import P256
from jwkest.jwk import RSAKey
from jwkest.jwk import ECKey
from jwkest.jwk import SYMKey
from oic.extension import provider
from oic.extension.message import RegistrationRequest
from oic.oauth2.message import AccessTokenRequest
from oic.oauth2.message import ASConfigurationResponse
from oic.utils.keyio import keyjar_init
from otest.events import EV_PROTOCOL_REQUEST
from otest.events import EV_HTTP_RESPONSE
__author__ = 'roland'

class TestError(Exception):
    pass


def sort_string(string):
    if string is None:
        return ''
    _l = list(string)
    _l.sort()
    return ''.join(_l)


class Provider(provider.Provider):

    def __init__(self, name, sdb, cdb, authn_broker, userinfo, authz, client_authn, symkey, urlmap=None, ca_certs='', keyjar=None, hostname='', template_lookup=None, template=None, verify_ssl=True, capabilities=None, event_db=None, config=None, **kwargs):
        (provider.Provider.__init__)(
 self, name, sdb, cdb, authn_broker, authz=authz, client_authn=client_authn, 
         symkey=symkey, urlmap=urlmap, ca_bundle=ca_certs, 
         keyjar=keyjar, hostname=hostname, verify_ssl=verify_ssl, 
         capabilities=capabilities, config=config, **kwargs)
        self.claims_type = [
         'normal']
        self.behavior_type = []
        self.server.behavior_type = self.behavior_type
        self.claim_access_token = {}
        self.init_keys = []
        self.update_key_use = ''
        self.events = event_db
        self.userinfo = userinfo
        self.template_lookup = template_lookup
        self.template = template
        self.strict = False

    def create_providerinfo(self, pcr_class=ASConfigurationResponse, setup=None):
        _response = provider.Provider.create_providerinfo(self, pcr_class, setup)
        if 'isso' in self.behavior_type:
            _response['issuer'] = 'https://example.com'
        return _response

    def check_scheme(self, reg_req):
        for endp in ('redirect_uris', 'jwks_uri', 'initiate_login_uri'):
            try:
                uris = reg_req[endp]
            except KeyError:
                continue

            if not isinstance(uris, list):
                uris = [
                 uris]
            for uri in uris:
                if not uri.startswith('https://'):
                    return self._error(error='invalid_configuration_parameter',
                      descr=("Non-HTTPS endpoint in '{}'".format(endp)))

    def registration_endpoint(self, request, authn=None, **kwargs):
        try:
            reg_req = RegistrationRequest().deserialize(request, 'json')
        except ValueError:
            reg_req = RegistrationRequest().deserialize(request)

        self.events.store(EV_PROTOCOL_REQUEST, reg_req)
        if self.strict:
            resp = self.check_scheme(reg_req)
            if resp:
                return resp
        _response = (provider.Provider.registration_endpoint)(self, request=request, authn=authn, **kwargs)
        self.init_keys = []
        if 'jwks_uri' in reg_req:
            if _response.status == '200 OK':
                req_resp = ASConfigurationResponse().from_json(_response.message)
                for kb in self.keyjar[req_resp['client_id']]:
                    if kb.imp_jwks:
                        self.trace.info('Client JWKS: {}'.format(kb.imp_jwks))

        return _response

    def authorization_endpoint(self, request='', cookie=None, **kwargs):
        _req = parse_qs(request)
        _response = (provider.Provider.authorization_endpoint)(self, request, 
         cookie, **kwargs)
        try:
            _resp = self.server.http_request(_req['request_uri'][0])
        except KeyError:
            pass
        else:
            if _resp.status_code == 200:
                self.events.store(EV_HTTP_RESPONSE, _resp)

    def token_endpoint(self, request='', authn=None, **kwargs):
        try:
            req = AccessTokenRequest().deserialize(request, 'urlencoded')
            client_id = self.client_authn(self, req, authn)
        except Exception as err:
            try:
                self.trace.error('Failed to verify client due to: %s' % err)
                return self._error(error='incorrect_behavior', descr='Failed to verify client')
            finally:
                err = None
                del err

        if self.events:
            self.events.store(EV_PROTOCOL_REQUEST, req)
        try:
            self._update_client_keys(client_id)
        except TestError:
            return self._error(error='incorrect_behavior', descr='No change in client keys')
        else:
            _response = (provider.Provider.token_endpoint)(
 self, authn=authn, request=request, **kwargs)
            return _response

    def generate_jwks(self, mode):
        if 'rotenc' in self.behavior_type:
            rsa_key = RSAKey(kid=('rotated_rsa_{}'.format(time.time())), use='enc').load_key(RSA.generate(2048))
            ec_key = ECKey(kid=('rotated_ec_{}'.format(time.time())), use='enc').load_key(P256)
            keys = [
             rsa_key.serialize(private=True),
             ec_key.serialize(private=True)]
            new_keys = {'keys': keys}
            signing_keys = [k.to_dict() for k in self.keyjar.get_signing_key()]
            new_keys['keys'].extend(signing_keys)
            return json.dumps(new_keys)
            if 'nokid1jwk' in self.behavior_type:
                alg = mode['sign_alg']
                if not alg:
                    alg = 'RS256'
                keys = [k.to_dict() for kb in self.keyjar[''] for k in list(kb.keys())]
                for key in keys:
                    if key['use'] == 'sig' and key['kty'].startswith(alg[:2]):
                        key.pop('kid', None)
                        jwk = dict(keys=[key])
                        return json.dumps(jwk)

                raise Exception('Did not find sig {} key for nokid1jwk test '.format(alg))
        else:
            keys = [k.to_dict() for kb in self.keyjar[''] for k in list(kb.keys())]
            jwks = dict(keys=keys)
            return json.dumps(jwks)

    def _update_client_keys(self, client_id):
        if 'updkeys' in self.behavior_type:
            if not self.init_keys:
                if 'rp_enc_key' in self.baseurl:
                    self.update_key_use = 'enc'
                else:
                    self.update_key_use = 'sig'
                self.init_keys = []
                for kb in self.keyjar[client_id]:
                    for key in kb.available_keys():
                        if isinstance(key, SYMKey):
                            continue
                        if key.use == self.update_key_use:
                            self.init_keys.append(key)

            else:
                for kb in self.keyjar[client_id]:
                    self.events.store('Updating client keys', '')
                    kb.update()
                    if kb.imp_jwks:
                        self.events.store('Client JWKS´', kb.imp_jwks)

                same = 0
                for kb in self.keyjar[client_id]:
                    for key in kb.available_keys():
                        if isinstance(key, SYMKey):
                            continue
                        if key.use == self.update_key_use:
                            if key in self.init_keys:
                                same += 1
                            else:
                                self.events.store('New key', key)

                if same == len(self.init_keys):
                    self.events.store('No change in keys')
                    raise TestError('Keys unchanged')
                else:
                    self.events.store('Key modifications', '{} changed, {} same'.format(len(self.init_keys) - same, same))

    def __setattr__(self, key, value):
        if key == 'keys':
            keyjar_init(self, value)
        else:
            super(provider.Provider, self).__setattr__(key, value)

    def _get_keyjar(self):
        return self.server.keyjar

    def _set_keyjar(self, item):
        self.server.keyjar = item

    keyjar = property(_get_keyjar, _set_keyjar)
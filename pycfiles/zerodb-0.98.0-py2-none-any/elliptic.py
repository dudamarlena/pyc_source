# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/permissions/elliptic.py
# Compiled at: 2016-07-10 18:14:13
"""
Module for auth with elliptic curve cryptography
"""
__module_name__ = 'auth_secp256k1_scrypt'
import ecdsa, hashlib, scrypt, struct
from ZEO import auth
from ZEO.auth.base import Client as BaseClient
from ZEO.auth import register_module
from ZEO.Exceptions import AuthError
from . import base
from . import subdb
from zerodb.crypto import rand
from zerodb.crypto import ecc

class ServerStorageMixin(object):
    curve = ecdsa.SECP256k1

    def auth_get_challenge(self):
        """Return realm, challenge, and nonce."""
        self._challenge = rand(32)
        self._key_nonce = self._get_nonce()
        return (self.auth_realm, self._challenge, self._key_nonce)

    def auth_response(self, resp):
        username, challenge, resp_sig = resp
        assert self._challenge == challenge
        user = self.database[username]
        verkey = ecc.public(user.pubkey, curve=self.curve)
        h_up = hashlib.sha256('%s:%s:%s' % (username.encode(), self.database.realm.encode(), user.pubkey)).digest()
        check = hashlib.sha256('%s:%s' % (h_up, challenge)).digest()
        verify = verkey.verify(resp_sig, check)
        if verify:
            self.connection.setSessionKey(base.session_key(h_up, self._key_nonce))
        authenticated = self._finish_auth(verify)
        if authenticated:
            user_id = self.database.db_root['usernames'][username]
            self.user_id = struct.pack(self.database.uid_pack, user_id)
        return authenticated


class StorageClass(ServerStorageMixin, subdb.StorageClass):
    pass


class Client(BaseClient):
    extensions = [
     'auth_get_challenge', 'auth_response', 'get_root_id']
    curve = ecdsa.SECP256k1

    @classmethod
    def kdf(cls, seed, salt):
        return scrypt.hash(seed, salt)[:cls.curve.baselen]

    def start(self, username, realm, password):
        priv = ecc.private(password, [username, realm], kdf=self.kdf, curve=self.curve)
        _realm, challenge, nonce = self.stub.auth_get_challenge()
        if _realm != realm:
            raise AuthError('expected realm %r, got realm %r' % (
             _realm, realm))
        h_up = hashlib.sha256('%s:%s:%s' % (username.encode(), realm.encode(), priv.get_pubkey())).digest()
        check = hashlib.sha256('%s:%s' % (h_up, challenge)).digest()
        sig = priv.sign(check)
        result = self.stub.auth_response((username, challenge, sig))
        if result:
            return base.session_key(h_up, nonce)
        else:
            return
            return


def register_auth():
    if __module_name__ not in auth._auth_modules:
        register_module(__module_name__, StorageClass, Client, base.PermissionsDatabase)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\tools\ssh_cert_loader.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 1563 bytes
from asn1crypto import keys, pem
import rsa
from rsa import pkcs1

class SSHPrivKey:

    def __init__(self, privkey=None):
        self.name = 'ssh-rsa'
        self.privkey = privkey

    @staticmethod
    def load_privkey_from_string(pk_str):
        """
                Loads a PEM encoded RSA private key
                Format must be the same as /etc/ssh/ssh_host_rsa_key
                (openssl RSA private key)
                """
        pk = SSHPrivKey()
        pk.privkey = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')
        return pk

    @staticmethod
    def load_privkey_from_file(filename):
        with open(filename, 'rb') as (f):
            return SSHPrivKey.load_privkey_from_string(f.read())

    def sign(self, data):
        """
                hashes the data with sha1 and signs the result using pkcs1.5 and SHA-1
                returns bytes
                data must be bytes!
                """
        return pkcs1.sign(data, self.privkey, 'SHA-1')


class OpenSSLRSAPrivateKey:

    def __init__(self):
        self.p = None
        self.q = None
        self.e = None


with open('ssh_server_test_cert.priv', 'rb') as (f):
    type_name, headers, der_bytes = pem.unarmor(f.read())
    object = keys.RSAPrivateKey.load(der_bytes)
    print(object['modulus'].native)
    print(object.native)
with open('ssh_server_test_cert.priv', 'rb') as (f):
    keydata = f.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')
    print(privkey)
a = pkcs1.sign('alma'.encode(), privkey, 'SHA-1')
pk = SSHPrivKey.load_privkey_from_file('ssh_server_test_cert.priv')
print()
print(pk.sign('alma'.encode()))
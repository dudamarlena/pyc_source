# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/lib/optestlib.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 4146 bytes
from sys import exit as sys_exit
from base64 import b64decode as base64_b64decode, urlsafe_b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
from binascii import a2b_hex as binascii_a2b_hex
from json import loads as json_loads
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import GCM
from cryptography.hazmat.primitives.ciphers.base import Cipher
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers, RSAPrivateNumbers
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import onepassword_local_search.exceptions.ManagedException as ManagedException
import six, struct

def aes_decrypt(ct, key, iv, tag):
    cipher = Cipher(AES(key), GCM(iv), default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize_with_tag(tag)


def intarr2long(arr):
    return int(''.join(['%02x' % byte for byte in arr]), 16)


def base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode('ascii')
    _d = urlsafe_b64decode(bytes(data) + b'==')
    return intarr2long(struct.unpack('%sB' % len(_d), _d))


def rsa_decrypt(key_raw, ct):
    jwk = json_loads(key_raw)
    public_numbers = RSAPublicNumbers(base64_to_long(jwk['e']), base64_to_long(jwk['n']))
    private_numbers = RSAPrivateNumbers(base64_to_long(jwk['p']), base64_to_long(jwk['q']), base64_to_long(jwk['d']), base64_to_long(jwk['dp']), base64_to_long(jwk['dq']), base64_to_long(jwk['qi']), public_numbers)
    private_key = private_numbers.private_key(backend=(default_backend()))
    pem = private_key.private_bytes(encoding=(serialization.Encoding.PEM),
      format=(serialization.PrivateFormat.TraditionalOpenSSL),
      encryption_algorithm=(serialization.NoEncryption()))
    decryptor = serialization.load_pem_private_key(pem,
      password=None,
      backend=(default_backend()))
    plain = decryptor.decrypt(get_binary_from_string(ct), padding.OAEP(mgf=padding.MGF1(algorithm=(hashes.SHA1())),
      algorithm=(hashes.SHA1()),
      label=None))
    return plain


def opb64d(b64dat):
    try:
        out = base64_b64decode(b64dat, altchars='-_')
    except:
        try:
            out = base64_b64decode((b64dat + '='), altchars='-_')
        except:
            try:
                out = base64_b64decode((b64dat + '=='), altchars='-_')
            except:
                raise ManagedException('Problem b64 decoding string: %s' % b64dat)

    return out


def get_binary_from_string(str):
    try:
        bin = binascii_a2b_hex(str)
    except:
        try:
            bin = opb64d(str)
        except:
            try:
                bin = base64_b64decode(str)
            except:
                raise ManagedException('Unable to decode the input. Enter in hex or base64_')

    return bin


def determine_session_file_path_from_session_key(session_key):
    decoded = urlsafe_b64decode(session_key + '==')
    sha1 = hashes.Hash((hashes.SHA1()), backend=(default_backend()))
    sha1.update(decoded)
    digest = sha1.finalize()
    return '.' + urlsafe_b64encode(digest).decode('utf-8')[:-1]
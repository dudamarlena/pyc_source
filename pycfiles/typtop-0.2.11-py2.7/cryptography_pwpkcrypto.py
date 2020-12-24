# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/typtop/cryptography_pwpkcrypto.py
# Compiled at: 2017-01-10 17:01:14
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
import os, random
from base64 import urlsafe_b64encode, urlsafe_b64decode
import struct
HASH_ALGOS = {'sha1': hashes.SHA1(), 
   'sha224': hashes.SHA224(), 
   'sha256': hashes.SHA256(), 
   'sha384': hashes.SHA384(), 
   'sha512': hashes.SHA512()}
HASH_CNT = 1000
SALT_LENGTH = 16
HASH_ALGO = 'sha256'
IV_LENGTH = 12
TAG_LENGTH = 16

def hash256(*args):
    """short function for Hashing the arguments with SHA-256"""
    assert len(args) > 0, 'Should give at least 1 message'
    assert all(isinstance(m, (bytes, basestring)) for m in args), 'All inputs should be byte string'
    h = hashes.Hash(hashes.SHA256(), backend=default_backend())
    h.update(bytes(len(args)) + bytes(args[0]) + bytes(len(args[0])))
    for m in args[1:]:
        h.update(bytes(m))
        h.update(bytes(len(m)))

    h.update(bytes(len(args)))
    return h.finalize()


def hmac256(secret, m):
    h = hmac.HMAC(bytes(secret), hashes.SHA256(), backend=default_backend())
    h.update(bytes(m))
    return h.finalize()


def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return (public_key, private_key)


def _slow_hash(pw, sa):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=16, salt=sa, iterations=HASH_CNT, backend=default_backend())
    key = kdf.derive(pw)
    return key


def verify_pk_sk(pk, sk):
    try:
        if isinstance(sk, (bytes, basestring)):
            sk = deserialize_sk(sk)
        if not isinstance(pk, (bytes, basestring)):
            pk = serialize_pk(pk)
        pkprime = serialize_pk(sk.public_key())
        return pkprime == pk
    except Exception as e:
        print ('ERRROR: {}').format(e)
        print ('sk: {}\npk:{}').format(sk, pk)
        raise e


def verify(pw, sa, h):
    """Verifies if h(pw, sa) == h
    returns k in case it matches, otherwise None.
    """
    sa = urlsafe_b64decode(bytes(sa))
    k = _slow_hash(pw, sa)
    hprime = hash256(k)
    if h == urlsafe_b64encode(hprime):
        return k
    else:
        return
        return


def harden_pw(pw):
    sa = os.urandom(SALT_LENGTH)
    k = _slow_hash(pw, sa)
    h = hash256(k)
    return (urlsafe_b64encode(sa), k, urlsafe_b64encode(h))


def serialize_pk(pk):
    if isinstance(pk, (basestring, bytes)):
        return pk
    if isinstance(pk, ec.EllipticCurvePrivateKey):
        pk = pk.public_key()
    return pk.public_bytes(serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


def serialize_sk(sk):
    if isinstance(sk, (basestring, bytes)):
        return sk
    else:
        return sk.private_bytes(serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())


def deserialize_sk(sk_s):
    if isinstance(sk_s, (bytes, basestring, unicode)):
        return serialization.load_pem_private_key(bytes(sk_s), password=None, backend=default_backend())
    else:
        return sk_s
        return


def deserialize_pk(pk_s):
    if isinstance(pk_s, (bytes, basestring, unicode)):
        return serialization.load_pem_public_key(bytes(pk_s), backend=default_backend())
    else:
        return pk_s


def pad_pw(pw, pad_length):
    """Pad pw to a pad_length, so that it hides the length of the password in bytes."""
    assert 0 < pad_length < 256
    pw = bytes(pw)
    k = len(pw) / pad_length
    topad = pw[k * pad_length:]
    topad_len = pad_length - len(topad)
    if topad_len == 0:
        topad_len = pad_length
    pad = chr(topad_len) * topad_len
    return pw + pad


def unpad_pw(padded_pw, pad_length):
    """Unpad pw"""
    padded_pw = bytes(padded_pw)
    padlen = ord(padded_pw[(-1)])
    assert padlen > 0, 'Malformed padding. Last byte cannot be zero.'
    pad = padded_pw[-padlen:]
    assert all(padi == chr(padlen) for padi in pad)
    return padded_pw[:-padlen]


def pwencrypt(pw, m):
    """Encrypt the message m under pw using AES-GCM method (AEAD scheme).
    iv = 0   # Promise me you will never reuse the key
    c = <hash_style>.<iteration>.<urlsafe-base64 <salt><iv><tag><ctx>>
    :hash_style: sha-256 or sha-512, scrypt
    :iteration: Number of iteration. These two are the parameters
    for PBKDF2HMAC.
    Size of the ciphertext:
    """
    m = m.encode('ascii', errors='ignore')
    hash_func = HASH_ALGOS[HASH_ALGO]
    itercnt = random.randint(HASH_CNT, 2 * HASH_CNT)
    header_txt = HASH_ALGO + '.' + str(itercnt)
    sa = os.urandom(SALT_LENGTH)
    kdf = PBKDF2HMAC(algorithm=hash_func, length=16, salt=sa, iterations=itercnt, backend=default_backend())
    key = kdf.derive(pw)
    iv, ctx, tag = _encrypt(key, m, associated_data=header_txt)
    ctx_b64 = urlsafe_b64encode(sa + iv + tag + ctx)
    return header_txt + '.' + ctx_b64


def pwdecrypt(pw, full_ctx_b64):
    """
    Decrypt a ciphertext using pw,
    Recover, hash algo, iteration count, and salt, iv, tag, ctx from ctx_b64
    """
    full_ctx_b64 = full_ctx_b64.encode('ascii', errors='ignore')
    hash_algo, itercnt, ctx_b64 = full_ctx_b64.split('.')
    header_txt = hash_algo + '.' + itercnt
    ctx_bin = urlsafe_b64decode(ctx_b64)
    sa, ctx_bin = ctx_bin[:SALT_LENGTH], ctx_bin[SALT_LENGTH:]
    iv, ctx_bin = ctx_bin[:IV_LENGTH], ctx_bin[IV_LENGTH:]
    tag, ctx = ctx_bin[:TAG_LENGTH], ctx_bin[TAG_LENGTH:]
    kdf = PBKDF2HMAC(algorithm=HASH_ALGOS[hash_algo], length=16, salt=sa, iterations=int(itercnt), backend=default_backend())
    key = kdf.derive(pw)
    try:
        m = _decrypt(key, iv, ctx, tag, associated_data=header_txt)
        return m
    except Exception as e:
        raise ValueError(e)


def _encrypt(key, plaintext, associated_data=''):
    iv = os.urandom(IV_LENGTH)
    if len(key) not in algorithms.AES.key_sizes:
        key = hash256(key)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
    encryptor.authenticate_additional_data(associated_data)
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return (
     iv, ciphertext, encryptor.tag)


def _decrypt(key, iv, ciphertext, tag, associated_data=''):
    if len(key) not in algorithms.AES.key_sizes:
        key = hash256(key)
    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()).decryptor()
    decryptor.authenticate_additional_data(associated_data)
    return decryptor.update(ciphertext) + decryptor.finalize()


def encrypt(k, m):
    """Symmetric encrpyt.
    """
    if not isinstance(m, bytes):
        m = bytes(m)
    iv, ctx, tag = _encrypt(k, m)
    return urlsafe_b64encode(iv + ctx + tag)


def decrypt(k, ctx):
    """Symmetric decrpyt.
    """
    if not isinstance(ctx, bytes):
        ctx = bytes(ctx)
    ctx_bin = urlsafe_b64decode(bytes(ctx))
    iv, c, tag = ctx_bin[:12], ctx_bin[12:-16], ctx_bin[-16:]
    try:
        return _decrypt(k, iv, c, tag)
    except Exception as e:
        print e
        raise ValueError(e)


def pkencrypt(pk, m):
    """Public key encrypt"""
    if not isinstance(pk, ec.EllipticCurvePublicKey):
        pk = deserialize_pk(pk)
    rpk, rsk = generate_key_pair()
    common_key = rsk.exchange(ec.ECDH(), pk)
    c = encrypt(common_key, m)
    rpk_s = serialize_pk(rpk)
    return ('||').join((rpk_s, c))


def pkdecrypt(sk, ctx):
    """Public key decrypt"""
    if isinstance(sk, (bytes, basestring)):
        sk = deserialize_sk(sk)
    rpk_s, c = ctx.split('||')
    rpk = deserialize_pk(rpk_s)
    common_key = sk.exchange(ec.ECDH(), rpk)
    m = decrypt(common_key, c)
    return m


def compute_id(salt, pwtypo):
    """
    Computes an ID for pwtypo.
    @pwtypo (byte string): mistyped (or correct) password
    @salt (byte string): global salt
    """
    if len(salt) > SALT_LENGTH:
        salt = urlsafe_b64decode(bytes(salt))
    assert len(salt) == SALT_LENGTH, ('len(salt)={} ({})').format(len(salt), SALT_LENGTH)
    h = hmac256(salt, bytes(pwtypo))
    return struct.unpack('<I', h[:4])[0]


def encrpyt_sk(key, sk):
    if not isinstance(sk, (bytes, basestring)):
        sk = serialize_sk(sk)
    return encrypt(key, sk)
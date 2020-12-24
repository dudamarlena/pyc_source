# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bip32/utils.py
# Compiled at: 2020-03-18 12:48:53
# Size of source mod 2**32: 6506 bytes
import coincurve, hashlib, hmac
HARDENED_INDEX = 2147483648
ENCODING_PREFIX = {'main':{'private':76066276, 
  'public':76067358}, 
 'test':{'private':70615956, 
  'public':70617039}}

class BIP32DerivationError(Exception):
    __doc__ = 'We derived an invalid (secret > N or point(secret) is infinity) key!'


def _privkey_to_pubkey(privkey):
    """Takes a 32 bytes privkey and returns a 33 bytes secp256k1 pubkey"""
    return coincurve.PublicKey.from_secret(privkey).format()


def _derive_unhardened_private_child(privkey, chaincode, index):
    """A.k.a CKDpriv, in bip-0032

    :param privkey: The parent's private key, as bytes
    :param chaincode: The parent's chaincode, as bytes
    :param index: The index of the node to derive, as int

    :return: (child_privatekey, child_chaincode)
    """
    if isinstance(privkey, bytes):
        if not isinstance(chaincode, bytes):
            raise AssertionError
        if index & HARDENED_INDEX:
            raise AssertionError
    else:
        pubkey = _privkey_to_pubkey(privkey)
        payload = hmac.new(chaincode, pubkey + index.to_bytes(4, 'big'), hashlib.sha512).digest()
        try:
            child_private = coincurve.PrivateKey(payload[:32]).add(privkey)
        except ValueError:
            raise BIP32DerivationError('Invalid private key at index {}, try the next one!'.format(index))

    return (
     bytes.fromhex(child_private.to_hex()), payload[32:])


def _derive_hardened_private_child(privkey, chaincode, index):
    """A.k.a CKDpriv, in bip-0032, but the hardened way

    :param privkey: The parent's private key, as bytes
    :param chaincode: The parent's chaincode, as bytes
    :param index: The index of the node to derive, as int

    :return: (child_privatekey, child_chaincode)
    """
    if isinstance(privkey, bytes):
        if not isinstance(chaincode, bytes):
            raise AssertionError
        if not index & HARDENED_INDEX:
            raise AssertionError
    else:
        payload = hmac.new(chaincode, b'\x00' + privkey + index.to_bytes(4, 'big'), hashlib.sha512).digest()
        try:
            child_private = coincurve.PrivateKey(payload[:32]).add(privkey)
        except ValueError:
            raise BIP32DerivationError('Invalid private key at index {}, try the next one!'.format(index))

    return (
     bytes.fromhex(child_private.to_hex()), payload[32:])


def _derive_public_child(pubkey, chaincode, index):
    """A.k.a CKDpub, in bip-0032.

    :param pubkey: The parent's (compressed) public key, as bytes
    :param chaincode: The parent's chaincode, as bytes
    :param index: The index of the node to derive, as int

    :return: (child_pubkey, child_chaincode)
    """
    if isinstance(pubkey, bytes):
        if not isinstance(chaincode, bytes):
            raise AssertionError
        if index & HARDENED_INDEX:
            raise AssertionError
    else:
        payload = hmac.new(chaincode, pubkey + index.to_bytes(4, 'big'), hashlib.sha512).digest()
        try:
            tmp_pub = coincurve.PublicKey.from_secret(payload[:32])
        except ValueError:
            raise BIP32DerivationError('Invalid private key at index {}, try the next one!'.format(index))

    parent_pub = coincurve.PublicKey(pubkey)
    try:
        child_pub = coincurve.PublicKey.combine_keys([tmp_pub, parent_pub])
    except ValueError:
        raise BIP32DerivationError('Invalid public key at index {}, try the next one!'.format(index))

    return (
     child_pub.format(), payload[32:])


def _pubkey_to_fingerprint(pubkey):
    rip = hashlib.new('ripemd160')
    rip.update(hashlib.sha256(pubkey).digest())
    return rip.digest()[:4]


def _serialize_extended_key(key, depth, parent, index, chaincode, network='main'):
    """Serialize an extended private *OR* public key, as spec by bip-0032.

    :param key: The public or private key to serialize. Note that if this is
                a public key it MUST be compressed.
    :param depth: 0x00 for master nodes, 0x01 for level-1 derived keys, etc..
    :param parent: The parent pubkey used to derive the fingerprint, or the
                   fingerprint itself None if master.
    :param index: The index of the key being serialized. 0x00000000 if master.
    :param chaincode: The chain code (not the labs !!).

    :return: The serialized extended key.
    """
    for param in {key, chaincode}:
        assert isinstance(param, bytes)

    for param in {depth, index}:
        assert isinstance(param, int)

    if parent:
        assert isinstance(parent, bytes)
        if len(parent) == 33:
            fingerprint = _pubkey_to_fingerprint(parent)
        elif len(parent) == 4:
            fingerprint = parent
        else:
            raise ValueError('Bad parent, a fingerprint or a pubkey is required')
    else:
        fingerprint = bytes(4)
    assert len(key) in {32, 33}
    if network not in {'main', 'test'}:
        raise ValueError('Unsupported network')
    is_privkey = len(key) == 32
    prefix = ENCODING_PREFIX[network][('private' if is_privkey else 'public')]
    extended = prefix.to_bytes(4, 'big')
    extended += depth.to_bytes(1, 'big')
    extended += fingerprint
    extended += index.to_bytes(4, 'big')
    extended += chaincode
    if is_privkey:
        extended += b'\x00'
    extended += key
    return extended


def _unserialize_extended_key(extended_key):
    """Unserialize an extended private *OR* public key, as spec by bip-0032.

    :param extended_key: The extended key to unserialize __as bytes__

    :return: network (str), depth (int), fingerprint (bytes), index (int),
             chaincode (bytes), key (bytes)
    """
    if isinstance(extended_key, bytes):
        raise len(extended_key) == 78 or AssertionError
    else:
        prefix = int.from_bytes(extended_key[:4], 'big')
        if prefix in list(ENCODING_PREFIX['main'].values()):
            network = 'main'
        else:
            network = 'test'
    depth = extended_key[4]
    fingerprint = extended_key[5:9]
    index = int.from_bytes(extended_key[9:13], 'big')
    chaincode, key = extended_key[13:45], extended_key[45:]
    return (network, depth, fingerprint, index, chaincode, key)


def _hardened_index_in_path(path):
    return len([i for i in path if i & HARDENED_INDEX]) > 0
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arky\lisk\crypto.py
# Compiled at: 2017-11-26 16:11:53
from nacl.bindings.crypto_sign import crypto_sign_seed_keypair, crypto_sign
from nacl.bindings import crypto_sign_BYTES
from .. import __PY3__
from .. import __FROZEN__
from .. import cfg
from .. import slots
from ..util import basint
from ..util import unpack
from ..util import pack
from ..util import unpack_bytes
from ..util import pack_bytes
from ..util import hexlify
from ..util import unhexlify
if not __PY3__:
    from StringIO import StringIO
else:
    from io import BytesIO as StringIO
import hashlib, binascii, struct

def getKeys(secret, seed=None):
    seed = (seed or hashlib.sha256((isinstance(secret, bytes) or secret.encode)('utf8') if 1 else secret).digest)() if 1 else seed
    publicKey, privateKey = list(hexlify(e) for e in crypto_sign_seed_keypair(seed))
    return {'publicKey': publicKey, 'privateKey': privateKey}


def getAddress(public):
    seed = hashlib.sha256(unhexlify(public)).digest()
    return '%s%s' % (struct.unpack('<Q', seed[:8]) + (cfg.marker,))


def getSignature(tx, private):
    return hexlify(crypto_sign(hashlib.sha256(getBytes(tx)).digest(), unhexlify(private))[:crypto_sign_BYTES])


def getId(tx):
    seed = hashlib.sha256(getBytes(tx)).digest()
    return '%s' % struct.unpack('<Q', seed[:8])


def getBytes(tx):
    buf = StringIO()
    pack('<bi', buf, (tx['type'], int(tx['timestamp'])))
    pack_bytes(buf, unhexlify(tx['senderPublicKey']))
    if 'requesterPublicKey' in tx:
        pack_bytes(buf, unhexlify(tx['requesterPublicKey']))
    if 'recipientId' in tx:
        pack('>Q', buf, (int(tx['recipientId'][:-len(cfg.marker)]),))
    else:
        pack('<Q', buf, (0, ))
    pack('<Q', buf, (int(tx['amount']),))
    if tx.get('asset', False):
        asset = tx['asset']
        typ = tx['type']
        if typ == 1 and 'signature' in asset:
            pack_bytes(buf, unhexlify(asset['signature']['publicKey']))
        elif typ == 2 and 'delegate' in asset:
            pack_bytes(buf, asset['delegate']['username'].encode('utf-8'))
        elif typ == 3 and 'votes' in asset:
            pack_bytes(buf, ('').join(asset['votes']).encode('utf-8'))
    if tx.get('signature', False):
        pack_bytes(buf, unhexlify(tx['signature']))
    if tx.get('signSignature', False):
        pack_bytes(buf, unhexlify(tx['signSignature']))
    result = buf.getvalue()
    buf.close()
    if not isinstance(result, bytes):
        return result.encode()
    return result


def bakeTransaction(**kw):
    if 'publicKey' in kw and 'privateKey' in kw:
        publicKey, privateKey = kw['publicKey'], kw['privateKey']
    else:
        if 'secret' in kw:
            keys = getKeys(kw['secret'])
            publicKey = keys['publicKey']
            privateKey = keys['privateKey']
        else:
            raise Exception('Can not initialize transaction (no secret or keys given)')
        payload = {'timestamp': int(slots.getTime()), 
           'type': int(kw.get('type', 0)), 
           'amount': int(kw.get('amount', 0)), 
           'fee': cfg.fees.get({0: 'send', 
                   1: 'secondsignature', 
                   2: 'delegate', 
                   3: 'vote'}[kw.get('type', 0)])}
        payload['senderPublicKey'] = publicKey
        for key in (k for k in ['requesterPublicKey', 'recipientId', 'asset'] if k in kw):
            payload[key] = kw[key]

    payload['signature'] = getSignature(payload, privateKey)
    if kw.get('secondSecret', None):
        secondKeys = getKeys(kw['secondSecret'])
        payload['signSignature'] = getSignature(payload, secondKeys['privateKey'])
    elif kw.get('secondPrivateKey', None):
        payload['signSignature'] = getSignature(payload, kw['secondPrivateKey'])
    payload['id'] = getId(payload)
    return payload
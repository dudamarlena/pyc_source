# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/jws/__init__.py
# Compiled at: 2015-03-10 10:18:32
from __future__ import absolute_import
import json, jws.utils as utils, jws.algos as algos, jws.header as header
from jws.exceptions import *

def sign(head, payload, key=None, is_json=False):
    data = {'key': key, 
       'header': json.loads(head) if is_json else head, 
       'payload': json.loads(payload) if is_json else payload, 
       'signer': None}
    header.process(data, 'sign')
    if not data['key']:
        raise MissingKey('Key was not passed as a param and a key could not be found from the header')
    if not data['signer']:
        raise MissingSigner('Header was processed, but no algorithm was found to sign the message')
    signer = data['signer']
    signature = signer(_signing_input(head, payload, is_json), key)
    return utils.to_base64(signature)


def verify(head, payload, encoded_signature, key=None, is_json=False):
    data = {'key': key, 
       'header': json.loads(head) if is_json else head, 
       'payload': json.loads(payload) if is_json else payload, 
       'verifier': None}
    header.process(data, 'verify')
    if not data['key']:
        raise MissingKey('Key was not passed as a param and a key could not be found from the header')
    if not data['verifier']:
        raise MissingVerifier('Header was processed, but no algorithm was found to sign the message')
    verifier = data['verifier']
    signature = utils.from_base64(encoded_signature)
    return verifier(_signing_input(head, payload, is_json), signature, key)


def _signing_input(head, payload, is_json=False):
    enc = utils.to_base64 if is_json else utils.encode
    (head_input, payload_input) = map(enc, [head, payload])
    return '%s.%s' % (head_input, payload_input)
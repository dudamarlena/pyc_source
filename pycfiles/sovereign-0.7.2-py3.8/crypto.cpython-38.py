# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/views/crypto.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 1731 bytes
from pydantic import BaseModel, Field
from fastapi import APIRouter, Body
from sovereign import json_response_class
from sovereign.utils.crypto import encrypt, decrypt, generate_key
router = APIRouter()

class EncryptionRequest(BaseModel):
    data = Field(..., title='Text to be encrypted', min_length=1, max_length=65535)
    data: str
    key = Field(None, title='Optional Fernet encryption key to use to encrypt', min_length=44, max_length=44)
    key: str


class DecryptionRequest(BaseModel):
    data = Field(..., title='Text to be decrypted', min_length=1, max_length=65535)
    data: str
    key = Field(..., title='Fernet encryption key to use to decrypt', min_length=44, max_length=44)
    key: str


class DecryptableRequest(BaseModel):
    data = Field(..., title='Text to be decrypted', min_length=1, max_length=65535)
    data: str


@router.post('/decrypt', summary='Decrypt provided encrypted data using a provided key', response_class=json_response_class)
async def _decrypt(request: DecryptionRequest=Body(None)):
    return {'result': decrypt(request.data, request.key)}


@router.post('/encrypt', summary='Encrypt provided data using this servers key', response_class=json_response_class)
async def _encrypt(request: EncryptionRequest=Body(None)):
    return {'result': encrypt(data=(request.data), key=(request.key))}


@router.post('/decryptable', summary='Check whether data is decryptable by this server', response_class=json_response_class)
async def _decryptable(request: DecryptableRequest=Body(None)):
    decrypt(request.data)
    return json_response_class({})


@router.get('/generate_key', summary='Generate a new asymmetric encryption key', response_class=json_response_class)
def _generate_key():
    return {'result': generate_key()}
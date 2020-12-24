# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/generators.py
# Compiled at: 2013-02-09 19:59:16
import time, random, hashlib

def _get_hash():
    sha = hashlib.sha256()
    sha.update(str(random.random()))
    sha.update(str(time.time()))
    return sha


def gen_client_id():
    return _get_hash().hexdigest()


def gen_client_secret():
    return _get_hash().hexdigest()


def gen_token(client):
    sha = _get_hash()
    sha.update(client.client_id)
    return sha.hexdigest()
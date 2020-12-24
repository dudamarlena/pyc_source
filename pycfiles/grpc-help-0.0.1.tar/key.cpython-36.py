# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/key.py
# Compiled at: 2018-12-26 02:01:51
# Size of source mod 2**32: 288 bytes


def read_private_key(private_key_path):
    with open(private_key_path, 'rb') as (f):
        private_key = f.read()
    return private_key


def read_public_key(public_key_path):
    with open(public_key_path, 'rb') as (f):
        certificate_chain = f.read()
    return certificate_chain
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/util/random_object_id.py
# Compiled at: 2020-04-15 22:33:43
# Size of source mod 2**32: 685 bytes
import binascii, os, time
from bson.objectid import ObjectId

class RandomObjectId(object):

    def __init__(self):
        pass

    def gen_random_object_id_string(self):
        timestamp = '{0:x}'.format(int(time.time()))
        rest = binascii.b2a_hex(os.urandom(8)).decode('ascii')
        object_id = timestamp + rest
        return object_id

    def gen_random_object_id(self):
        timestamp = '{0:x}'.format(int(time.time()))
        rest = binascii.b2a_hex(os.urandom(8)).decode('ascii')
        object_id = timestamp + rest
        return ObjectId(object_id)
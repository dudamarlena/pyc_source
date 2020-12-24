# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/__init__.py
# Compiled at: 2018-06-15 00:23:08
# Size of source mod 2**32: 138 bytes
from motor import pymongo
from tailow.connection import Connection

def connect(*args, **kwargs):
    (Connection.connect)(*args, **kwargs)
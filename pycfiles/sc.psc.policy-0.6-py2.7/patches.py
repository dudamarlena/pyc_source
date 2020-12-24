# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sc/psc/policy/patches.py
# Compiled at: 2012-07-17 18:10:20
from collective.psc.blobstorage import BlobWrapper

def __init__(self, content_type='PSCFile'):
    """ Set a default content_type for BlobWrapper """
    super(BlobWrapper, self).__init__(content_type)


def run():
    setattr(BlobWrapper, '__init__', __init__)
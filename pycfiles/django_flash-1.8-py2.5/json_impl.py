# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/djangoflash/codec/json_impl.py
# Compiled at: 2011-01-28 16:01:34
"""This module provides a JSON-based codec implementation.
"""
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from djangoflash.codec import BaseCodec
from djangoflash.models import FlashScope

class CodecClass(BaseCodec):
    """JSON-based codec implementation.
    """

    def __init__(self):
        """Returns a new JSON-based codec.
        """
        BaseCodec.__init__(self)

    def encode(self, flash):
        """Encodes the given *flash* as a JSON string.
        """
        return json.dumps(flash.to_dict())

    def decode(self, encoded_flash):
        """Restores the *flash* from the given JSON string.
        """
        return FlashScope(json.loads(encoded_flash))
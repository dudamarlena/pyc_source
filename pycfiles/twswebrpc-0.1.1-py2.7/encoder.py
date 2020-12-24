# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twswebrpc/encoder.py
# Compiled at: 2014-06-08 12:14:52
import json
from zope.interface import Interface
from zope.interface import implementer
from twisted.spread.jelly import jelly, unjelly, SecurityOptions
from twisted.spread.banana import encode as bananaEncode
from twisted.spread.banana import decode as bananaDecode

class IEncoder(Interface):

    def encode(self, data):
        """

        :param data: python data to encode
        :return: encoded string data
        """
        pass

    def decode(self, data):
        """

        :param data: string data
        :return: python data
        """
        pass


@implementer(IEncoder)
class JSONEncoder(object):

    def encode(self, data):
        return json.dumps(data)

    def decode(self, data):
        return json.loads(data)


@implementer(IEncoder)
class JellyEncoder(object):

    def encode(self, data):
        security = SecurityOptions()
        security.allowBasicTypes()
        jellyMessage = jelly(data, taster=security)
        return bananaEncode(jellyMessage)

    def decode(self, data):
        security = SecurityOptions()
        security.allowBasicTypes()
        bananaMessage = bananaDecode(data)
        return unjelly(bananaMessage, taster=security)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/neokami1/Dropbox/Neokami/Code/Bitbucket/neokami-python-sdk/neokami/src/Neokami/Base.py
# Compiled at: 2015-09-15 08:16:27
""" Copyright 2015 Neokami GmbH. """
from dicttoxml import dicttoxml

class Base:
    API_BASE = 'https://api.neokami.io'
    SDK_VERSION = '0.2'
    SDK_LANG = 'python'

    def getUrl(self, path):
        return self.API_BASE + path

    def toXML(self, array):
        return dicttoxml(array, attr_type=False)
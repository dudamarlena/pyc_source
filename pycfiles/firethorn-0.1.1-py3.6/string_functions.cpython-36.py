# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/utils/string_functions.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 368 bytes
"""
Created on Nov 7, 2012

@author: stelios
"""
from urllib.parse import quote_plus, unquote, unquote_plus
from io import StringIO

class string_functions:

    def encode(self, _string):
        return quote_plus(_string.encode('utf8'))

    def decode(self, _string):
        return unquote_plus(str(_string.encode('utf8').decode('utf8')))
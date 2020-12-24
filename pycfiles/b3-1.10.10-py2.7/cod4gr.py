# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\cod4gr.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'Fenix'
__version__ = '1.0'
import b3.clients, b3.functions, b3.parsers.cod4, re

class Cod4grParser(b3.parsers.cod4.Cod4Parser):
    _guidLength = 10
    _regPlayer = re.compile('^\\s*(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+GameRanger-Account-ID_(?P<guid>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+?)\\s*(?P<ip>(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])):?(?P<port>-?[0-9]{1,5})\\s*(?P<qport>-?[0-9]{1,5})\\s+(?P<rate>[0-9]+)$', re.IGNORECASE | re.VERBOSE)

    def __new__(cls, *args, **kwargs):
        b3.parsers.cod4.patch_b3_clients()
        return b3.parsers.cod4.Cod4Parser.__new__(cls)
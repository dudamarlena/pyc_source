# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/erlport/__init__.py
# Compiled at: 2010-02-24 12:36:22
"""Erlang port protocol."""
__author__ = 'Dmitry Vasiliev <dima@hlabs.spb.ru>'
__version__ = '0.4'
from erlport.erlproto import Port, Protocol
from erlport.erlterms import IncompleteData, decode, encode
from erlport.erlterms import Atom, String, BitBinary
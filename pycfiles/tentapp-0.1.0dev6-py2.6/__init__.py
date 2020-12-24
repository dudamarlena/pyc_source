# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/tentapp/__init__.py
# Compiled at: 2012-10-17 02:22:53
import sys
try:
    import requests
except ImportError:
    print >> sys.stderr, 'The tentapp library requires that you have the "requests" library installed.  Run "pip install requests".'

__version__ = '0.1.0dev6'
from tentapp import TentApp, KeyStore, DiscoveryFailure, RegistrationFailure, AuthRequestFailure, ConnectionFailure
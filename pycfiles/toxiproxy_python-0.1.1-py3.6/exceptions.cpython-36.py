# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/toxiproxy/exceptions.py
# Compiled at: 2018-08-22 09:02:13
# Size of source mod 2**32: 238 bytes
ProxyExists = type('ProxyExists', (Exception,), {})
NotFound = type('NotFound', (Exception,), {})
InvalidToxic = type('InvalidToxic', (Exception,), {})
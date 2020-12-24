# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/typtop/pw_pkcrypto.py
# Compiled at: 2016-12-15 18:38:58
try:
    import cryptography
    from typtop.cryptography_pwpkcrypto import *
except ImportError as e:
    from typtop.pycryptodome_pwpkcrypto import *
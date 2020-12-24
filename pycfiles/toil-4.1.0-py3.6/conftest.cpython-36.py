# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/encryption/conftest.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 159 bytes
collect_ignore = []
try:
    import nacl
except ImportError:
    collect_ignore.append('_nacl.py')
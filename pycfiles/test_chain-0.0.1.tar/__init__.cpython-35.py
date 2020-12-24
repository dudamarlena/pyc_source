# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\github\testchain\test_chain\__init__.py
# Compiled at: 2017-01-04 10:26:36
# Size of source mod 2**32: 174 bytes
from .test_chain_meta import *
if sys.version_info[0] == 2:
    from .test_chain2 import TestChain
elif sys.version_info[0] == 3:
    from .test_chain3 import TestChain
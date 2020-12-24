# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sean/sandbox/stoicheia/stoicheia/__tests.py
# Compiled at: 2020-02-17 17:39:47
# Size of source mod 2**32: 82 bytes
from .stoicheia import Catalog

def test_catalog_in_memory():
    cat = Catalog()
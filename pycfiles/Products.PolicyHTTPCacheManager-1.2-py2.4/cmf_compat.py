# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/PolicyHTTPCacheManager/cmf_compat.py
# Compiled at: 2008-04-16 06:12:03
from Acquisition import Implicit

class _ViewEmulator(Implicit):
    """Auxiliary class used to adapt FSFile and FSImage
    for caching_policy_manager
    """
    __module__ = __name__

    def __init__(self, view_name=''):
        self._view_name = view_name

    def getId(self):
        return self._view_name
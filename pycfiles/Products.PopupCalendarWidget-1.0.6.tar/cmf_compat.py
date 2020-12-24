# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
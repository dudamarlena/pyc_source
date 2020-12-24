# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsacls.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource

class NSAcls(NSBaseResource):

    def __init__(self):
        super(NSAcls, self).__init__()
        self.options = {}
        self.resourcetype = NSAcls.get_resourcetype()

    @staticmethod
    def get_resourcetype():
        return 'nsacls'

    @staticmethod
    def renumber(nitro):
        """
        Use this API to renumber nsacls.
        """
        __nsacls = NSAcls()
        return __nsacls.perform_operation(nitro, 'renumber')

    @staticmethod
    def clear(nitro):
        """
        Use this API to clear nsacls.
        """
        __nsacls = NSAcls()
        return __nsacls.perform_operation(nitro, 'clear')

    @staticmethod
    def apply(nitro):
        """
        Use this API to apply nsacls.
        """
        __nsacls = NSAcls()
        return __nsacls.perform_operation(nitro, 'apply')
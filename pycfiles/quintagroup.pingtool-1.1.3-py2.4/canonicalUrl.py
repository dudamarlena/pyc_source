# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/canonicalUrl.py
# Compiled at: 2009-03-31 04:47:33
from Products.CMFCore.utils import getToolByName

class CanonicalURL(object):
    """ CanonicalURL adapter
    """
    __module__ = __name__

    def __init__(self, context):
        """ init
        """
        self.context = context

    def getCanonicalURL(self):
        """Get canonical_url property value
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return portal.getProperty('canonical_url', None)
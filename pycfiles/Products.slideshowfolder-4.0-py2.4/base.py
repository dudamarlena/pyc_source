# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/tests/base.py
# Compiled at: 2008-06-02 02:45:55
"""
Base class for integration tests, based on ZopeTestCase and PloneTestCase.
   
Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""
from Testing import ZopeTestCase
ZopeTestCase.installProduct('CMFonFive')
ZopeTestCase.installProduct('slideshowfolder')
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
setupPloneSite(products=['slideshowfolder'])

class SlideshowFolderTestCase(PloneTestCase):
    """Base class for integration tests for the 'slideshowfolder' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """
    __module__ = __name__

    def afterSetUp(self):
        pass
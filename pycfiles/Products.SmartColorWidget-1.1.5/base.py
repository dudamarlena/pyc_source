# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/tests/base.py
# Compiled at: 2008-06-02 02:45:55
__doc__ = '\nBase class for integration tests, based on ZopeTestCase and PloneTestCase.\n   \nNote that importing this module has various side-effects: it registers a set of\nproducts with Zope, and it sets up a sandbox Plone site with the appropriate\nproducts installed.\n'
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
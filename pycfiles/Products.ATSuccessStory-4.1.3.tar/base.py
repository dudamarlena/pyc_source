# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/tests/base.py
# Compiled at: 2015-12-17 03:21:31
"""Base testing infrastructure
"""
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from zope.schema.vocabulary import getVocabularyRegistry
from Products.ATSuccessStory.vocabularies import existingSSFolders
ztc.installProduct('ATSuccessStory')

@onsetup
def setup_atsuccessstory():
    """Set up the additional products required for the atsuccessstory product.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer.
    """
    try:
        vr = getVocabularyRegistry()
        vr.register('atss.existing_folders', existingSSFolders)
    except:
        pass


setup_atsuccessstory()
ptc.setupPloneSite(products=['ATSuccessStory'])

class ATSuccessStoryTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here.
    """
    pass


class ATSuccessStoryFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here.
    """
    pass
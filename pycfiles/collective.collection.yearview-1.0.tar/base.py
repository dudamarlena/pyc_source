# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/collection/alphabetic/tests/base.py
# Compiled at: 2009-06-10 12:35:24
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_collective_collection_alphabetic():
    fiveconfigure.debug_mode = True
    import collective.collection.alphabetic
    zcml.load_config('configure.zcml', collective.collection.alphabetic)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.collection.alphabetic')


setup_collective_collection_alphabetic()
ptc.setupPloneSite(products=['collective.collection.alphabetic'])

class CollectionAlphabeticTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__

    def afterSetUp(self):
        """Code that is needed is the afterSetUp of both test cases.
        """
        ztc.utils.setupCoreSessions(self.app)


class CollectionAlphabeticFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__
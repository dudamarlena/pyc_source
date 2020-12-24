# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
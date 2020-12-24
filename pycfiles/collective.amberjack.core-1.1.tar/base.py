# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/allowtypes/tests/base.py
# Compiled at: 2008-11-10 16:17:20
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
import collective.allowtypes

@onsetup
def setup_collective_allowtypes():
    """Set up the additional products
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', collective.allowtypes)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.allowtypes')


setup_collective_allowtypes()
ptc.setupPloneSite(products=['collective.allowtypes'])

class PackageTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__


class PackageFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__
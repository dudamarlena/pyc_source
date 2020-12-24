# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/plonetheme/terrafirma/tests/base.py
# Compiled at: 2008-04-13 21:05:46
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_theme_tests():
    """
    """
    fiveconfigure.debug_mode = True
    import plonetheme.terrafirma
    zcml.load_config('configure.zcml', plonetheme.terrafirma)
    fiveconfigure.debug_mode = False
    ztc.installPackage('plonetheme.terrafirma')


setup_theme_tests()
ptc.setupPloneSite(products=['plonetheme.terrafirma'])

class TerrafirmaTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__


class TerrafirmaFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__
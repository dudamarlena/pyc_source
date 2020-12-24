# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/tests/base.py
# Compiled at: 2008-04-14 11:51:37
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 57037 $'
__version__ = '$Revision: 57037 $'[11:-2]
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_contentmirror():
    """Set up the additional products
    """
    fiveconfigure.debug_mode = True
    import inquant.contentmirror.base
    zcml.load_config('configure.zcml', inquant.contentmirror.base)
    fiveconfigure.debug_mode = False
    ztc.installPackage('inquant.contentmirror.base')


setup_contentmirror()
ptc.setupPloneSite(products=['inquant.contentmirror.base'])

class CMTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__

    def create(self, context, what, name):
        context.invokeFactory(what, name, title=name)
        object = context.get(name)
        object.processForm()
        return object


class CMFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/jyu/portalview/tests/base.py
# Compiled at: 2009-11-16 03:44:25
"""Test setup for integration and functional tests.
 
When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """
    fiveconfigure.debug_mode = True
    import jyu.portalview
    zcml.load_config('configure.zcml', jyu.portalview)
    fiveconfigure.debug_mode = False
    ztc.installPackage('jyu.portalview')


setup_product()
ptc.setupPloneSite(products=['jyu.portalview'])
from Products.CMFCore.utils import getToolByName

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """
    __module__ = __name__


class ContentTypeTestCase(TestCase):
    """Defines custom methods for testing content type configuration.
    """
    __module__ = __name__
    name = None
    schema = None

    def afterSetUp(self):
        self.types = getToolByName(self.portal, 'portal_types')
        self.factory = getToolByName(self.portal, 'portal_factory')
        self.fieldnames = [ field.getName() for field in self.schema.fields() ]

    def assertProperty(self, name, value):
        self.assertEquals(value, self.types.get(self.name).getProperty(name))

    def assertMethodAlias(self, name, value):
        self.assertEquals(value, self.types.get(self.name).getMethodAliases()[name])

    def assertAction(self, action_id, params):
        actions = [ action for action in self.types.get(self.name).listActions() if action.id == action_id ]
        self.assertEquals(1, len(actions), "Content type doesn't have action ``%(action_id)s``." % vars())
        action = actions[0]
        for key in params:
            {'title': lambda x, y: x.assertEquals(y, action.title), 'category': lambda x, y: x.assertEquals(y, action.category), 
               'condition_expr': lambda x, y: x.assertEquals(y, action.condition and action.condition.text or ''), 
               'url_expr': lambda x, y: x.assertEquals(y, action.action and action.action.text) or '', 
               'visible': lambda x, y: x.assertEquals(y, action.visible), 
               'permission': lambda x, y: x.assertEquals(y, action.getPermissions())}[key](self, params[key])


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    __module__ = __name__

    def afterSetUp(self):
        self.portal.error_log._ignored_exceptions = ()
        self.portal.portal_membership.addMember('contributor', 'secret', ('Member',
                                                                          'Contributor'), [])
        self.portal.portal_membership.addMember('reviewer', 'secret', ('Member', 'Contributor',
                                                                       'Editor',
                                                                       'Reviewer'), [])
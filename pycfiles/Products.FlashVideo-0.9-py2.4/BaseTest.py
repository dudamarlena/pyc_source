# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\tests\BaseTest.py
# Compiled at: 2009-03-02 16:14:25
"""
Unit tests for FlashVideo
"""
import unittest, sys, os
from StringIO import StringIO
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.setup import default_user
from Products.PloneTestCase.setup import default_password
from Products.PloneTestCase.setup import portal_owner
from Products.CMFCore.utils import getToolByName
from Products.FlashVideo.content.FlashVideo import FlashVideo
from Products.FlashVideo.utils import IS_PLONE_21
from Products.FlashVideo.utils import IS_PLONE_30
from Products.FlashVideo.utils import IS_PLONE_31
import warnings
warnings.simplefilter('ignore')
products = []
try:
    from Products.FileSystemStorage import config
    ZopeTestCase.installProduct('FileSystemStorage')
    products.append('FileSystemStorage')
except ImportError:
    pass

products.append('FlashVideo')
ZopeTestCase.installProduct('FlashVideo')
PloneTestCase.setupPloneSite(products=products)

class FakeFile(StringIO):
    __module__ = __name__
    filename = 'fake_file'


class PloneUnitTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__
    portal_type = ''
    object_id = ''

    def getMovieFile(self):
        """
        Get test flash video file
        """
        ihome = os.environ.get('INSTANCE_HOME')
        path = os.path.join(ihome, 'Products', 'FlashVideo', 'tests', 'test_movie.flv')
        data = file(path, 'r').read()
        fakefile = FakeFile()
        fakefile.write(data)
        return fakefile

    def getImageFile(self):
        """
        Get teswt image file
        """
        ihome = os.environ.get('INSTANCE_HOME')
        path = os.path.join(ihome, 'Products', 'FlashVideo', 'tests', 'test_movie.jpg')
        f = file(path, 'rb')
        data = f.read()
        fakefile = FakeFile()
        fakefile.write(data)
        f.close()
        return fakefile

    def createInstance(self):
        """
        Create object instance of defined portal_type
        """
        self.folder.invokeFactory(self.portal_type, id=self.object_id)
        obj = self.folder._getOb(self.object_id)
        return obj


class PloneIntegrationTestCase(PloneTestCase.PloneTestCase):
    """
    Functional tests checking that all configuration works
    """
    __module__ = __name__
    portal_type = ''
    object_id = ''
    type_properties = (('', ''), )
    skin_files = ()
    object_actions = ['view', 'edit', 'metadata', 'local_roles']
    type_actions = ['view', 'edit', 'metadata', 'local_roles']

    def afterSetUp(self):
        """
        Run before tests
        """
        if IS_PLONE_21:
            if 'references' not in self.type_actions:
                self.type_actions.append('references')
        if IS_PLONE_30 or IS_PLONE_31:
            if 'local_roles' in self.type_actions:
                self.type_actions.remove('local_roles')

    def test_object_actions(self):
        """
        Test if object have all required tabs
        """
        id = self.folder.invokeFactory(self.portal_type, id=self.object_id)
        obj = self.folder._getOb(id)
        portal_actions = getToolByName(self.folder, 'portal_actions')
        actions = portal_actions.listFilteredActionsFor(obj)
        object_actions = actions['object']
        object_actions_ids = [ x['id'] for x in object_actions ]
        self.assertEqual(len(object_actions_ids), len(self.object_actions), '%s object should have %d actions, has %d' % (self.portal_type, len(self.object_actions), len(object_actions_ids)))
        for action in self.object_actions:
            self.failUnless(action in object_actions_ids, "%s object should have '%s' action" % (self.portal_type, action))

    def test_portal_types(self):
        """
        Test type in portal_types
        """
        portal_types = getToolByName(self.folder, 'portal_types')
        self.failUnless(self.portal_type in portal_types.objectIds(), '%s not found in portal_types' % self.portal_type)
        type = portal_types.getTypeInfo(self.portal_type)
        self.failUnless(type, '%s not found in portal_types' % self.portal_type)

    def test_portal_type_properties(self):
        """
        'Flash Video' portal type properties
        """
        portal_types = getToolByName(self.folder, 'portal_types')
        type = portal_types.getTypeInfo(self.portal_type)
        for p in self.type_properties:
            p_val = getattr(type, p[0], None)
            self.assertEqual(p_val, p[1], "'%s' type property '%s' set to '%s' instead of '%s'" % (self.portal_type, p[0], p_val, p[1]))

        return

    def test_portal_type_actions(self):
        """
        Portal type actions
        """
        portal_types = getToolByName(self.folder, 'portal_types')
        type = portal_types.getTypeInfo(self.portal_type)
        type_actions = type.listActions()
        actions_ids = [ x.getId() for x in type_actions if x.getVisibility() ]
        self.assertEqual(len(actions_ids), len(self.type_actions), '%s type should have %d actions, has %d' % (self.portal_type, len(self.type_actions), len(actions_ids)))
        for action in self.type_actions:
            self.failUnless(action in actions_ids, "%s type should have '%s' action" % (self.portal_type, action))

    def test_portal_skins(self):
        """
        Test if files exist in portal_skins
        """
        skin_name = 'FlashVideo'
        portal_skins = getToolByName(self.folder, 'portal_skins')
        self.failUnless(skin_name in portal_skins.objectIds())
        skin = getattr(portal_skins, skin_name)
        files = skin.objectIds()
        for f in self.skin_files:
            self.failUnless(f in files, "%s object should have '%s' in skins" % (self.portal_type, f))


class PloneFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """
    Functional tests for view and edit templates
    """
    __module__ = __name__
    portal_type = ''
    object_id = ''

    def getMovieFile(self):
        """
        Get test flash video file
        """
        ihome = os.environ.get('INSTANCE_HOME')
        path = os.path.join(ihome, 'Products', 'FlashVideo', 'tests', 'test_movie.flv')
        data = file(path, 'r').read()
        fakefile = FakeFile()
        fakefile.write(data)
        return fakefile

    def afterSetUp(self):
        """
        Run before tests
        """
        self.folder_url = self.folder.absolute_url()
        self.folder_path = '/%s' % self.folder.absolute_url(1)
        self.basic_auth = '%s:%s' % (default_user, default_password)
        self.owner_auth = '%s:%s' % (portal_owner, default_password)

    def test_createObject(self):
        """
        Create an object using the createObject script
        """
        response = self.publish(self.folder_path + '/createObject?type_name=%s' % self.portal_type, self.basic_auth)
        self.assertEqual(response.getStatus(), 302)
        url = response.getBody().split('?')[0]
        self.failUnless(url.startswith(self.folder_url))
        self.failUnless(url.endswith('edit'))
        edit_form_path = url[len(self.app.REQUEST.SERVER_URL):]
        response = self.publish(edit_form_path, self.basic_auth)
        self.assertEqual(response.getStatus(), 200)
        temp_id = url.split('/')[(-2)]
        new_obj = getattr(self.folder.portal_factory, temp_id)
        self.failUnlessEqual(new_obj.checkCreationFlag(), True)

    def test_edit_view(self):
        """
        Edit tab template
        """
        self.folder.invokeFactory(self.portal_type, self.object_id)
        obj = getattr(self.folder, self.object_id)
        path = '/%s/atct_edit' % obj.absolute_url(1)
        response = self.publish(path, self.basic_auth)
        self.assertEqual(response.getStatus(), 200)

    def test_metadata_edit_view(self):
        """
        Metadata tab template
        """
        self.folder.invokeFactory(self.portal_type, self.object_id)
        obj = getattr(self.folder, self.object_id)
        path = '/%s/base_metadata' % obj.absolute_url(1)
        response = self.publish(path, self.basic_auth)
        self.assertEqual(response.getStatus(), 200)

    def test_base_view(self):
        """
        Base view tab template
        """
        self.folder.invokeFactory(self.portal_type, self.object_id)
        obj = getattr(self.folder, self.object_id)
        path = '/%s/base_view' % obj.absolute_url(1)
        response = self.publish(path, self.basic_auth)
        self.assertEqual(response.getStatus(), 200)

    def test_view(self):
        """
        Dynamic 'view' template
        """
        self.folder.invokeFactory(self.portal_type, self.object_id)
        obj = getattr(self.folder, self.object_id)
        path = '/%s/view' % obj.absolute_url(1)
        response = self.publish(path, self.basic_auth)
        self.assertEqual(response.getStatus(), 200)

    def test_folder_localrole_form(self):
        """
        Sharing tab template
        """
        self.folder.invokeFactory(self.portal_type, self.object_id)
        obj = getattr(self.folder, self.object_id)
        path = '/%s/folder_localrole_form' % obj.absolute_url(1)
        response = self.publish(path, self.basic_auth)
        self.failUnless(response.getStatus() in (200, 302))
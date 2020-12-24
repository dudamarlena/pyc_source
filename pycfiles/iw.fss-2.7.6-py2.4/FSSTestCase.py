# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/tests/FSSTestCase.py
# Compiled at: 2008-10-23 05:55:15
"""
Base test case
$Id: FSSTestCase.py 69081 2008-07-28 13:39:24Z b_mathieu $
"""
import os, Globals, transaction
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase
portal_name = 'portal'
portal_owner = 'portal_owner'
default_user = PloneTestCase.default_user
default_password = PloneTestCase.default_password
STORAGE_PATH = os.path.join(Globals.INSTANCE_HOME, 'var', 'unittests_storage')
BACKUP_PATH = os.path.join(Globals.INSTANCE_HOME, 'var', 'unittests_backup')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
CONTENT_PATH = os.path.join(DATA_PATH, 'word.doc')
IMAGE_PATH = os.path.join(DATA_PATH, 'image.jpg')
CONTENT_TXT = 'mytestfile'
from Products.PloneTestCase.layer import onsetup
from Products.Five import fiveconfigure
from Products.Five import zcml
from Testing import ZopeTestCase as ztc

@onsetup
def setup_fss():
    fiveconfigure.debug_mode = True
    import iw.fss
    zcml.load_config('meta.zcml', iw.fss)
    zcml.load_config('configure.zcml', iw.fss)
    fiveconfigure.debug_mode = False
    ztc.installPackage('iw.fss')


setup_fss()

class FSSTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__

    class Session(dict):
        __module__ = __name__

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        from iw.fss.customconfig import INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE
        from iw.fss.interfaces import IConf
        os.environ[INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE] = 'True'
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
        for base_path in (STORAGE_PATH, BACKUP_PATH):
            if not os.path.exists(base_path):
                os.mkdir(base_path)

        conf = getUtility(IConf, 'globalconf')
        self.conf = conf()
        strategy_klass = self.strategy_klass

        def getStorageStrategy(self):
            return strategy_klass(STORAGE_PATH, BACKUP_PATH)

        from iw.fss.conffile import ConfFile
        ConfFile.getStorageStrategy = getStorageStrategy
        self.use_atct = False
        ttool = getToolByName(self.portal, 'portal_types')
        info = ttool.getTypeInfo('Folder')
        if info.getProperty('meta_type') == 'ATFolder':
            self.use_atct = True

    def beforeTearDown(self):
        """Remove all the stuff again.
        """
        import shutil
        shutil.rmtree(STORAGE_PATH)
        shutil.rmtree(BACKUP_PATH)

    def getDataPath(self):
        """Returns data path used for test cases"""
        return DATA_PATH

    def loginAsPortalOwner(self):
        """Use if you need to manipulate an article as member."""
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)
        return

    def addFileByString(self, folder, content_id):
        """Adds a file by string.
        """
        folder.invokeFactory('FSSItem', id=content_id)
        content = getattr(folder, content_id)
        transaction.savepoint(optimistic=True)
        kw = {'file': CONTENT_TXT}
        content.edit(**kw)
        return content

    def addFileByFileUpload(self, folder, content_id):
        """Adds a file by file upload.
        """
        folder.invokeFactory('FSSItem', id=content_id)
        content = getattr(folder, content_id)
        transaction.savepoint(optimistic=True)
        self.updateContent(content, 'file', CONTENT_PATH)
        return content

    def addImageByFileUpload(self, folder, content_id):
        """
        Adding image
        """
        folder.invokeFactory('FSSItem', id=content_id)
        content = getattr(folder, content_id)
        transaction.savepoint(optimistic=True)
        self.updateContent(content, 'image', IMAGE_PATH)
        return content

    def addATFileByString(self, folder, content_id):
        """Adds a file by string.
        """
        folder.invokeFactory('ATFSSItem', id=content_id)
        content = getattr(folder, content_id)
        transaction.savepoint(optimistic=True)
        kw = {'file': CONTENT_TXT}
        content.edit(**kw)
        return content

    def addATFileByFileUpload(self, folder, content_id):
        """Adds a file by file upload.
        """
        folder.invokeFactory('ATFSSItem', id=content_id)
        content = getattr(folder, content_id)
        transaction.savepoint(optimistic=True)
        self.updateContent(content, 'file', CONTENT_PATH)
        return content

    def addATImageByFileUpload(self, folder, content_id):
        """
        Adding image
        """
        folder.invokeFactory('ATFSSItem', id=content_id)
        content = getattr(folder, content_id)
        transaction.savepoint(optimistic=True)
        self.updateContent(content, 'image', IMAGE_PATH)
        return content

    def updateContent(self, content, field, filepath):
        """Updates a field content for a file.
        """
        from dummy import FileUpload
        file = open(filepath, 'rb')
        file.seek(0)
        filename = filepath.split('/')[(-1)]
        fu = FileUpload(filename=filename, file=file)
        kw = {field: fu}
        content.edit(**kw)


DEFAULT_PRODUCTS = [
 'kupu', 'iw.fss']
HAS_ATCT = True
ZopeTestCase.installProduct('ATContentTypes')
PloneTestCase.setupPloneSite(products=DEFAULT_PRODUCTS, extension_profiles=['iw.fss:testfixtures'])
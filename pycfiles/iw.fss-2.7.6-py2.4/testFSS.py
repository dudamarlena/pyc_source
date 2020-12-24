# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/tests/testFSS.py
# Compiled at: 2008-10-23 05:55:15
"""
Testing FSS features
$Id: testFSS.py 69084 2008-07-28 14:28:25Z b_mathieu $
"""
from common import *
from ZPublisher.HTTPRequest import HTTPRequest
from ZPublisher.HTTPResponse import HTTPResponse
from StringIO import StringIO
from zope.component import getUtility
from iw.fss.interfaces import IConf

class TestFSS(FSSTestCase.FSSTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()
        content_id = 'test_folder'
        self.portal.invokeFactory(FOLDER_TYPE, id=content_id)
        self.test_folder = getattr(self.portal, content_id)
        self.logout()
        self.portal_repository = self.portal.portal_repository
        conf_class = getUtility(IConf, 'globalconf')
        self.conf = conf_class()

    def testAddFileFromString(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByString(self.test_folder, content_id)
        file_field = self.file_content.getField('file')
        file_value = file_field.get(self.file_content)
        self.assertEquals(str(file_value.data), 'mytestfile')
        self.assertEquals(file_value.filename, '')
        self.assertEquals(file_value.get_size(), 10)
        self.assertEquals(file_field.getContentType(self.file_content), 'text/plain')
        bu = file_field.getBaseUnit(self.file_content)
        bu_value = bu.getRaw()
        self.assertEquals(len(bu_value), 10)
        self.assertEquals(bu_value, 'mytestfile')
        ftp_value = self.file_content.manage_FTPget()
        self.failIf(ftp_value is None)
        self.assertEquals(len(ftp_value), 10)
        self.assertEquals(ftp_value, 'mytestfile')
        self.logout()
        return

    def _testDefaultContentFromUploadedFile(self):
        file_field = self.file_content.getField('file')
        file_value = file_field.get(self.file_content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(self.file_content), 'application/msword')
        bu = file_field.getBaseUnit(self.file_content)
        bu_value = bu.getRaw()
        self.assertEquals(len(bu_value), 10240)
        ftp_value = self.file_content.manage_FTPget()
        self.failIf(ftp_value is None)
        self.assertEquals(len(ftp_value), 10240)
        return

    def testAddFileFromUploadedFile(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByFileUpload(self.test_folder, content_id)
        self._testDefaultContentFromUploadedFile()
        self.logout()

    def testEditFile(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByFileUpload(self.test_folder, content_id)
        self._testDefaultContentFromUploadedFile()
        data_path = self.getDataPath()
        self.updateContent(self.file_content, 'file', os.path.join(data_path, 'excel.xls'))
        file_field = self.file_content.getField('file')
        file_value = file_field.get(self.file_content)
        self.assertEquals(file_value.filename, 'excel.xls')
        self.assertEquals(file_value.get_size(), 13824)
        self.assertEquals(file_field.getContentType(self.file_content), 'application/vnd.ms-excel')
        self.logout()

    def testRenameContent(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByFileUpload(self.test_folder, content_id)
        old_uid = self.file_content.UID()
        new_content_id = 'new_test_file'
        self.test_folder.manage_renameObjects((content_id,), (new_content_id,))
        self.assertEquals(self.file_content.getId(), new_content_id)
        self.assertEquals(self.file_content.UID(), old_uid)
        self._testDefaultContentFromUploadedFile()
        self.logout()

    def testCopyContent(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByFileUpload(self.test_folder, content_id)
        cb = self.test_folder.manage_copyObjects(ids=(content_id,))
        new_folder_id = 'new_test_folder'
        self.portal.invokeFactory(FOLDER_TYPE, id=new_folder_id)
        new_folder = getattr(self.portal, new_folder_id)
        new_folder.manage_pasteObjects(cb_copy_data=cb)
        self._testDefaultContentFromUploadedFile()
        new_file_content = getattr(new_folder, content_id)
        file_field = new_file_content.getField('file')
        file_value = file_field.get(new_file_content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(new_file_content), 'application/msword')
        old_storage = getattr(self.test_folder, content_id).getField('file').getStorage()
        new_storage = file_field.getStorage()
        old_instance = getattr(self.test_folder, content_id)
        old_fss = old_storage.getFSSInfo('file', old_instance)
        new_fss = new_storage.getFSSInfo('file', new_file_content)
        old_brains = self.conf.getStorageBrainsByUID(old_fss.getUID())
        new_brains = self.conf.getStorageBrainsByUID(new_fss.getUID())
        st_old = [ x for x in old_brains if x['name'] == 'file' ][0]
        st_new = [ x for x in new_brains if x['name'] == 'file' ][0]
        self.assertNotEqual(old_fss.getUID(), new_fss.getUID())
        self.assertNotEqual(len(st_old.keys()), 0, str(st_old))
        self.assertNotEqual(len(st_new.keys()), 0, str(st_new))
        self.assertNotEqual(st_old['fs_path'], st_new['fs_path'])
        self.assertEqual(st_old['size'], st_new['size'])
        self.assertNotEqual(st_old['path'], st_new['path'])
        self.logout()

    def testCopyFolderWithImages(self):
        if not self.use_atct:
            return
        self.loginAsPortalOwner()
        self.portal.invokeFactory(id='test_source_folder', type_name=FOLDER_TYPE)
        self.sf = getattr(self.portal, 'test_source_folder')
        self.addImageByFileUpload(self.sf, 's1')
        self.addImageByFileUpload(self.sf, 's2')
        self.addImageByFileUpload(self.sf, 's3')
        self.addImageByFileUpload(self.sf, 's4')
        self.addImageByFileUpload(self.sf, 's5')
        self.addImageByFileUpload(self.sf, 's6')
        self.assertEqual(len(self.sf.objectValues()), 6)
        self.portal.invokeFactory(id='test_target_folder', type_name=FOLDER_TYPE)
        obnum = random.choice([1, 2, 3, 4, 5, 6])
        o_cobject = getattr(self.sf, 's%s' % obnum)
        o_storage = o_cobject.getField('image').getStorage()
        o_fssinfo = o_storage.getFSSInfo('image', o_cobject)
        o_brains = self.conf.getStorageBrainsByUID(o_fssinfo.getUID())
        cb = self.portal.manage_copyObjects(ids=(self.sf.getId(),))
        self.tf = getattr(self.portal, 'test_target_folder')
        self.assertEqual(len(self.tf.objectValues()), 0)
        self.tf.manage_pasteObjects(cb_copy_data=cb)
        self.assertEqual(len(self.tf.objectValues()), 1)
        self.cf = getattr(self.tf, 'test_source_folder')
        self.assertEqual(len(self.cf.objectValues()), 6)
        self.assertNotEqual(self.cf.getPhysicalPath(), self.sf.getPhysicalPath())
        self.assertEqual(self.cf.getId(), self.sf.getId())
        n_cobject = getattr(self.cf, 's%s' % obnum)
        n_storage = n_cobject.getField('image').getStorage()
        n_fssinfo = n_storage.getFSSInfo('image', n_cobject)
        n_brains = self.conf.getStorageBrainsByUID(n_fssinfo.getUID())
        self.assertNotEqual(o_fssinfo.getUID(), n_fssinfo.getUID())
        self.assertNotEqual(len(o_brains), 0, str(o_brains))
        self.assertNotEqual(len(n_brains), 0, str(n_brains))
        for name in ('image_mini', 'image_thumb'):
            fs_path = [ x['fs_path'] for x in o_brains if x['name'] == name ][0]
            assert os.path.exists(fs_path)

        for name in ('image_mini', 'image_thumb'):
            fs_path = [ x['fs_path'] for x in n_brains if x['name'] == name ][0]
            assert os.path.exists(fs_path)

        for name in ('image', 'image_mini', 'image_thumb'):
            o_brain = [ x for x in o_brains if x['name'] == name ][0]
            n_brain = [ x for x in n_brains if x['name'] == name ][0]
            self.assertNotEqual(o_brain['fs_path'], n_brain['fs_path'])
            self.assertEqual(o_brain['size'], n_brain['size'])
            self.assertNotEqual(o_brain['path'], n_brain['path'])

        old_s1_uid = self.sf.s1.UID()
        s1_brains = self.conf.getStorageBrainsByUID(old_s1_uid)
        assert len(s1_brains) > 0
        self.sf.manage_delObjects(['s1'])
        assert 's1' not in self.sf.objectIds()
        s1_brains = self.conf.getStorageBrainsByUID(old_s1_uid)
        assert len(s1_brains) == 0
        self.logout()

    def testCutContent(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByFileUpload(self.test_folder, content_id)
        old_uid = self.file_content.UID()
        old_storage = getattr(self.test_folder, content_id).getField('file').getStorage()
        old_instance = getattr(self.test_folder, content_id)
        old_fss = old_storage.getFSSInfo('file', old_instance)
        cb = self.test_folder.manage_cutObjects(ids=(content_id,))
        new_folder_id = 'new_test_folder'
        self.portal.invokeFactory(FOLDER_TYPE, id=new_folder_id)
        new_folder = getattr(self.portal, new_folder_id)
        new_folder.manage_pasteObjects(cb_copy_data=cb)
        self.failIf(hasattr(self.test_folder, content_id))
        new_file_content = getattr(new_folder, content_id)
        file_field = new_file_content.getField('file')
        file_value = file_field.get(new_file_content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(new_file_content), 'application/msword')
        self.assertEquals(new_file_content.UID(), old_uid)
        new_storage = file_field.getStorage()
        new_fss = new_storage.getFSSInfo('file', new_file_content)
        st_old = self.conf.getStorageBrainsByUID(old_fss.getUID())[0]
        st_new = self.conf.getStorageBrainsByUID(new_fss.getUID())[0]
        self.assertEqual(old_fss.getUID(), new_fss.getUID())
        self.assertNotEqual(len(st_old.keys()), 0, str(st_old))
        self.assertNotEqual(len(st_new.keys()), 0, str(st_new))
        self.assertEqual(st_old['fs_path'], st_new['fs_path'])
        self.assertEqual(st_old['size'], st_new['size'])
        self.logout()

    def testCutFolderWithFSSContent(self):
        self.loginAsPortalOwner()
        src_folder_id = 'src_folder'
        self.portal.invokeFactory(FOLDER_TYPE, id=src_folder_id)
        src_folder = getattr(self.portal, src_folder_id)
        src_content_id = 'src_file'
        src_content = self.addFileByFileUpload(src_folder, src_content_id)
        old_instance = src_content
        old_uid = old_instance.UID()
        old_storage = old_instance.getField('file').getStorage()
        old_fss = old_storage.getFSSInfo('file', old_instance)
        cb = self.portal.manage_cutObjects(ids=(src_folder_id,))
        dst_folder_id = 'dst_folder'
        self.portal.invokeFactory(FOLDER_TYPE, id=dst_folder_id)
        dst_folder = getattr(self.portal, dst_folder_id)
        dst_folder.manage_pasteObjects(cb_copy_data=cb)
        self.failIf(hasattr(self.portal, src_folder_id))
        new_folder = getattr(dst_folder, src_folder_id)
        new_content = getattr(new_folder, src_content_id)
        file_field = new_content.getField('file')
        file_value = file_field.get(new_content)
        self.failUnless(isinstance(file_value, VirtualBinary), file_value.__class__)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(new_content), 'application/msword')
        self.assertEquals(new_content.UID(), old_uid)
        new_storage = file_field.getStorage()
        new_fss = new_storage.getFSSInfo('file', new_content)
        st_old = self.conf.getStorageBrainsByUID(old_fss.getUID())[0]
        st_new = self.conf.getStorageBrainsByUID(new_fss.getUID())[0]
        self.assertEqual(old_fss.getUID(), new_fss.getUID())
        self.assertNotEqual(len(st_old.keys()), 0, str(st_old))
        self.assertNotEqual(len(st_new.keys()), 0, str(st_new))
        self.assertEqual(st_old['fs_path'], st_new['fs_path'])
        self.assertEqual(st_old['size'], st_new['size'])
        self.logout()

    def testDeleteContent(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByFileUpload(self.test_folder, content_id)
        self.test_folder.manage_delObjects(ids=[content_id])
        self.failIf(hasattr(self.test_folder, content_id))
        self.logout()

    def testStorageWhenDeleteContent(self):
        from FSSTestCase import STORAGE_PATH
        self.loginAsPortalOwner()
        content_id = 'test_file'
        self.file_content = self.addFileByFileUpload(self.test_folder, content_id)
        self.failUnlessEqual(len(os.listdir(STORAGE_PATH)), 1)
        self.test_folder.manage_delObjects(ids=[content_id])
        self.failUnlessEqual(len(os.listdir(STORAGE_PATH)), 0)
        self.logout()

    def testDeleteField(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        file_content = self.addFileByFileUpload(self.test_folder, content_id)
        file_field = file_content.getField('file')
        file_value = file_field.get(file_content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(file_content), 'application/msword')
        file_field.set(file_content, 'DELETE_FILE')
        file_value = file_field.get(file_content)
        self.assertEquals(file_value, '')

    def testModifyField(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        file_content = self.addFileByFileUpload(self.test_folder, content_id)
        file_field = file_content.getField('file')
        file_value = file_field.get(file_content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(file_content), 'application/msword')
        new_value = 'example of content'
        file_field.set(file_content, new_value)
        file_value = file_field.get(file_content)
        self.assertEquals(str(file_value), new_value)
        self.assertEquals(file_field.getContentType(file_content), 'text/plain')

    def test_setUID(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        file_content = self.addFileByFileUpload(self.test_folder, content_id)
        file_field = file_content.getField('file')
        file_value = file_field.get(file_content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(file_content), 'application/msword')
        file_content._setUID('dummyUID')
        self.assertEquals(file_content.UID(), 'dummyUID')
        file_field = file_content.getField('file')
        file_value = file_field.get(file_content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(file_content), 'application/msword')

    def testVirtualBinaryAbsoluteUrl(self):
        self.loginAsPortalOwner()
        content_id = 'test_file'
        file_content = self.addFileByFileUpload(self.test_folder, content_id)
        file_field = file_content.getField('file')
        file_value = file_field.get(file_content)
        url = '%(instance_url)s/%(name)s' % {'instance_url': file_content.absolute_url(), 'name': 'file'}
        self.assertEquals(file_value.absolute_url(), url)

    def _testFileStreamIterator(self, start, end):
        """
        unit test about range_filestream_iterator
        """
        from FSSTestCase import CONTENT_PATH
        from iw.fss.FileSystemStorage import range_filestream_iterator
        iterator = range_filestream_iterator(CONTENT_PATH, start, end, mode='rb')
        data = ''
        for i in iterator:
            data += i

        self.assertEqual(len(data), end - start, '%i != %i len is not correct' % (len(data), end - start))

    def testRangeFileStreamIterator(self):
        """ test range operation of file stream operator """
        self._testFileStreamIterator(0, 10)
        self._testFileStreamIterator(30, 1000)
        self._testFileStreamIterator(500, 1023)

    def testRangeSupport(self):
        """
        functionnal test of range support
        """
        self.loginAsPortalOwner()
        content_id = 'test_file'
        file_content = self.addFileByFileUpload(self.test_folder, content_id)
        file_field = file_content.getField('file')
        file_content = file_field.get(file_content)
        e = {'SERVER_NAME': 'foo', 'SERVER_PORT': '80', 'REQUEST_METHOD': 'GET'}
        out = StringIO()
        resp = HTTPResponse(stdout=out)
        req = HTTPRequest(sys.stdin, e, resp)
        req.RESPONSE = resp
        data = file_content.index_html(req, resp)
        self.failUnless(len(data) == len(file_content), 'not good lenght data ')
        e = {'SERVER_NAME': 'foo', 'SERVER_PORT': '80', 'REQUEST_METHOD': 'GET', 'HTTP_RANGE': 'bytes=0-10'}
        resp = HTTPResponse(stdout=out)
        req = HTTPRequest(sys.stdin, e, resp)
        req.RESPONSE = resp
        data = file_content.index_html(req, resp)
        read_data = ''
        for d in data:
            read_data += d

        self.failUnless(len(read_data) == 11, 'not good lenght data <%s>' % len(read_data))
        e = {'SERVER_NAME': 'foo', 'SERVER_PORT': '80', 'REQUEST_METHOD': 'GET', 'HTTP_RANGE': 'bytes=0-10, 50-80'}
        resp = HTTPResponse(stdout=out)
        req = HTTPRequest(sys.stdin, e, resp)
        req.RESPONSE = resp
        data = file_content.index_html(req, resp)

    def testCMFEditions(self):
        self.loginAsPortalOwner()
        portal_repository = self.portal_repository
        data_path = self.getDataPath()
        file1_path = os.path.join(data_path, 'word.doc')
        file1 = open(file1_path, 'rb').read()
        file2_path = os.path.join(data_path, 'excel.xls')
        file2 = open(file2_path, 'rb').read()
        image1_path = os.path.join(data_path, 'image.jpg')
        image1 = open(image1_path, 'rb').read()
        content = self.addATFileByFileUpload(self.folder, 'test_file_and_image')
        portal_repository.applyVersionControl(content, comment='save no 1')
        self.updateContent(content, 'file', file2_path)
        self.updateContent(content, 'image', image1_path)
        portal_repository.save(content, comment='save no 2')
        vdata = portal_repository.retrieve(content, 0)
        obj = vdata.object
        file_field = obj.getField('file')
        file_value = file_field.get(obj)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(obj), 'application/msword')
        vdata = portal_repository.retrieve(content, 1)
        obj = vdata.object
        file_field = obj.getField('file')
        file_value = file_field.get(obj)
        self.assertEquals(file_value.filename, 'excel.xls')
        self.assertEquals(file_value.get_size(), 13824)
        self.assertEquals(file_field.getContentType(obj), 'application/vnd.ms-excel')
        portal_repository.revert(content, 0)
        file_field = content.getField('file')
        file_value = file_field.get(content)
        self.assertEquals(file_value.filename, 'word.doc')
        self.assertEquals(file_value.get_size(), 10240)
        self.assertEquals(file_field.getContentType(content), 'application/msword')
        self.logout()


strategies = (
 (
  'FlatStorageStrategy', 'from iw.fss.strategy import FlatStorageStrategy'), ('DirectoryStorageStrategy', 'from iw.fss.strategy import DirectoryStorageStrategy'), ('SiteStorageStrategy', 'from iw.fss.strategy import SiteStorageStrategy'), ('SiteStorageStrategy2', 'from iw.fss.strategy import SiteStorageStrategy2'))
dynamic_class = '\n%(import)s\n\nclass Test%(name)s(TestFSS):\n    "Test fss"\n\n    strategy_klass = %(name)s\n'

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    module = sys.modules[TestFSS.__module__]
    for strategy in strategies:
        code = dynamic_class % {'name': strategy[0], 'import': strategy[1]}
        exec code in module.__dict__
        suite.addTest(makeSuite(getattr(module, 'Test%s' % strategy[0])))

    return suite


if __name__ == '__main__':
    framework()
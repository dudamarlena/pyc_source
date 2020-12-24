# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/tests/testSignedDocument.py
# Compiled at: 2012-03-06 02:26:51
"""
"""
__docformat__ = 'restructuredtext'
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
import time, transaction
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.Archetypes.interfaces.layer import ILayerContainer
from Products.Archetypes.public import *
from Products.ATContentTypes.tests.utils import dcEdit
from Products.ATContentTypes.tests.atcttestcase import ATCTTypeTestCase
from Products.BastionCrypto.SignedDocument import SignedDocument
from Products.ATContentTypes.lib.validators import TidyHtmlWithCleanupValidator
from Products.ATContentTypes.tests.utils import TidyHTMLValidator
from Products.ATContentTypes.tests.utils import input_file_path
from Products.CMFDefault.Document import Document
from Products.ATContentTypes.interfaces import IHistoryAware
from Products.ATContentTypes.interfaces import ITextContent
from Products.ATContentTypes.interfaces import IATDocument
from zope.interface.verify import verifyObject
from cgi import FieldStorage
from Products.ATContentTypes import config as atct_config
from ZPublisher.HTTPRequest import FileUpload
from Products.ATContentTypes.interface import IHistoryAware as Z3IHistoryAware
from Products.ATContentTypes.interface import ITextContent as Z3TextContent
from Products.ATContentTypes.interface import IATDocument as Z3IATDocument
from zope.interface.verify import verifyObject as Z3verifyObject
ZopeTestCase.installProduct('BastionCrypto')
example_stx = '\nHeader\n\n Text, Text, Text\n\n   * List\n   * List\n'
example_rest = '\nHeader\n======\n\nText, text, text\n\n* List\n* List\n'

def editCMF(obj):
    text_format = 'stx'
    dcEdit(obj)
    obj.edit(text_format=text_format, text=example_stx)


def editATCT(obj):
    text_format = 'text/structured'
    dcEdit(obj)
    obj.setText(example_stx, mimetype=text_format)


tests = []

class TestSiteSignedDocument(ATCTTypeTestCase):
    klass = SignedDocument
    portal_type = 'SignedDocument'
    cmf_portal_type = 'CMF Document'
    cmf_klass = Document
    title = 'Signed Document'
    meta_type = 'SignedDocument'
    icon = 'signed_document_icon.gif'

    def test_doesImplementHistoryAware(self):
        iface = IHistoryAware
        self.failUnless(iface.isImplementedBy(self._ATCT))
        self.failUnless(verifyObject(iface, self._ATCT))

    def test_doesImplementZ3HistoryAware(self):
        iface = Z3IHistoryAware
        self.failUnless(Z3verifyObject(iface, self._ATCT))

    def test_implementsTextContent(self):
        iface = ITextContent
        self.failUnless(iface.isImplementedBy(self._ATCT))
        self.failUnless(verifyObject(iface, self._ATCT))

    def test_implementsZ3TextContent(self):
        iface = Z3TextContent
        self.failUnless(Z3verifyObject(iface, self._ATCT))

    def test_implementsATDocument(self):
        iface = IATDocument
        self.failUnless(iface.isImplementedBy(self._ATCT))
        self.failUnless(verifyObject(iface, self._ATCT))

    def test_implementsZ3ATDocument(self):
        iface = Z3IATDocument
        self.failUnless(Z3verifyObject(iface, self._ATCT))

    def test_edit(self):
        old = self._cmf
        new = self._ATCT
        editCMF(old)
        editATCT(new)
        self.failUnless(old.CookedBody(stx_level=2) == new.CookedBody(), 'Body mismatch: %s / %s' % (
         old.CookedBody(stx_level=2), new.CookedBody()))

    def test_cmf_edit_failure(self):
        self._ATCT.edit(thisisnotcmfandshouldbeignored=1)

    def Xtest_migration(self):
        old = self._cmf
        id = old.getId()
        editCMF(old)
        title = old.Title()
        description = old.Description()
        mod = old.ModificationDate()
        created = old.CreationDate()
        body = old.CookedBody(stx_level=2)
        time.sleep(1.0)
        transaction.savepoint(optimistic=True)
        m = DocumentMigrator(old)
        m(unittest=1)
        transaction.savepoint(optimistic=True)
        self.failUnless(id in self.folder.objectIds(), self.folder.objectIds())
        migrated = getattr(self.folder, id)
        self.compareAfterMigration(migrated, mod=mod, created=created)
        self.compareDC(migrated, title=title, description=description)
        self.assertEquals(migrated.Schema()['text'].getContentType(migrated), 'text/structured')
        self.failUnless(migrated.CookedBody() == body, 'Body mismatch: %s / %s' % (
         migrated.CookedBody(), body))

    def test_rename_keeps_contenttype(self):
        doc = self._ATCT
        doc.setText(example_rest, mimetype='text/x-rst')
        self.failUnless(str(doc.getField('text').getContentType(doc)) == 'text/x-rst')
        transaction.savepoint(optimistic=True)
        cur_id = 'ATCT'
        new_id = 'WasATCT'
        self.folder.manage_renameObject(cur_id, new_id)
        doc = getattr(self.folder, new_id)
        field = doc.getField('text')
        self.failUnless(str(field.getContentType(doc)) == 'text/x-rst')

    def test_x_safe_html(self):
        doc = self._ATCT
        mimetypes = (
         ('text/html', '<p>test</p>'),
         ('text/structured', '<p><p>test</p></p>\n'))
        for (mimetype, expected) in mimetypes:
            text = "<p>test</p><script>I'm a nasty boy<p>nested</p></script>"
            doc.setText(text, mimetype=mimetype)
            txt = doc.getText()
            self.failUnlessEqual(txt, expected, (txt, expected, mimetype))

    def test_get_size(self):
        atct = self._ATCT
        editATCT(atct)
        self.failUnlessEqual(atct.get_size(), len(example_stx))

    if atct_config.HAS_MX_TIDY:

        def test_tidy_validator_with_upload_wrong_encoding(self):
            doc = self._ATCT
            field = doc.getField('text')
            request = self.app.REQUEST
            setattr(request, 'text_text_format', 'text/html')
            input_file_name = 'tidy1-in.html'
            in_file = open(input_file_path(input_file_name))
            env = {'REQUEST_METHOD': 'PUT'}
            headers = {'content-type': 'text/html', 'content-length': len(in_file.read()), 
               'content-disposition': 'attachment; filename=%s' % input_file_name}
            in_file.seek(0)
            fs = FieldStorage(fp=in_file, environ=env, headers=headers)
            f = FileUpload(fs)
            tcv = TidyHtmlWithCleanupValidator('tidy_validator_with_cleanup')
            result = tcv.__call__(f, field=field, REQUEST=request)
            self.assertEquals(result, 1)
            expected_file = open(input_file_path('tidy1-out.html'))
            expected = expected_file.read()
            expected_file.close()
            self.assertEquals(request['text_tidier_data'], expected)


tests.append(TestSiteSignedDocument)

class TestSignedDocumentFields(ATCTFieldTestCase):

    def afterSetUp(self):
        ATCTFieldTestCase.afterSetUp(self)
        self._dummy = self.createDummy(klass=SignedDocument)

    def test_text_field_mutator_filename(self):
        dummy = self._dummy
        field = dummy.getField('text')
        mutator = field.getMutator(dummy)
        self.assertEquals(field.getFilename(dummy), '')
        self.assertEquals(field.getContentType(dummy), 'text/html')
        mutator('', filename='foo.txt')
        self.assertEquals(field.getFilename(dummy), 'foo.txt')
        self.assertEquals(field.getContentType(dummy), 'text/plain')

    def test_text_field_mutator_mime(self):
        dummy = self._dummy
        field = dummy.getField('text')
        mutator = field.getMutator(dummy)
        self.assertEquals(field.getFilename(dummy), '')
        self.assertEquals(field.getContentType(dummy), 'text/html')
        mutator('', mimetype='text/plain')
        self.assertEquals(field.getFilename(dummy), '')
        self.assertEquals(field.getContentType(dummy), 'text/plain')

    def test_text_field_mutator_none_mime(self):
        dummy = self._dummy
        field = dummy.getField('text')
        mutator = field.getMutator(dummy)
        self.assertEquals(field.getFilename(dummy), '')
        self.assertEquals(field.getContentType(dummy), 'text/html')
        mutator('', mimetype=None)
        self.assertEquals(field.getFilename(dummy), '')
        self.assertEquals(field.getContentType(dummy), 'text/plain')
        return

    def test_text_field_mutator_none_filename(self):
        dummy = self._dummy
        field = dummy.getField('text')
        mutator = field.getMutator(dummy)
        self.assertEquals(field.getFilename(dummy), '')
        self.assertEquals(field.getContentType(dummy), 'text/html')
        mutator('', filename=None)
        self.assertEquals(field.getFilename(dummy), '')
        self.assertEquals(field.getContentType(dummy), 'text/plain')
        return

    def test_textField(self):
        dummy = self._dummy
        field = dummy.getField('text')
        self.failUnless(ILayerContainer.isImplementedBy(field))
        self.failUnless(field.required == 1, 'Value is %s' % field.required)
        self.failUnless(field.default == '', 'Value is %s' % str(field.default))
        self.failUnless(field.searchable == 1, 'Value is %s' % field.searchable)
        self.failUnless(field.vocabulary == (), 'Value is %s' % str(field.vocabulary))
        self.failUnless(field.enforceVocabulary == 0, 'Value is %s' % field.enforceVocabulary)
        self.failUnless(field.multiValued == 0, 'Value is %s' % field.multiValued)
        self.failUnless(field.isMetadata == 0, 'Value is %s' % field.isMetadata)
        self.failUnless(field.accessor == 'getText', 'Value is %s' % field.accessor)
        self.failUnless(field.mutator == 'setText', 'Value is %s' % field.mutator)
        self.failUnless(field.read_permission == View, 'Value is %s' % field.read_permission)
        self.failUnless(field.write_permission == ModifyPortalContent, 'Value is %s' % field.write_permission)
        self.failUnless(field.generateMode == 'veVc', 'Value is %s' % field.generateMode)
        self.failUnless(field.force == '', 'Value is %s' % field.force)
        self.failUnless(field.type == 'text', 'Value is %s' % field.type)
        self.failUnless(isinstance(field.storage, AnnotationStorage), 'Value is %s' % type(field.storage))
        self.failUnless(field.getLayerImpl('storage') == AnnotationStorage(migrate=True), 'Value is %s' % field.getLayerImpl('storage'))
        self.failUnless(ILayerContainer.isImplementedBy(field))
        self.failUnless(field.validators == TidyHTMLValidator, 'Value is %s' % repr(field.validators))
        self.failUnless(isinstance(field.widget, RichWidget), 'Value is %s' % id(field.widget))
        vocab = field.Vocabulary(dummy)
        self.failUnless(isinstance(vocab, DisplayList), 'Value is %s' % type(vocab))
        self.failUnless(tuple(vocab) == (), 'Value is %s' % str(tuple(vocab)))
        self.failUnless(field.primary == 1, 'Value is %s' % field.primary)
        self.failUnless(field.default_content_type == 'text/html', 'Value is %s' % field.default_content_type)
        self.failUnless(field.default_output_type == 'text/x-html-safe', 'Value is %s' % field.default_output_type)
        self.failUnless('text/html' in field.allowable_content_types)
        self.failUnless('text/structured' in field.allowable_content_types)


tests.append(TestSignedDocumentFields)

class TestSignedDocumentFunctional(ATCTIntegrationTestCase):
    portal_type = 'SignedDocument'
    views = ('signed_document_view', )

    def afterSetUp(self):
        self.loginAsPortalOwner()
        ATCTIntegrationTestCase.afterSetUp(self)

    def test_id_change_on_initial_edit(self):
        """Make sure Id is taken from title on initial edit and not otherwise"""
        response = self.publish(self.folder_path + '/createObject?type_name=%s' % self.portal_type, self.basic_auth)
        self.assertStatusEqual(response.getStatus(), 302)
        location = response.getHeader('Location').split('?')[0]
        self.failUnless(location.startswith(self.folder_url), location)
        self.failUnless(location.endswith('edit'), location)
        edit_form_path = location[len(self.app.REQUEST.SERVER_URL):]
        response = self.publish(edit_form_path, self.basic_auth)
        self.assertStatusEqual(response.getStatus(), 200)
        temp_id = location.split('/')[(-2)]
        obj_title = 'New Title for Object'
        new_id = 'new-title-for-object'
        new_obj = getattr(self.folder.aq_explicit, temp_id)
        new_obj_path = '/%s' % new_obj.absolute_url(1)
        self.failUnlessEqual(new_obj.checkCreationFlag(), True)
        response = self.publish('%s/atct_edit?form.submitted=1&title=%s&text=Blank' % (new_obj_path, obj_title), self.basic_auth)
        self.assertStatusEqual(response.getStatus(), 302)
        self.failUnlessEqual(new_obj.getId(), new_id)
        self.failUnlessEqual(new_obj.checkCreationFlag(), False)
        new_title = 'Second Title'
        response = self.publish('%s/atct_edit?form.submitted=1&title=%s&text=Blank' % ('/%s' % new_obj.absolute_url(1), new_title), self.basic_auth)
        self.assertStatusEqual(response.getStatus(), 302)
        self.failUnlessEqual(new_obj.getId(), new_id)


tests.append(TestSignedDocumentFunctional)

def test_suite():
    import unittest
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    return suite
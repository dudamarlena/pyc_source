# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/archetypes/schematuning/tests/test_update_schema.py
# Compiled at: 2010-01-22 07:59:46
import sys
from ZPublisher.HTTPRequest import HTTPRequest
from Testing import ZopeTestCase
from Products.Archetypes.ArchetypeTool import registerType
from Products.Archetypes.atapi import *
from Products.Archetypes.tests.utils import mkDummyInContext
from archetypes.schematuning.tests.base import SchemaTuningTestCase
textfield1 = TextField('TEXTFIELD1', required=True, default='A')
textfield1b = TextField('TEXTFIELD1', required=False, default='A')
textfield2 = TextField('TEXTFIELD2', default='B')
schema1 = BaseSchema + Schema((textfield1,))
schema2 = BaseSchema + Schema((textfield1b, textfield2))

class Dummy1(BaseContent):
    __module__ = __name__


class Dummy2(BaseContent):
    __module__ = __name__


class TestUpdateSchema(ZopeTestCase.Sandboxed, SchemaTuningTestCase):
    __module__ = __name__

    def afterSetUp(self):
        SchemaTuningTestCase.afterSetUp(self)
        self.attool = self.portal.archetype_tool
        self._dummy1 = mkDummyInContext(Dummy1, oid='dummy1', context=self.portal, schema=schema1)
        self._dummy2 = mkDummyInContext(Dummy2, oid='dummy2', context=self.portal, schema=schema2)

    def test_instance_schema_is_harmful(self):
        """Show that having a schema in the instance is harmful.

        schema should be a class attribute, not an instance attribute.

        The only thing this really tests is that for AT >= 1.5.2,
        having a schema attribute on the instance is bad.  In earlier
        ATs this is no problem.  Nothing bad happens due to the
        earlier AT code.  But the newer ATs cannot handle older
        content that has had a schema update already.

        So: if you copy this test to an earlier Archetypes and it
        fails, that is okay really.  But in AT >= 1.5.2 it does *not*
        fail and this means that some code needs be added to migrate
        old content.
        """
        dummy = self._dummy1
        self.failUnless(dummy._isSchemaCurrent())
        self.failIf('schema' in dummy.__dict__)
        dummy.schema = dummy.__class__.schema
        self.failUnless('schema' in dummy.__dict__)
        self.failUnless(dummy._isSchemaCurrent())
        dummy.__class__.schema = schema2.copy()
        dummy.invalidateSchema()
        registerType(Dummy1, 'Archetypes')
        dummy._signature = 'bogus'
        dummy.invalidateSchema()
        self.failIf(dummy._isSchemaCurrent())
        dummy.getTEXTFIELD2
        self.assertRaises(KeyError, dummy.getTEXTFIELD2)
        dummy._updateSchema()
        self.failUnless(hasattr(dummy, 'getTEXTFIELD2'))
        self.assertRaises(KeyError, dummy.getTEXTFIELD2)
        self.failIf(hasattr(dummy, 'TEXTFIELD2'))
        self.failUnless(dummy.getField('TEXTFIELD1').required)
        del dummy.schema
        dummy.invalidateSchema()
        self.failIf(dummy.getField('TEXTFIELD1').required)
        self.failIf(hasattr(dummy, 'TEXTFIELD2'))
        self.assertEqual(dummy.getTEXTFIELD2(), 'B')
        self.assertEqual(dummy.TEXTFIELD2(), 'B')

    def test_no_schema_attribute_added(self):
        """Does updating the schema mess things up?

        Updating the schema should not add the schema as instance
        attribute, unless you *really* know what you are doing.
        """
        dummy = self._dummy1
        dummy._updateSchema()
        self.failIf('schema' in dummy.__dict__)

    def test_detect_schema_change(self):
        dummy = self._dummy1
        self.failUnless(dummy._isSchemaCurrent())
        dummy.__class__.schema = schema2.copy()
        dummy.invalidateSchema()
        registerType(Dummy1, 'Archetypes')
        dummy._isSchemaCurrent()
        self.failIf(dummy._isSchemaCurrent())
        dummy._updateSchema()
        self.failUnless(dummy._isSchemaCurrent())

    def test_remove_instance_schemas(self):
        dummy = self._dummy1
        dummy.schema = schema2.copy()
        dummy.invalidateSchema()
        self.failUnless('schema' in dummy.__dict__)
        dummy._updateSchema()
        self.failUnless('schema' in dummy.__dict__)
        dummy._updateSchema(remove_instance_schemas=True)
        self.failIf('schema' in dummy.__dict__)

    def test_manage_update_schema(self):
        dummy = self._dummy1
        dummy.schema = schema2.copy()
        dummy.invalidateSchema()
        self.failUnless('schema' in dummy.__dict__)
        self.failIf(dummy._isSchemaCurrent())
        self.assertEqual(self.types_to_update(), [])
        self.attool._types['Archetypes.Dummy1'] = 'cheat'
        self.assertEqual(self.types_to_update(), ['Archetypes.Dummy1'])
        self.attool.manage_updateSchema()
        self.failUnless('schema' in dummy.__dict__)
        self.failUnless(dummy._isSchemaCurrent())
        dummy._signature = 'bogus'
        dummy.invalidateSchema()
        self.failIf(dummy._isSchemaCurrent())
        self.assertEqual(self.types_to_update(), [])
        self.attool._types['Archetypes.Dummy1'] = 'cheat'
        self.assertEqual(self.types_to_update(), ['Archetypes.Dummy1'])
        self.attool.manage_updateSchema(remove_instance_schemas=True)
        self.failIf('schema' in dummy.__dict__)

    def types_to_update(self):
        """Which types have a changed schema?
        """
        return [ ti[0] for ti in self.attool.getChangedSchema() if ti[1] ]


class TestBasicSchemaUpdate(SchemaTuningTestCase):
    """Tests for update schema behavior which depend only on the basic
       types, and examine baseline behavior when no real schema changes have
       happened."""
    __module__ = __name__

    def test_update_preserves_mimetype(self):
        self.folder.invokeFactory('DDocument', 'mydoc', title='My Doc')
        doc = self.folder.mydoc
        doc.setBody('\nAn rst Document\n===============\n\n* Which\n\n  * has\n\n  * some\n\n* bullet::\n\n  points.\n\n* for testing', mimetype='text/restructured')
        doc.reindexObject()
        mimetype = doc.getField('body').getContentType(doc)
        self.assertEqual(mimetype, 'text/x-rst')
        request = HTTPRequest(sys.stdin, {'SERVER_NAME': 'test', 'SERVER_PORT': '8080'}, {})
        request.form['Archetypes.DDocument'] = True
        request.form['update_all'] = True
        self.portal.archetype_tool.manage_updateSchema(REQUEST=request)
        doc = self.folder.mydoc
        mimetype = doc.getField('body').getContentType(doc)
        self.assertEqual(mimetype, 'text/x-rst')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUpdateSchema))
    suite.addTest(makeSuite(TestBasicSchemaUpdate))
    return suite
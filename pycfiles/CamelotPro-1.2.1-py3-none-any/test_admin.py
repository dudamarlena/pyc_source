# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_admin.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nTests for the Admin classes\n'
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.entity_admin import EntityAdmin
from camelot.admin.object_admin import ObjectAdmin
from camelot.test import ModelThreadTestCase
from camelot.view.controls import delegates
from camelot.view.art import Icon
from PyQt4.QtCore import Qt
from sqlalchemy import schema, types

class ApplicationAdminCase(ModelThreadTestCase):

    def test_application_admin(self):
        app_admin = ApplicationAdmin()
        self.assertTrue(app_admin.get_sections())
        self.assertTrue(app_admin.create_main_window())
        self.assertTrue(app_admin.get_related_toolbar_actions(Qt.RightToolBarArea, 'onetomany'))
        self.assertTrue(app_admin.get_related_toolbar_actions(Qt.RightToolBarArea, 'manytomany'))
        self.assertTrue(app_admin.get_version())
        self.assertTrue(app_admin.get_icon())
        self.assertTrue(app_admin.get_splashscreen())
        self.assertTrue(app_admin.get_organization_name())
        self.assertTrue(app_admin.get_organization_domain())
        self.assertTrue(app_admin.get_stylesheet())
        self.assertTrue(app_admin.get_about())

    def test_admin_for_exising_database(self):
        from .snippet.existing_database import app_admin
        self.assertTrue(app_admin.get_sections())


class ObjectAdminCase(ModelThreadTestCase):
    """Test the ObjectAdmin
    """

    def setUp(self):
        super(ObjectAdminCase, self).setUp()
        self.app_admin = ApplicationAdmin()

    def test_not_editable_admin_class_decorator(self):
        from camelot.model.i18n import Translation
        from camelot.admin.not_editable_admin import not_editable_admin
        OriginalAdmin = Translation.Admin
        original_admin = OriginalAdmin(self.app_admin, Translation)
        self.assertTrue(len(original_admin.get_list_actions()))
        self.assertTrue(original_admin.get_field_attributes('value')['editable'])
        NewAdmin = not_editable_admin(Translation.Admin, actions=True)
        new_admin = NewAdmin(self.app_admin, Translation)
        self.assertTrue(len(new_admin.get_list_actions()))
        self.assertFalse(new_admin.get_field_attributes('value')['editable'])
        self.assertFalse(new_admin.get_field_attributes('source')['editable'])
        NewAdmin = not_editable_admin(Translation.Admin, actions=False)
        new_admin = NewAdmin(self.app_admin, Translation)
        self.assertFalse(len(new_admin.get_list_actions()))
        self.assertFalse(new_admin.get_field_attributes('value')['editable'])
        self.assertFalse(new_admin.get_field_attributes('source')['editable'])
        NewAdmin = not_editable_admin(Translation.Admin, editable_fields=[
         'value'])
        new_admin = NewAdmin(self.app_admin, Translation)
        self.assertFalse(len(new_admin.get_list_actions()))
        self.assertTrue(new_admin.get_field_attributes('value')['editable'])
        self.assertFalse(new_admin.get_field_attributes('source')['editable'])

    def test_signature(self):

        class A(object):

            def __init__(self):
                self.x = 1
                self.y = 2

            class Admin(ObjectAdmin):
                list_display = [
                 'x', 'y']

        a = A()
        a_admin = self.app_admin.get_related_admin(A)
        self.assertTrue(str(a_admin))
        self.assertTrue(repr(a_admin))
        self.assertFalse(a_admin.primary_key(a))
        self.assertTrue(isinstance(a_admin.get_modifications(a), dict))
        a_admin.get_icon()
        a_admin.flush(a)
        a_admin.delete(a)
        a_admin.expunge(a)
        a_admin.refresh(a)
        a_admin.add(a)
        a_admin.is_deleted(a)
        a_admin.is_persistent(a)
        a_admin.copy(a)


class EntityAdminCase(ModelThreadTestCase):
    """Test the EntityAdmin
    """

    def setUp(self):
        super(EntityAdminCase, self).setUp()
        self.app_admin = ApplicationAdmin()

    def test_sql_field_attributes(self):
        column_1 = schema.Column(types.Unicode(), nullable=False)
        fa_1 = EntityAdmin.get_sql_field_attributes([column_1])
        self.assertTrue(fa_1['editable'])
        self.assertFalse(fa_1['nullable'])
        self.assertEqual(fa_1['delegate'], delegates.PlainTextDelegate)
        column_2 = schema.Column(types.FLOAT(), nullable=True)
        fa_2 = EntityAdmin.get_sql_field_attributes([column_2])
        self.assertTrue(fa_2['editable'])
        self.assertTrue(fa_2['nullable'])
        self.assertEqual(fa_2['delegate'], delegates.FloatDelegate)
        from sqlalchemy.dialects import mysql
        column_3 = schema.Column(mysql.BIGINT(), default=2)
        fa_3 = EntityAdmin.get_sql_field_attributes([column_3])
        self.assertTrue(fa_3['default'])
        self.assertEqual(fa_3['delegate'], delegates.IntegerDelegate)
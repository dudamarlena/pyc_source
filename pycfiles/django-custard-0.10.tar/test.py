# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucio/Projects/django-custard/custard/custard/tests/test.py
# Compiled at: 2015-06-10 04:56:13
from __future__ import unicode_literals
from datetime import date, time, datetime
import django
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from custard.conf import CUSTOM_TYPE_TEXT, CUSTOM_TYPE_INTEGER, CUSTOM_TYPE_BOOLEAN, CUSTOM_TYPE_FLOAT, CUSTOM_TYPE_DATE, CUSTOM_TYPE_DATETIME, CUSTOM_TYPE_TIME, settings
from custard.builder import CustomFieldsBuilder
from custard.utils import import_class
from .models import SimpleModelWithManager, SimpleModelWithoutManager, CustomFieldsModel, CustomValuesModel, builder

class SimpleModelWithManagerForm(builder.create_modelform()):

    class Meta:
        model = SimpleModelWithManager
        fields = b'__all__'


class CustomModelsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.simple_with_manager_ct = ContentType.objects.get_for_model(SimpleModelWithManager)
        self.simple_without_manager_ct = ContentType.objects.get_for_model(SimpleModelWithoutManager)
        self.cf = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'text_field', label=b'Text field', data_type=CUSTOM_TYPE_TEXT)
        self.cf.save()
        self.cf2 = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'another_text_field', label=b'Text field 2', data_type=CUSTOM_TYPE_TEXT, required=True, searchable=False)
        self.cf2.clean()
        self.cf2.save()
        self.cf3 = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'int_field', label=b'Integer field', data_type=CUSTOM_TYPE_INTEGER)
        self.cf3.save()
        self.cf4 = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'boolean_field', label=b'Boolean field', data_type=CUSTOM_TYPE_BOOLEAN)
        self.cf4.save()
        self.cf5 = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'float_field', label=b'Float field', data_type=CUSTOM_TYPE_FLOAT)
        self.cf5.save()
        self.cf6 = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'date_field', label=b'Date field', data_type=CUSTOM_TYPE_DATE)
        self.cf6.save()
        self.cf7 = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'datetime_field', label=b'Datetime field', data_type=CUSTOM_TYPE_DATETIME)
        self.cf7.save()
        self.cf8 = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'time_field', label=b'Time field', data_type=CUSTOM_TYPE_TIME)
        self.cf8.save()
        self.obj = SimpleModelWithManager.objects.create(name=b'old test')
        self.obj.save()

    def tearDown(self):
        CustomFieldsModel.objects.all().delete()

    def test_import_class(self):
        self.assertEqual(import_class(b'custard.builder.CustomFieldsBuilder'), CustomFieldsBuilder)

    def test_model_repr(self):
        self.assertEqual(repr(self.cf), b'<CustomFieldsModel: text_field>')
        val = CustomValuesModel.objects.create(custom_field=self.cf, object_id=self.obj.pk, value=b'abcdefg')
        val.save()
        self.assertEqual(repr(val), b'<CustomValuesModel: text_field: abcdefg>')

    @override_settings(CUSTOM_CONTENT_TYPES=[b'tests.SimpleModelWithManager'])
    def test_field_creation(self):
        builder2 = CustomFieldsBuilder(b'tests.CustomFieldsModel', b'tests.CustomValuesModel', settings.CUSTOM_CONTENT_TYPES)

        class TestCustomFieldsModel(builder2.create_fields()):

            class Meta:
                app_label = b'tests'

        self.assertQuerysetEqual(ContentType.objects.filter(builder2.content_types_query), ContentType.objects.filter(Q(app_label__in=[b'tests'], model__in=[
         b'SimpleModelWithManager'])))

    def test_mixin(self):
        self.assertIn(self.cf, self.obj.get_custom_fields())
        self.assertIn(self.cf, SimpleModelWithManager.get_model_custom_fields())
        self.assertEqual(self.cf, self.obj.get_custom_field(b'text_field'))
        with self.assertRaises(ObjectDoesNotExist):
            self.obj.get_custom_value(b'non_existent_value')
        val = CustomValuesModel.objects.create(custom_field=self.cf, object_id=self.obj.pk, value=b'123456')
        val.save()
        self.assertEqual(b'123456', self.obj.get_custom_value(b'text_field').value)
        self.obj.set_custom_value(b'text_field', b'abcdefg')
        self.assertEqual(b'abcdefg', self.obj.get_custom_value(b'text_field').value)
        val.delete()

    def test_field_model_clean(self):
        cf = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'another_text_field', label=b'Text field already present', data_type=CUSTOM_TYPE_INTEGER)
        with self.assertRaises(ValidationError):
            cf.full_clean()
        cf = CustomFieldsModel.objects.create(content_type=self.simple_with_manager_ct, name=b'name', label=b'Text field already in model', data_type=CUSTOM_TYPE_TEXT)
        with self.assertRaises(ValidationError):
            cf.full_clean()

    def test_value_model_clean(self):
        val = CustomValuesModel.objects.create(custom_field=self.cf2, object_id=self.obj.pk)
        val.value = b'qwertyuiop'
        val.save()
        val = CustomValuesModel.objects.create(custom_field=self.cf2, object_id=self.obj.pk)
        val.value = b'qwertyuiop'
        with self.assertRaises(ValidationError):
            val.full_clean()

    def test_value_types_accessor(self):
        val = CustomValuesModel.objects.create(custom_field=self.cf2, object_id=self.obj.pk)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf2, object_id=self.obj.pk, value=b'xxxxxxxxxxxxx')
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf3, object_id=self.obj.pk)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf3, object_id=self.obj.pk, value=1)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf4, object_id=self.obj.pk)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf4, object_id=self.obj.pk, value=True)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf5, object_id=self.obj.pk)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf5, object_id=self.obj.pk, value=3.1456)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf6, object_id=self.obj.pk)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf6, object_id=self.obj.pk, value=date.today())
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf7, object_id=self.obj.pk)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf7, object_id=self.obj.pk, value=datetime.now())
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf8, object_id=self.obj.pk)
        val.save()
        val = val.value
        val = CustomValuesModel.objects.create(custom_field=self.cf8, object_id=self.obj.pk, value=datetime.now().time())
        val.save()
        val = val.value

    def test_value_creation(self):
        val = CustomValuesModel.objects.create(custom_field=self.cf, object_id=self.obj.pk, value=b'qwertyuiop')
        val.save()
        self.assertEqual(val.content_type, self.simple_with_manager_ct)
        self.assertEqual(val.content_type, val.custom_field.content_type)
        self.assertEqual(val.value_text, b'qwertyuiop')
        self.assertEqual(val.value, b'qwertyuiop')

    def test_value_search(self):
        newobj = SimpleModelWithManager.objects.create(name=b'new simple')
        newobj.save()
        v1 = CustomValuesModel.objects.create(custom_field=self.cf, object_id=self.obj.pk, value=b'qwertyuiop')
        v1.save()
        v2 = CustomValuesModel.objects.create(custom_field=self.cf, object_id=newobj.pk, value=b'qwertyuiop')
        v2.save()
        v3 = CustomValuesModel.objects.create(custom_field=self.cf, object_id=newobj.pk, value=b'000asdf123')
        v3.save()
        qs1 = SimpleModelWithManager.objects.search(b'asdf')
        self.assertQuerysetEqual(qs1, [repr(newobj)])
        qs2 = SimpleModelWithManager.objects.search(b'qwerty')
        self.assertQuerysetEqual(qs2, [repr(self.obj), repr(newobj)], ordered=False)

    def test_value_search_not_searchable_field(self):
        v1 = CustomValuesModel.objects.create(custom_field=self.cf, object_id=self.obj.pk, value=b'12345')
        v1.save()
        v2 = CustomValuesModel.objects.create(custom_field=self.cf2, object_id=self.obj.pk, value=b'67890')
        v2.save()
        qs1 = SimpleModelWithManager.objects.search(b'12345')
        self.assertQuerysetEqual(qs1, [repr(self.obj)])
        qs2 = SimpleModelWithManager.objects.search(b'67890')
        self.assertQuerysetEqual(qs2, [])

    def test_get_formfield_for_field(self):
        with self.settings(CUSTOM_FIELD_TYPES={CUSTOM_TYPE_TEXT: b'django.forms.fields.EmailField'}):
            builder2 = CustomFieldsBuilder(b'tests.CustomFieldsModel', b'tests.CustomValuesModel')

            class SimpleModelWithManagerForm2(builder2.create_modelform(field_types=settings.CUSTOM_FIELD_TYPES)):

                class Meta:
                    model = SimpleModelWithManager
                    fields = b'__all__'

            form = SimpleModelWithManagerForm2(data={}, instance=self.obj)
            self.assertIsNotNone(form.get_formfield_for_field(self.cf))
            self.assertEqual(django.forms.fields.EmailField, form.get_formfield_for_field(self.cf).__class__)

    def test_get_widget_for_field(self):
        with self.settings(CUSTOM_WIDGET_TYPES={CUSTOM_TYPE_TEXT: b'django.forms.widgets.CheckboxInput'}):
            builder2 = CustomFieldsBuilder(b'tests.CustomFieldsModel', b'tests.CustomValuesModel')

            class SimpleModelWithManagerForm2(builder2.create_modelform(widget_types=settings.CUSTOM_WIDGET_TYPES)):

                class Meta:
                    fields = b'__all__'
                    model = SimpleModelWithManager

            form = SimpleModelWithManagerForm2(data={}, instance=self.obj)
            self.assertIsNotNone(form.get_widget_for_field(self.cf))
            self.assertEqual(django.forms.widgets.CheckboxInput, form.get_widget_for_field(self.cf).__class__)

    def test_form(self):

        class TestForm(builder.create_modelform()):
            custom_name = b'My Custom Fields'
            custom_description = b'Edit the Example custom fields here'
            custom_classes = b'zzzap-class'

            class Meta:
                fields = b'__all__'
                model = SimpleModelWithManager

        request = self.factory.post(b'/', {b'text_field': b'123'})
        form = TestForm(request.POST, instance=self.obj)
        self.assertFalse(form.is_valid())
        self.assertIn(b'another_text_field', form.errors)
        self.assertRaises(ValueError, lambda : form.save())
        request = self.factory.post(b'/', {b'id': self.obj.pk, b'name': b'xxx', 
           b'text_field': b'000111222333', 
           b'another_text_field': b'wwwzzzyyyxxx'})
        form = TestForm(request.POST, instance=self.obj)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.obj.get_custom_value(b'text_field').value, b'000111222333')
        self.assertEqual(self.obj.get_custom_value(b'another_text_field').value, b'wwwzzzyyyxxx')
        self.assertEqual(self.obj.name, b'xxx')
        request = self.factory.post(b'/', {b'id': self.obj.pk, b'name': b'aaa', 
           b'another_text_field': b'qqqwwweeerrrtttyyyy'})
        form = TestForm(request.POST, instance=self.obj)
        self.assertTrue(form.is_valid())
        obj = form.save(commit=False)
        obj.save()
        self.assertEqual(obj.another_text_field, b'wwwzzzyyyxxx')
        form.save_m2m()
        form.save_custom_fields()
        self.assertEqual(obj.another_text_field, b'qqqwwweeerrrtttyyyy')
        self.assertEqual(obj.name, b'aaa')

    def test_admin(self):
        modeladmin_class = builder.create_modeladmin()
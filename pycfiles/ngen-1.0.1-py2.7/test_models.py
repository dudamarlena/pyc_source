# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngen/tests/test_models.py
# Compiled at: 2017-10-08 17:55:08
from __future__ import unicode_literals, print_function, absolute_import
import unittest
try:
    import mock
except ImportError:
    from unittest import mock

from ngen.exceptions import ValidationError
from ngen.models import BaseOptions, BooleanField, CharField, Field, FieldError, FieldOptions, ImproperlyConfigured, IntegerField, ListField, Model, ModelField, ModelMeta, ModelOptions, ModelType, NOT_FOUND

class TestBaseOptions(unittest.TestCase):

    class TempOptions(BaseOptions):

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    options = TempOptions(_missing=True, here=True)

    class IncompleteOptions(BaseOptions):
        pass

    def test_IncompleteOptions_raises_when_instantiated(self):
        self.assertRaises(TypeError, self.IncompleteOptions)

    def test_len_equals_iter_len(self):
        self.assertEqual(len(self.options), len(dict(self.options)))
        self.assertEqual(len(self.options), 1)

    def test_mapping(self):

        def func(**kwargs):
            return kwargs

        self.assertEqual(func(**self.options), {b'here': True})

    def test_str(self):
        self.assertEqual(str(self.options), b'(here=True)')

    def test_repr(self):
        self.assertEqual(repr(self.options), b'<TempOptions: (here=True)>')

    def test_iter(self):
        self.assertEqual(dict(self.options), {b'here': True})


class TestModelOptions(unittest.TestCase):

    def test_is_subclass_of_BaseOptions(self):
        self.assertTrue(issubclass(ModelOptions, BaseOptions))

    def test_init_with_no_meta_cls(self):
        options = ModelOptions()
        self.assertFalse(options.abstract)

    def test_init_with_meta_cls(self):

        class Meta:
            abstract = True

        options = ModelOptions(Meta)
        self.assertTrue(options.abstract)

    def test_init_with_meta_cls_unknown_options(self):

        class Meta:
            unknown = b'value'

        self.assertRaises(ImproperlyConfigured, ModelOptions, Meta)


class TestModelMeta(unittest.TestCase):

    def test_init_defaults(self):
        meta = ModelMeta()
        self.assertIsNone(meta.model)
        self.assertEqual(meta.fields, [])
        self.assertEqual(meta.field_names, [])

    def test_init_kwargs_mapping(self):
        meta = ModelMeta(test=True)
        self.assertTrue(meta.test)

    def test_str(self):
        meta = ModelMeta()
        field1 = mock.MagicMock()
        field1.name = b'foo'
        meta.add_field(field1)
        field2 = mock.MagicMock()
        field2.name = b'bar'
        meta.add_field(field2)
        self.assertEqual(str(meta), b'foo, bar')

    def test_repr(self):
        meta = ModelMeta()
        meta.model = b'test'
        self.assertEqual(repr(meta), b'<Meta: test>')

    def test_add_field(self):
        meta = ModelMeta()
        field = mock.MagicMock()
        field.name = b'test'
        meta.add_field(field)
        self.assertEqual(field.rel_idx, 0)
        self.assertTrue(field in meta.fields)
        self.assertTrue(b'test' in meta.field_names)

    def test_add_field_with_field_replacement(self):
        meta = ModelMeta()
        field1 = mock.MagicMock()
        field1.name = b'foo'
        meta.add_field(field1)
        field2 = mock.MagicMock()
        field2.name = b'bar'
        meta.add_field(field2)
        self.assertTrue(meta.get_field(b'foo'), field1)
        self.assertTrue(meta.fields[0], field1)
        self.assertTrue(meta.fields[1], field2)
        field3 = mock.MagicMock()
        field3.name = b'foo'
        meta.add_field(field3)
        self.assertTrue(meta.get_field(b'foo'), field3)
        self.assertTrue(meta.fields[0], field3)
        self.assertTrue(meta.fields[1], field2)


class TestModelType(unittest.TestCase):

    def test_meta_class_attr(self):
        self.assertEqual(ModelType.meta_class, ModelMeta)

    def test_options_class(self):
        self.assertEqual(ModelType.options_class, ModelOptions)

    def test_Meta_is_not_an_attribute(self):

        class Meta:
            abstract = False

        model = ModelType.__new__(ModelType, str(b'SomeModel'), (
         Model,), {b'Meta': Meta, b'__module__': b'foo'})
        self.assertFalse(hasattr(model, b'Meta'))

    def test_add_meta(self):
        with mock.patch.object(ModelType, b'meta_class') as (meta_class):
            with mock.patch.object(ModelType, b'options_class') as (options_class):
                options_class.return_value = {}
                meta = mock.MagicMock()
                meta_class.return_value = meta
                _meta = mock.MagicMock()
                model = ModelType.__new__(ModelType, str(b'SomeModel'), (
                 Model,), {b'Meta': _meta, b'__module__': b'foo'})
                options_class.assert_called_once_with(_meta)
                meta_class.assert_called_once_with(model)
                self.assertEqual(model.meta, meta)

    def test_add_parent_fields(self):
        with mock.patch.object(Model, b'meta') as (meta):
            field = mock.MagicMock()
            field.add_to_class = mock.MagicMock()
            meta.fields = [field]
            model = ModelType.__new__(ModelType, str(b'SomeModel'), (
             Model,), {b'__module__': b'foo'})
            self.assertTrue(field.add_to_class.called)
            field.add_to_class.assert_called_once_with(model, field.name)

    def test_add_fields(self):
        field = CharField()
        with mock.patch.object(field, b'add_to_class') as (add_to_class):
            model = ModelType.__new__(ModelType, str(b'SomeModel'), (
             Model,), {b'__module__': b'foo', b'foo': field})
            self.assertFalse(hasattr(model, b'foo'))
            self.assertTrue(add_to_class.called)
            add_to_class.assert_called_once_with(model, b'foo')

    def test_attribute_instances_with_add_to_class_method(self):
        thing = mock.MagicMock()
        thing.add_to_class = mock.MagicMock()
        model = ModelType.__new__(ModelType, str(b'SomeModel'), (
         Model,), {b'__module__': b'foo', b'foo': thing})
        self.assertTrue(thing.add_to_class.called)
        thing.add_to_class.assert_called_once_with(model, b'foo')

    def test_regular_attribute(self):
        model = ModelType.__new__(ModelType, str(b'SomeModel'), (
         Model,), {b'__module__': b'foo', b'foo': b'bar'})
        self.assertTrue(hasattr(model, b'foo'))
        self.assertEqual(model.foo, b'bar')


class TestModels(unittest.TestCase):

    class Friend(Model):
        name = CharField()
        age = IntegerField()
        surname = CharField(source=b'last_name')

    class Entity(Model):
        id = IntegerField(required=True, allow_null=False)
        first_name = CharField(source=b'name')
        tags = ListField(source=b'foo.tags')

    def setUp(self):
        self.data = {b'id': 1, 
           b'name': b'larry', 
           b'url': b'google.com', 
           b'foo': {b'bar': 2, 
                    b'tags': [
                            b'cool', b'easy']}, 
           b'friends': [{b'name': b'bob', b'age': 24}, {b'name': b'alice', b'age': None, b'last_name': b'secret'}]}
        return

    def test_meta_fields_order(self):
        self.assertEqual(self.Friend.meta.field_names, [b'name', b'age', b'surname'])
        self.assertEqual(self.Entity.meta.field_names, [b'id', b'first_name', b'tags'])

    def test_meta_fields_order_inheritance(self):

        class Person(self.Entity):
            friends = ListField(child=ModelField(self.Friend))

        self.assertEqual(Person.meta.field_names, [
         b'id', b'first_name', b'tags', b'friends'])

    def test_init_with_data(self):
        with mock.patch.object(self.Entity, b'unpack') as (unpack):
            self.Entity(self.data)
            self.assertTrue(unpack.called)
            unpack.assert_called_once_with(self.data)

    def test_init_with_valid_kwargs(self):
        entity = self.Entity(first_name=b'bob')
        self.assertEqual(entity.first_name, b'bob')

    def test_init_with_invalid_kwargs(self):
        self.assertRaises(ValueError, self.Entity, foo=b'bar')

    def test_unpack(self):
        entity = self.Entity()
        entity.unpack(self.data)
        self.assertEqual(entity.first_name, b'larry')
        self.assertEqual(entity.id, 1)
        self.assertEqual(entity.tags, [b'cool', b'easy'])

    def test_str(self):
        entity = self.Entity(id=10)
        self.assertEqual(str(entity), b'10')
        entity = self.Entity()
        self.assertEqual(str(entity), b'None')

    def test_repr(self):
        entity = self.Entity(id=10)
        self.assertEqual(repr(entity), b'<Entity: 10>')


class TestFieldOptions(unittest.TestCase):

    def test_init_with_valid_kwargs(self):
        options = FieldOptions(None, random=True)
        self.assertTrue(options.random)
        return

    def test_init_with_invalid_kwargs(self):
        self.assertRaises(ImproperlyConfigured, FieldOptions, None, _foo=b'bar')
        return

    def test_raises_on_invalid_source(self):
        self.assertRaises(ImproperlyConfigured, FieldOptions, None, source=1)
        return

    def test_raises_on_invalid_delimiter(self):
        self.assertRaises(ImproperlyConfigured, FieldOptions, None, delimiter=1)
        return

    def test_raises_on_invalid_child(self):
        self.assertRaises(ImproperlyConfigured, FieldOptions, None, child=1)
        return

    def test_raises_on_invalid_model(self):
        self.assertRaises(ImproperlyConfigured, FieldOptions, None, model=1)
        return


class TestFields(unittest.TestCase):

    def setUp(self):
        self.field.__dict__.pop(b'path', None)
        return

    class CustomField(Field):
        pass

    model = mock.MagicMock()
    model.__name__ = b'model'
    field = CustomField()
    field.name = b'foo'
    field.model = model

    def test_options_namespacing_of_kwargs(self):
        self.assertIsNotNone(self.field._idx)

    def test_clean(self):
        value = mock.MagicMock()
        self.assertEqual(self.field.clean(value), value)

    def test_clone(self):
        clone = self.field.clone()
        self.assertIsInstance(clone, self.CustomField)
        self.assertFalse(clone is self.field)

    def test_add_to_class_hits_clone(self):
        with mock.patch.object(self.field, b'clone') as (clone):
            self.field.add_to_class(mock.MagicMock(), b'foo')
            self.assertTrue(clone.called)

    def test_add_to_class_hits_model_meta_add_field(self):
        with mock.patch.object(self.field, b'clone') as (clone):
            model = mock.MagicMock()
            self.field.add_to_class(model, b'foo')
            self.assertTrue(model.meta.add_field.called)
            model.meta.add_field.assert_called_once_with(clone.return_value)

    def test_parse_hits_traverse_path(self):
        with mock.patch.object(self.field, b'traverse_path') as (traverse_path):
            value = mock.MagicMock()
            output = self.field.parse(value)
            self.assertTrue(traverse_path.called)
            self.assertEqual(output, traverse_path.return_value)

    def test_parse_raises_FieldError_on_allow_null_False(self):
        self.field.options.allow_null = False
        with mock.patch.object(self.field, b'traverse_path') as (traverse_path):
            traverse_path.return_value = None
            self.assertRaises(FieldError, self.field.parse, None)
        self.field.options.allow_null = True
        return

    def test_parse_raises_when_not_found_and_required(self):
        self.field.options.required = True
        with mock.patch.object(self.field, b'traverse_path') as (traverse_path):
            traverse_path.return_value = NOT_FOUND
            self.assertRaises(FieldError, self.field.parse, None)
        self.field.options.required = False
        return

    def test_parse_returns_default_when_not_found_and_not_required(self):
        with mock.patch.object(self.field, b'traverse_path') as (traverse_path):
            traverse_path.return_value = NOT_FOUND
            self.assertEqual(self.field.parse(mock.MagicMock()), self.field.default)

    def test_parse_returns_None_when_null_value_is_found_and_is_allowed(self):
        with mock.patch.object(self.field, b'traverse_path') as (traverse_path):
            traverse_path.return_value = None
            self.assertEqual(self.field.parse(mock.MagicMock()), None)
        return

    def test_parse_hits_run_validators_when_non_None_value_is_found(self):
        with mock.patch.object(self.field, b'traverse_path') as (traverse_path):
            with mock.patch.object(self.field, b'run_validators') as (run_validators):
                value = mock.MagicMock()
                self.field.parse(value)
                self.assertTrue(run_validators.called)
                run_validators.assert_called_once_with(traverse_path.return_value)

    def test_parse_hits_clean_when_non_None_value_is_found(self):
        with mock.patch.object(self.field, b'traverse_path') as (traverse_path):
            with mock.patch.object(self.field, b'clean') as (clean):
                value = mock.MagicMock()
                self.field.parse(value)
                self.assertTrue(clean.called)
                clean.assert_called_once_with(traverse_path.return_value)

    def test_path_is_name_when_source_is_None(self):
        self.assertEqual(self.field.get_path(), [self.field.name])

    def test_path_is_empty_when_source_and_name_are_None(self):
        self.field.name = None
        self.assertEqual(self.field.get_path(), [])
        self.field.name = b'foo'
        return

    def test_path_is_cached(self):
        with mock.patch.object(self.field, b'get_path') as (get_path):
            self.assertEqual(self.field.path, get_path.return_value)
            self.assertTrue(get_path.called)
            self.assertEqual(get_path.call_count, 1)
            self.field.path
            self.assertEqual(get_path.call_count, 1)

    def test_path_on_source(self):
        self.field.options.source = b'some.dot.path'
        self.assertEqual(self.field.get_path(), [b'some', b'dot', b'path'])

    def test_default_on_callable(self):
        self.field.options.default = dict
        default = self.field.default
        self.assertIsInstance(default, dict)
        self.assertFalse(self.field.default is default)
        self.field.options.default = None
        return

    def test_default_on_constant(self):
        self.field.options.default = b'hello'
        self.assertEqual(self.field.default, b'hello')
        self.field.options.default = None
        return

    def test_traverse_path_on_inconsistent_data(self):
        self.field.options.source = b'foo.bar'
        self.assertRaises(FieldError, self.field.traverse_path, {b'foo': 1})
        self.field.options.source = None
        return

    def test_traverse_path_on_valid_path(self):
        self.field.options.source = b'foo.bar'
        self.assertEqual(self.field.traverse_path({b'foo': {b'bar': 1}}), 1)
        self.field.options.source = None
        return

    def test_traverse_path_on_incomplete_data(self):
        self.field.options.source = b'foo.bar'
        self.assertEqual(self.field.traverse_path({b'foo': {b'baz': 1}}), NOT_FOUND)
        self.field.options.source = None
        return

    def test_traverse_path_on_null_value(self):
        self.field.options.source = b'foo.bar'
        self.assertEqual(self.field.traverse_path({b'foo': None}), None)
        self.field.options.source = None
        return

    def test_run_validators_both_options_and_core_hit(self):

        def side_effect(value):
            return value

        fake_validator1 = mock.MagicMock(side_effect=side_effect)
        fake_validator2 = mock.MagicMock(side_effect=side_effect)
        self.field.validators = (fake_validator1,)
        self.field.options.validators = (fake_validator2,)
        self.field.run_validators(None)
        self.assertTrue(fake_validator1.called)
        fake_validator1.assert_called_once_with(None)
        self.assertTrue(fake_validator2.called)
        fake_validator2.assert_called_once_with(None)
        return

    def test_str(self):
        self.assertEqual(str(self.field), b'model.foo')

    def test_repr(self):
        self.assertEqual(repr(self.field), b'<CustomField: model.foo>')

    def test_ListField_parse_calls_child_parse(self):
        field = ListField(child=CharField())
        with mock.patch.object(field.options.child, b'parse') as (parse):
            field.parse([b'foo', b'bar'])
            self.assertTrue(parse.called)
            self.assertEqual(parse.call_count, 2)
            parse.assert_called_with(b'bar')
            parse.assert_any_call(b'foo')

    def test_ModelField_parse_returns_instance_of_model(self):

        class TestModel(Model):
            foo = CharField()

        field = ModelField(TestModel)
        value = field.parse({b'foo': b'bar'})
        self.assertIsInstance(value, TestModel)
        self.assertEqual(value.foo, b'bar')

    def test_IntegerField_validators(self):
        field = IntegerField()
        self.assertRaises(ValidationError, field.run_validators, None)
        self.assertEqual(field.run_validators(1), None)
        return

    def test_IntegerField_clean_coerces_int(self):
        field = IntegerField()
        self.assertEqual(field.clean(b'1'), 1)

    def test_CharField_validators(self):
        field = CharField()
        self.assertRaises(ValidationError, field.run_validators, None)
        self.assertEqual(field.run_validators(b'foo'), None)
        return

    def test_BooleanField_validators(self):
        field = BooleanField()
        self.assertRaises(ValidationError, field.run_validators, None)
        self.assertEqual(field.run_validators(False), None)
        return


if __name__ == b'__main__':
    unittest.main()
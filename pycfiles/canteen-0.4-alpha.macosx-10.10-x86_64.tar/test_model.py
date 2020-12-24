# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_model/test_model.py
# Compiled at: 2014-09-30 20:17:12
"""

  model tests
  ~~~~~~~~~~~

  tests canteen's model classes.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
import abc, json, inspect
try:
    import config
    _APPCONFIG = True
except ImportError as e:
    _APPCONFIG = False

class Config(object):
    config = {}
    debug = True


config = Config()
config.config = {}
if 'canteen.model' not in config.config:
    config.config['canteen.model'] = {}
config.config['canteen.model']['debug'] = True
for k in filter(lambda x: x.startswith('canteen.model'), config.config.iterkeys()):
    config.config[k]['debug'] = True

from canteen import model, core
from canteen.model import adapter
from canteen.model import exceptions
from canteen.test import FrameworkTest
from canteen.util import struct as datastructures

class TestCar(model.Model):
    """ An automobile. """
    make = (
     basestring, {'indexed': True})
    model = (basestring, {'indexed': True})
    year = (int, {'choices': xrange(1900, 2015)})
    color = (basestring,
     {'choices': ('blue', 'green', 'red', 'silver', 'white', 'black')})


class TestPerson(model.Vertex):
    """ A human being. """
    firstname = (
     basestring, {'indexed': True})
    lastname = (basestring, {'indexed': True})
    active = (bool, {'default': True})
    cars = (TestCar, {'repeated': True})
    cars_ref = (model.Key, {'repeated': True})
    cars_embedded = (TestCar, {'repeated': True, 'embedded': True})


class Friendship(TestPerson > TestPerson):
    """ A friendship between people. """
    year_met = int


class ModelTests(FrameworkTest):
    """ Tests `model.Model` and `model.AbstractModel`. """

    def test_construct_model(self):
        """ Test constructing a `Model` manually """
        car = TestCar(make='BMW', model='M3', year=2013, color='white')
        person = TestPerson()
        person.firstname = 'John'
        person.cars = [car]
        self.assertIsInstance(car, TestCar)
        self.assertIsInstance(person, TestPerson)
        self.assertEqual(person.firstname, 'John')
        self.assertIsInstance(person.cars, list)
        self.assertEqual(len(person.cars), 1)
        self.assertIsInstance(person.cars[0], TestCar)
        self.assertEqual(person.active, True)
        self.assertEqual(person.lastname, None)
        cls = str(TestPerson)
        obj = str(person)
        self.assertTrue('Person' in cls)
        self.assertTrue('lastname' in cls)
        self.assertTrue('firstname' in cls)
        self.assertTrue('Person' in obj)
        self.assertTrue('lastname' in obj)
        self.assertTrue('firstname' in obj)
        self.assertTrue('John' in obj)
        return

    def test_invalid_model_adapter(self):
        """ Test using invalid model adapter, which should raise `RuntimeError` """
        with self.assertRaises(RuntimeError):

            class InvalidAdapterModel(model.Model):
                __adapter__ = 'DumbInvalidModelAdapter'
                prop1 = basestring

    def test_model_inheritance(self):
        """ Test proper inheritance structure for `Model` """
        self.assertTrue(issubclass(TestCar, model.Model))
        self.assertTrue(issubclass(TestPerson, model.Model))
        self.assertTrue(issubclass(model.Model, model.AbstractModel))

    def test_model_schema(self):
        """ Test that there's a proper schema spec on `Model` """
        self.assertTrue(hasattr(TestPerson, '__lookup__'))
        self.assertIsInstance(TestPerson.__lookup__, frozenset)
        self.assertTrue(hasattr(TestPerson, 'firstname'))
        self.assertTrue(hasattr(TestPerson, 'lastname'))
        self.assertTrue(hasattr(TestPerson, 'cars'))
        self.assertTrue(hasattr(TestPerson, 'kind'))
        self.assertIsInstance(TestPerson.kind(), basestring)
        self.assertTrue(hasattr(TestPerson, '_get_value'))
        self.assertTrue(hasattr(TestPerson, '_set_value'))
        self.assertTrue(inspect.ismethod(TestPerson._get_value))
        self.assertTrue(inspect.ismethod(TestPerson._set_value))
        self.assertTrue(hasattr(TestPerson, 'key'))
        self.assertTrue(hasattr(TestPerson(), '__key__'))
        self.assertTrue(not hasattr(TestPerson, '__key__'))

    def test_model_set_attribute(self):
        """ Test setting an unknown and known attribute on `Model` """
        john = TestPerson(firstname='John')
        self.assertEqual(john.firstname, 'John')
        john.firstname = 'Blabs'
        self.assertEqual(john.firstname, 'Blabs')
        with self.assertRaises(AttributeError):
            john.blabs = 'John'

    def test_model_adapter(self):
        """ Test that adapter is attached correctly to `Model` """
        self.assertTrue(hasattr(TestPerson, '__adapter__'))
        self.assertIsInstance(TestPerson.__adapter__, adapter.ModelAdapter)

    def test_model_stringify(self):
        """ Test the string representation of a `Model` object """
        self.assertIsInstance(TestPerson().__repr__(), basestring)

    def test_model_kind(self):
        """ Test that `Model.kind` is properly set """
        self.assertIsInstance(TestPerson.kind(), basestring)
        self.assertEqual(TestPerson.kind(), 'TestPerson')
        john = TestPerson()
        self.assertIsInstance(john.kind(), basestring)
        self.assertEqual(john.kind(), 'TestPerson')

    def test_abstract_model(self):
        """ Test that `AbstractModel` works abstractly """
        self.assertTrue(not isinstance(model.Model, abc.ABCMeta))
        with self.assertRaises(exceptions.AbstractConstructionFailure):
            model.AbstractModel()

    def test_concrete_model(self):
        """ Test that `Model` works concretely """
        self.assertIsInstance(TestPerson(), TestPerson)

        class SampleTestModel(model.Model):
            """ Test parent model class. """
            parent = basestring

        class SampleSubModel(SampleTestModel):
            """ Test child model class. """
            child = basestring

        self.assertTrue(hasattr(SampleTestModel, 'parent'))
        self.assertTrue(not hasattr(SampleTestModel, 'child'))
        self.assertTrue(hasattr(SampleSubModel, 'child'))
        self.assertTrue(hasattr(SampleSubModel, 'parent'))
        self.assertIsInstance(SampleTestModel(), model.Model)
        self.assertIsInstance(SampleSubModel(), SampleTestModel)
        self.assertIsInstance(SampleSubModel(), model.Model)

    def test_model_to_dict(self, method='to_dict'):
        """ Test flattening a `Model` into a raw dictionary """
        p = TestPerson(firstname='John')
        raw_dict = getattr(p, method)()
        if method == 'to_dict':
            self.assertEqual(len(raw_dict), 2)
            self.assertIsInstance(raw_dict, dict)
            self.assertEqual(raw_dict['firstname'], 'John')
            self.assertEqual(raw_dict['active'], True)
            with self.assertRaises(KeyError):
                raw_dict['lastname']
        return raw_dict

    def test_model_update_with_dict(self):
        """ Test updating a `Model` from a `dict` """
        p = TestPerson(firstname='John')
        update = {'firstname': 'Sup', 
           'lastname': 'Bleebs'}
        p.update(update)
        assert p.firstname == 'Sup'
        assert p.lastname == 'Bleebs'

    def test_model_to_dict_schema(self):
        """ Test flattening a `Model` class into a schema dictionary """
        schema = TestPerson.to_dict_schema()
        assert 'firstname' in schema
        assert isinstance(schema['firstname'], model.Property)
        assert schema['firstname']._basetype == basestring

    def test_model_to_dict_all_arguments(self, method='to_dict'):
        """ Test using `Model.to_dict` with the `all` flag """
        p = TestPerson(firstname='John')
        all_dict = getattr(p, method)(_all=True)
        if method == 'to_dict':
            self.assertEqual(len(all_dict), len(p.__lookup__))
            self.assertEqual(all_dict['firstname'], 'John')
            self.assertEqual(all_dict['lastname'], None)
            self.assertEqual(all_dict['active'], True)
        return all_dict

    def test_model_to_dict_with_filter(self, method='to_dict'):
        """ Test using `Model.to_dict` with a filter function """
        p = TestPerson(firstname='John')
        filtered_dict = getattr(p, method)(filter=lambda x: len(x[0]) > 7)
        if method == 'to_dict':
            self.assertEqual(len(filtered_dict), 1)
            self.assertIsInstance(filtered_dict, dict)
            self.assertEqual(filtered_dict['firstname'], 'John')
            with self.assertRaises(KeyError):
                filtered_dict['active']
        return filtered_dict

    def test_model_to_dict_with_include(self, method='to_dict'):
        """ Test using `Model.to_dict` with an inclusion list """
        p = TestPerson(firstname='John')
        included_dict = getattr(p, method)(include=('firstname', 'lastname'))
        if method == 'to_dict':
            self.assertEqual(len(included_dict), 2)
            self.assertIsInstance(included_dict, dict)
            self.assertEqual(included_dict['firstname'], 'John')
            self.assertEqual(included_dict['lastname'], None)
            with self.assertRaises(KeyError):
                included_dict['active']
        return included_dict

    def test_model_to_dict_with_exclude(self, method='to_dict'):
        """ Test using `Model.to_dict` with an exclusion list """
        p = TestPerson(firstname='John')
        excluded_dict = getattr(p, method)(exclude=('active', ))
        if method == 'to_dict':
            self.assertEqual(len(excluded_dict), 1)
            self.assertIsInstance(excluded_dict, dict)
            self.assertEqual(excluded_dict['firstname'], 'John')
            with self.assertRaises(KeyError):
                excluded_dict['active']
        return excluded_dict

    def test_model_to_dict_with_map(self, method='to_dict'):
        """ Test using `Model.to_dict` with a map function """
        p = TestPerson(firstname='John')
        mapped_dict = getattr(p, method)(map=lambda x: tuple([x[0] + '-cool', x[1]]))
        if method == 'to_dict':
            self.assertEqual(len(mapped_dict), 2)
            self.assertIsInstance(mapped_dict, dict)
            self.assertEqual(mapped_dict['firstname-cool'], 'John')
            self.assertEqual(mapped_dict['active-cool'], True)
        return mapped_dict

    def test_model_to_dict_convert_keys(self):
        """ Test flattening a `Model` instance with key references to a dict """
        p = TestPerson(key=model.Key(TestPerson, 'john'), firstname='John', lastname='Doe')
        bmw = TestCar(key=model.Key(TestCar, 'bmw'), make='BMW', model='M3', color='white', year=1998)
        civic = TestCar(key=model.Key(TestCar, 'civic'), make='Honda', model='Civic', color='black', year=2001)
        p.cars_ref = (
         bmw.key, civic.key)
        _john_raw = p.to_dict(convert_keys=False)
        _john_converted = p.to_dict(convert_keys=True)
        assert bmw.key in _john_raw['cars_ref'], "expected key for car `BMW` but found none in object: '%s'." % _john_raw
        assert civic.key in _john_raw['cars_ref'], "expected key for car `civic` but found none in object: '%s'." % _john_raw
        assert bmw.key.urlsafe() in _john_converted['cars_ref'], "expected converted key for car `BMW` but found none in object: '%s'." % _john_converted
        assert civic.key.urlsafe() in _john_converted['cars_ref'], "expected converted key for car `civic` but found none in object: '%s'." % _john_converted

    def test_model_to_dict_convert_models(self):
        """ Test flattening a `Model` instance with submodels to a dict """
        p = TestPerson(key=model.Key(TestPerson, 'john'), firstname='John', lastname='Doe')
        bmw = TestCar(key=model.Key(TestCar, 'bmw'), make='BMW', model='M3', color='white', year=1998)
        civic = TestCar(key=model.Key(TestCar, 'civic'), make='Honda', model='Civic', color='black', year=2001)
        p.cars_ref = (
         bmw.key, civic.key)
        p.cars_embedded = (bmw, civic)
        _john_raw = p.to_dict(convert_keys=False, convert_models=False)
        _john_converted = p.to_dict(convert_keys=True, convert_models=True)
        assert bmw in _john_raw['cars_embedded'], "expected object for car `BMW` but found none in object: '%s'." % _john_raw
        assert civic in _john_raw['cars_embedded'], "expected object for car `civic` but found none in object: '%s'." % _john_raw
        assert bmw.key in _john_raw['cars_ref'], "expected key for car `BMW` but found none in object: '%s'." % _john_raw
        assert civic.key in _john_raw['cars_ref'], "expected key for car `civic` but found none in object: '%s'." % _john_raw
        assert bmw.key.urlsafe() in _john_converted['cars_ref'], "expected converted key for car `BMW` but found none in object: '%s'." % _john_converted
        assert civic.key.urlsafe() in _john_converted['cars_ref'], "expected converted key for car `civic` but found none in object: '%s'." % _john_converted
        assert len(_john_converted['cars_embedded']) == 2
        for i in _john_converted['cars_embedded']:
            assert isinstance(i, dict), 'submodels are expected to convert to dicts when `convert_models` is active'

    def test_JSON_model_format(self):
        """ Test serializing a `Model` into a JSON struct """
        p = TestPerson(firstname='John', lastname='Doe')

        def test_json_flow(original, js=None):
            if not js:
                original, js = original('to_dict'), original('to_json')
            self.assertTrue(len(js) > 0)
            self.assertIsInstance(js, basestring)
            decoded = json.loads(js)
            self.assertIsInstance(decoded, dict)
            self.assertEqual(len(original), len(decoded))
            for key in original:
                self.assertEqual(original[key], decoded[key])

        test_json_flow(p.to_dict(), p.to_json())
        test_structs = {'raw_dict': self.test_model_to_dict, 
           'all_dict': self.test_model_to_dict_all_arguments, 
           'mapped_dict': self.test_model_to_dict_with_map, 
           'filtered_dict': self.test_model_to_dict_with_filter, 
           'included_dict': self.test_model_to_dict_with_include, 
           'excluded_dict': self.test_model_to_dict_with_exclude}
        test_json_flow(test_structs['raw_dict'])
        test_json_flow(test_structs['all_dict'])
        test_json_flow(test_structs['mapped_dict'])
        test_json_flow(test_structs['filtered_dict'])
        test_json_flow(test_structs['included_dict'])
        test_json_flow(test_structs['excluded_dict'])
        return

    def test_inflate_model_from_json(self):
        """ Test inflating a `Model` object from a JSON string """
        obj = {'firstname': 'John', 'lastname': 'Doe'}
        json_string = json.dumps(obj)
        p = TestPerson.from_json(json_string)
        assert p.firstname == 'John'
        assert p.lastname == 'Doe'

    with core.Library('msgpack') as (library, msgpack):
        import msgpack

        def test_msgpack_model_format(self):
            """ Test serializing a `Model` into a msgpack struct """
            p = TestPerson(firstname='John', lastname='Doe')

            def test_msgpack_flow(original, mp=None):
                if not mp:
                    original, mp = original('to_dict'), original('to_msgpack')
                self.assertTrue(len(mp) > 0)
                self.assertIsInstance(mp, basestring)
                decoded = self.msgpack.unpackb(mp)
                self.assertIsInstance(decoded, dict)
                self.assertEqual(len(original), len(decoded))
                for key in original:
                    self.assertEqual(original[key], decoded[key])

            test_msgpack_flow(p.to_dict(), p.to_msgpack())
            test_structs = {'raw_dict': self.test_model_to_dict, 
               'all_dict': self.test_model_to_dict_all_arguments, 
               'mapped_dict': self.test_model_to_dict_with_map, 
               'filtered_dict': self.test_model_to_dict_with_filter, 
               'included_dict': self.test_model_to_dict_with_include, 
               'excluded_dict': self.test_model_to_dict_with_exclude}
            test_msgpack_flow(test_structs['raw_dict'])
            test_msgpack_flow(test_structs['all_dict'])
            test_msgpack_flow(test_structs['mapped_dict'])
            test_msgpack_flow(test_structs['filtered_dict'])
            test_msgpack_flow(test_structs['included_dict'])
            test_msgpack_flow(test_structs['excluded_dict'])
            return

        def test_inflate_model_from_msgpack(self):
            """ Test inflating a `Model` object from a msgpack payload """
            obj = {'firstname': 'John', 'lastname': 'Doe'}
            mpack = self.msgpack.dumps(obj)
            p = TestPerson.from_msgpack(mpack)
            assert p.firstname == 'John'
            assert p.lastname == 'Doe'

    def test_explicit(self):
        """ Test a `Model`'s behavior in `explicit` mode """
        s = TestPerson(firstname='Sam')
        p = TestPerson(firstname='John')
        self.assertEqual(p.__explicit__, False)
        explicit_firstname, explicit_lastname, explicit_active = (None, None, None)
        with p:
            explicit_firstname, explicit_lastname, explicit_active = p.firstname, p.lastname, p.active
            self.assertNotEqual(p.__explicit__, s.__explicit__)
            self.assertEqual(s.lastname, None)
            self.assertEqual(s.active, True)
            self.assertEqual(s.firstname, 'Sam')
            self.assertEqual(p.__explicit__, True)
        self.assertEqual(p.__explicit__, False)
        self.assertEqual(explicit_firstname, 'John')
        self.assertEqual(explicit_active, datastructures.EMPTY)
        self.assertEqual(explicit_lastname, datastructures.EMPTY)
        self.assertEqual(p.firstname, 'John')
        self.assertEqual(p.lastname, None)
        self.assertEqual(p.active, True)
        return

    def test_generator_implicit(self):
        """ Test a `Model`'s behavior when used as an iterator """
        p = TestPerson(firstname='John')
        items = {}
        for name, value in p:
            items[name] = value

        self.assertEqual(len(items), 2)
        self.assertEqual(items['firstname'], 'John')
        self.assertEqual(items['active'], True)

    def test_generator_explicit(self):
        """ Test `Model` behavior when used as an iterator in `explicit` mode """
        p = TestPerson(firstname='John')
        items = {}
        with p:
            for name, value in p:
                items[name] = value

        self.assertEqual(len(items), len(p.__lookup__))
        self.assertEqual(items['firstname'], 'John')
        self.assertEqual(items['active'], datastructures.EMPTY)
        self.assertEqual(items['lastname'], datastructures.EMPTY)

    def test_len(self):
        """ Test a `Model`'s behavior when used with `len()` """
        p = TestPerson()
        self.assertEqual(len(p), 0)
        p.firstname = 'John'
        self.assertEqual(len(p), 1)
        p.lastname = 'Doe'
        self.assertEqual(len(p), 2)

    def test_nonzero(self):
        """ Test a `Model`'s falsyness with no properties """
        p = TestPerson()
        self.assertTrue(not p)
        p.firstname = 'John'
        self.assertTrue(p)

    def test_get_invalid_property(self):
        """ Test getting an invalid `Model` property """
        p = TestPerson()
        with self.assertRaises(AttributeError):
            p.blabble
        with self.assertRaises(AttributeError):
            TestPerson.blabble
        with self.assertRaises(AttributeError):
            p._get_value('blabble')

    def test_get_value_all_properties(self):
        """ Test getting *all* properties via `_get_value` """
        p = TestPerson(firstname='John', lastname='Doe')
        properties = p._get_value(None)
        self.assertEqual(len(properties), 6)
        self.assertIsInstance(properties, list)
        self.assertIsInstance(properties[0], tuple)
        for k, v in properties:
            self.assertEqual(v, getattr(p, k))

        return

    def test_model_getitem_setitem(self):
        """ Test a `Model`'s compliance with Python's Item API """
        p = TestPerson(firstname='John')
        self.assertEqual(p.firstname, 'John')
        self.assertEqual(p['firstname'], 'John')
        p['lastname'] = 'Gammon'
        self.assertEqual(p.lastname, 'Gammon')
        with self.assertRaises(KeyError):
            p['invalidproperty']
        with self.assertRaises(AttributeError):
            p.invalidproperty

    def test_model_setvalue(self):
        """ Test protected method `_set_value`, which is used by model internals """
        p = TestPerson(firstname='John')
        x = p._set_value('key', model.VertexKey(TestPerson, 'john'))
        self.assertEqual(x, p)
        with self.assertRaises(AttributeError):
            p._set_value('invalidproperty', 'value')
        with self.assertRaises(AttributeError):
            TestPerson.__dict__['firstname'].__set__(None, 'invalid')
        return

    def test_model_setkey(self):
        """ Test protected method `_set_key`, which is used by model internals """
        p = TestPerson(firstname='John')
        with self.assertRaises(TypeError):
            p._set_key(5.5)
        k = model.VertexKey(TestPerson, 'john')
        p._set_key(urlsafe=k.urlsafe())
        p._set_key(raw=k.flatten(False)[1])
        p._set_key(constructed=k)
        with self.assertRaises(TypeError):
            p._set_key(k, urlsafe=k.urlsafe())
        with self.assertRaises(TypeError):
            p._set_key(urlsafe=k.urlsafe(), raw=k.flatten(False)[1])
        with self.assertRaises(TypeError):
            p._set_key(None)
        return

    def test_early_mutate(self):
        """ Test setting attributes and items on a model before it's ready """

        class EarlyMutateModel(model.Model):
            """ Tests mutation of properties before instantiation. """
            string = basestring

        with self.assertRaises(AttributeError):
            EarlyMutateModel.string = 'testing123'
        with self.assertRaises(AttributeError):
            EarlyMutateModel.newprop = 'newvalue'
        EarlyMutateModel.__impl__ = {}

    def test_validation_of_required_properties(self):
        """ Test validation of required properties """

        class RequiredPropertyModel(model.Model):
            """ Tests required properties. """
            nonrequired = basestring
            required = (basestring, {'required': True})

        p = RequiredPropertyModel(nonrequired='sup')
        with self.assertRaises(ValueError):
            p.put()
        p.required = 'sup'
        p.put()

    def test_validation_of_property_basetype(self):
        """ Test validation of property basetypes """

        class BasetypedPropertyModel(model.Model):
            """ Tests property basetypes. """
            string = basestring
            number = int
            floating = float
            boolean = bool
            always_empty = basestring

        b = BasetypedPropertyModel()
        b.string = 5
        with self.assertRaises(ValueError):
            b.put()
        b.string = 'sample'
        b.number = '5'
        with self.assertRaises(ValueError):
            b.put()
        b.number = 5
        b.floating = 5
        with self.assertRaises(ValueError):
            b.put()
        b.floating = 5.5
        b.boolean = 5.5
        with self.assertRaises(ValueError):
            b.put()
        b.boolean = True
        b.put()

    def test_validation_of_repeated_properties(self):
        """ Test validation of repeated properties """

        class RepeatedPropertyModel(model.Model):
            """ Tests repeated properties. """
            nonrepeated = basestring
            repeated = (int, {'repeated': True})

        r = RepeatedPropertyModel(nonrepeated=['blabble', '1', '2', '3'])
        with self.assertRaises(ValueError):
            r.put()
        r.nonrepeated = 'validvalue'
        r.repeated = 5
        with self.assertRaises(ValueError):
            r.put()
        r.repeated = [
         'one', 'two', 'three']
        with self.assertRaises(ValueError):
            r.put()
        r.repeated = [
         1, 2, 3]
        r.put()

    def test_class_level_default_value(self):
        """ Test reading a property with a default set at the class level """

        class ClassDefaultSample(model.Model):
            """ Tests properties with default values at the class level. """
            sample_default = (
             basestring, {'default': 'Hello, default!'})

        self.assertIsInstance(ClassDefaultSample.sample_default, model.Property)

    def test_class_level_propery_access(self):
        """ Test class-level property access on `Model` subclasses """
        assert isinstance(TestCar.make, model.Property)
        assert 'make' in TestCar.make.__repr__()
        assert 'Property' in TestCar.make.__repr__()

    def test_class_level_item_access(self):
        """ Test class-level item access on `Model` subclasses """
        assert isinstance(TestCar['make'], model.Property)
        assert 'make' in TestCar['make'].__repr__()
        assert 'Property' in TestCar['make'].__repr__()

    def test_graph_class_existence(self):
        """ Test proper export of ``Vertex`` and ``Edge`` models """
        assert hasattr(model, 'Vertex')
        assert hasattr(model, 'Edge')
        assert issubclass(model.Vertex, model.Model)
        assert issubclass(model.Edge, model.Model)

    def test_vertex_class_mro(self):
        """ Test proper MRO for ``Vertex`` models """
        assert hasattr(TestPerson, 'edges')
        assert hasattr(TestPerson(), 'edges')
        assert hasattr(TestPerson, 'neighbors')
        assert hasattr(TestPerson(), 'neighbors')
        assert issubclass(TestPerson, model.Vertex)
        assert isinstance(TestPerson(), model.Vertex)

    def test_edge_class_mro(self):
        """ Test proper MRO for ``Edge`` models """
        assert hasattr(Friendship, 'peers')
        assert issubclass(Friendship, model.Edge)
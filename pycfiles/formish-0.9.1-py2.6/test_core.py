# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/tests/unittests/test_core.py
# Compiled at: 2010-03-01 05:16:45
import formish, unittest, schemaish
from dottedish.api import dotted, unflatten
from formish.forms import validation
from webob.multidict import MultiDict
import validatish

class DummyObject(object):
    pass


class Request(object):
    headers = {'content-type': 'text/html'}

    def __init__(self, form_name='form', POST=None, GET=None, method='POST'):
        self.GET = MultiDict(GET or {})
        self.POST = MultiDict(POST or {})
        getattr(self, method.upper())['__formish_form__'] = form_name
        self.method = method

    def get_post(self):

        def container_factory(parent_key, item_key):
            if item_key.isdigit():
                return []
            return {}

        return unflatten(self.POST.dict_of_lists().iteritems(), container_factory=container_factory)


class TestFormBuilding(unittest.TestCase):
    """Build a Form and test that it doesn't raise exceptions on build and that the methods/properties are as expected"""

    def test_form(self):
        """Test empty form construction """
        schema_empty = schemaish.Structure()
        name = 'Empty Form'
        form = formish.Form(schema_empty, name)
        self.assertEqual(form.structure.attr, schema_empty)
        self.assertEqual(form.name, name)
        assert list(form.fields) == []

    def test_readonly_field(self):
        """Test a form that has no a read only field"""
        schema_readonly = schemaish.Structure([('a', schemaish.String()), ('b', schemaish.String())])
        name = 'Flat Form'
        request = Request(name)
        form = formish.Form(schema_readonly, name)
        form['a'].widget = formish.Input(readonly=True)
        request = Request(name, {'b': 'bar'})
        actualdata = form.validate(request)
        expecteddata = {'a': None, 'b': 'bar'}
        assert actualdata == expecteddata
        form.defaults = {'a': 'foo'}
        actualdata = form.validate(request)
        expecteddata = {'a': 'foo', 'b': 'bar'}
        assert actualdata == expecteddata
        form()
        return

    def test_flat_form(self):
        """Test a form that has no nested sections """
        schema_flat = schemaish.Structure([('a', schemaish.String()), ('b', schemaish.String())])
        name = 'Flat Form'
        form = formish.Form(schema_flat, name)
        assert form.structure.attr is schema_flat
        assert len(list(form.fields)) is 2

    def test_nested_form(self):
        """Test a form two nested levels"""
        one = schemaish.Structure([('a', schemaish.String()), ('b', schemaish.String())])
        two = schemaish.Structure([('a', schemaish.String()), ('b', schemaish.String())])
        schema_nested = schemaish.Structure([('one', one), ('two', two)])
        name = 'Nested Form One'
        form = formish.Form(schema_nested, name)
        assert form.structure.attr is schema_nested
        assert len(list(form.fields)) == 2

    def test_nested_form_validation_errors(self):
        schema_nested = schemaish.Structure([
         (
          'one',
          schemaish.Structure([
           (
            'a', schemaish.String(validator=validatish.Required())),
           (
            'b', schemaish.String()),
           (
            'c', schemaish.Structure([('x', schemaish.String()), ('y', schemaish.String())]))]))])
        name = 'Nested Form Two'
        form = formish.Form(schema_nested, name)
        r = {'one.a': '', 'one.b': '', 'one.c.x': '', 'one.c.y': ''}
        request = Request(name, r)
        self.assertRaises(formish.FormError, form.validate, request)
        self.assert_(form.errors['one.a'], 'is_required')

    def test_nested_form_validation_output(self):
        schema_nested = schemaish.Structure([
         (
          'one',
          schemaish.Structure([
           (
            'a', schemaish.String(validator=validatish.Required())),
           (
            'b', schemaish.String()),
           (
            'c', schemaish.Structure([('x', schemaish.String()), ('y', schemaish.String())]))]))])
        name = 'Nested Form two'
        form = formish.Form(schema_nested, name)
        request = Request(name, {'one.a': 'woot!', 'one.b': '', 'one.c.x': '', 'one.c.y': ''})
        expected = {'one': {'a': 'woot!', 'b': None, 'c': {'x': None, 'y': None}}}
        self.assert_(form.validate(request) == expected)
        self.assertEquals(form.errors, {})
        return

    def test_integer_type(self):
        schema_flat = schemaish.Structure([('a', schemaish.Integer()), ('b', schemaish.String())])
        name = 'Integer Form'
        form = formish.Form(schema_flat, name)
        r = {'a': '3', 'b': '4'}
        request = Request(name, r)
        reqr = {'a': ['3'], 'b': ['4']}
        self.assert_(form.structure.attr is schema_flat)
        self.assertEquals(form.validate(request), {'a': 3, 'b': '4'})
        self.assertEqual(form.widget.from_request_data(form, request.POST), {'a': 3, 'b': '4'})
        self.assert_(form.widget.to_request_data(form, {'a': 3, 'b': '4'}) == reqr)

    def test_failure_and_success_callables(self):
        schema_flat = schemaish.Structure([('a', schemaish.Integer(validator=validatish.Range(min=10))), ('b', schemaish.String())])
        name = 'Integer Form'
        form = formish.Form(schema_flat, name)
        r = {'a': '2', 'b': '4'}
        request = Request(name, r)
        self.assertEquals(form.validate(request, failure, success), 'failure')
        self.assertEquals(form.validate(request, failure), 'failure')
        self.assertRaises(formish.FormError, form.validate, request, success_callable=success)
        r = {'a': '12', 'b': '4'}
        request = Request(name, r)
        form = formish.Form(schema_flat, name)
        self.assertEquals(form.validate(request, failure, success), 'success')
        self.assertEquals(form.validate(request, success_callable=success), 'success')
        self.assertEquals(form.validate(request, failure_callable=failure), {'a': 12, 'b': '4'})

    def test_datetuple_type(self):
        schema_flat = schemaish.Structure([('a', schemaish.Date()), ('b', schemaish.String())])
        name = 'Date Form'
        form = formish.Form(schema_flat, name)
        form['a'].widget = formish.DateParts()
        r = {'a.day': '1', 'a.month': '3', 'a.year': '1966', 'b': '4'}
        request = Request(name, r)
        from datetime import date
        d = date(1966, 3, 1)
        self.assertEquals(form.validate(request), {'a': d, 'b': '4'})
        self.assertEqual(form.widget.from_request_data(form, request.get_post()), {'a': d, 'b': '4'})
        self.assert_(form.widget.to_request_data(form, {'a': d, 'b': '4'}) == {'a': {'month': [3], 'day': [1], 'year': [1966]}, 'b': ['4']})

    def test_form_retains_request_data(self):
        form = formish.Form(schemaish.Structure([('field', schemaish.String())]), 'form')
        assert 'name="field" value=""' in form()
        data = form.validate(Request('form', {'field': 'value'}))
        assert data == {'field': 'value'}
        assert form.request_data['field'] == ['value']
        assert 'name="field" value="value"' in form()

    def test_form_accepts_request_data(self):
        form = formish.Form(schemaish.Structure([('field', schemaish.String())]))
        form.request_data = {'field': ['value']}
        assert form._request_data == {'field': ['value']}

    def test_form_with_defaults_accepts_request_data(self):
        form = formish.Form(schemaish.Structure([('field', schemaish.String())]))
        form.defaults = {'field': 'default value'}
        assert 'name="field" value="default value"' in form()
        form.request_data = {'field': ['value']}
        assert form._request_data == {'field': ['value']}
        assert 'name="field" value="value"' in form()

    def test_form_defaults_clears_request_data(self):
        form = formish.Form(schemaish.Structure([('field', schemaish.String())]))
        form.request_data = {'field': ['value']}
        form.defaults = {'field': 'default value'}
        assert form._defaults == {'field': 'default value'}
        assert form._request_data == None
        assert 'name="field" value="default value"' in form()
        return

    def test_method(self):
        schema = schemaish.Structure([('string', schemaish.String())])
        self.assertTrue('method="post"' in formish.Form(schema, 'form')().lower())
        for method in ['POST', 'GET', 'get', 'Get']:
            expected = ('method="%s"' % method).lower()
            rendered = formish.Form(schema, method=method)().lower()
            self.assertTrue(expected in rendered)

        self.assertRaises(ValueError, formish.Form, schema, method='unsupported')
        for (method, request) in [('post', Request(POST={'string': 'abc'})),
         (
          'get', Request(GET={'string': 'abc'}, method='GET'))]:
            data = formish.Form(schema, 'form', method=method).validate(request)
            self.assertTrue(data == {'string': 'abc'})

    def test_simple_validation(self):
        schema_flat = schemaish.Structure([('a', schemaish.Integer())])
        name = 'Integer Form'
        form = formish.Form(schema_flat, name)
        r = {'a': '3'}
        request = Request(name, r)
        reqr = {'a': ['3']}
        self.assertEquals(form.validate(request), {'a': 3})


class TestActions(unittest.TestCase):

    def test_get(self):
        request = Request(method='GET')
        self.assertTrue(self._form('GET').action(request) == 'one')
        request = Request(GET={'one': 'One'}, method='GET')
        self.assertTrue(self._form('GET').action(request) == 'one')
        request = Request(GET={'two': 'Two'}, method='GET')
        self.assertTrue(self._form('GET').action(request) == 'two')

    def test_post(self):
        request = Request(method='POST')
        self.assertTrue(self._form('POST').action(request) == 'one')
        request = Request(POST={'one': 'One'}, method='POST')
        self.assertTrue(self._form('POST').action(request) == 'one')
        request = Request(POST={'two': 'Two'}, method='POST')
        self.assertTrue(self._form('POST').action(request) == 'two')

    def _form(self, method):

        def callback1(*a, **k):
            return 'one'

        def callback2(*a, **k):
            return 'two'

        schema = schemaish.Structure([('string', schemaish.String())])
        form = formish.Form(schema, method=method, add_default_action=False)
        form.add_action('one', 'One', callback1)
        form.add_action('two', 'Two', callback2)
        return form


def success(request, data):
    return 'success'


def failure(request, form):
    return 'failure'


class TestBugs(unittest.TestCase):

    def test_date_conversion(self):
        from datetime import date, datetime
        schema = schemaish.Structure([('date', schemaish.Date())])
        form = formish.Form(schema, name='form')
        form['date'].widget = formish.SelectChoice([(date(1970, 1, 1), 'a'),
         (
          date(1980, 1, 1), 'b'),
         (
          datetime(1990, 1, 1), 'c')])
        self.assertRaises(formish.FormError, form.validate, Request('form', {'date': '1990-01-01T00:00:00'}))
        form()


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/unit/test_siren.py
# Compiled at: 2015-12-08 14:33:04
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from pypermedia.siren import _check_and_decode_response, SirenBuilder, UnexpectedStatusError, MalformedSirenError, SirenLink, SirenEntity, SirenAction, TemplatedString, _create_action_fn
from requests import Response, PreparedRequest
import json, mock, six, types, unittest2

class TestSirenBuilder(unittest2.TestCase):

    def test_check_and_decode_response_404(self):
        """
        Tests the private _check_and_decode_response method
        """
        resp = mock.Mock(status_code=404)
        self.assertIsNone(_check_and_decode_response(resp))

    def test_check_and_decode_bad_status_code(self):
        """
        Tests that an exception is raised for non-200
        status codes.
        """
        resp = mock.Mock(status_code=400)
        self.assertRaises(UnexpectedStatusError, _check_and_decode_response, resp)

    def test_check_and_decode_empty_text(self):
        """
        Tests that an exception is raised when
        the body is empty.
        """
        resp = mock.Mock(status_code=200, text=b'')
        self.assertRaises(MalformedSirenError, _check_and_decode_response, resp)

    def test_construct_link(self):
        builder = SirenBuilder()
        link = builder._construct_link(dict(rel=[b'rel'], href=b'whocares'))
        self.assertIsInstance(link, SirenLink)

    def test_construct_link_bad(self):
        """
        Tests constructing a link.
        """
        builder = SirenBuilder()
        self.assertRaises(KeyError, builder._construct_link, dict(rel=[b'blah']))

    def test_construct_entity_missing_class(self):
        entity = dict(properties={}, actions=[], links=[], entities=[])
        builder = SirenBuilder()
        self.assertRaises(KeyError, builder._construct_entity, entity)

    def test_construct_entity_missing_non_essential(self):
        """Tests that non-essential pieces are ignored."""
        entity = {b'class': [b'blah']}
        builder = SirenBuilder()
        resp = builder._construct_entity(entity)
        self.assertIsInstance(resp, SirenEntity)

    def test_from_api_response(self):
        """
        Tests for a requests.Response object.
        """
        entity = {b'class': [b'blah']}
        resp = Response()
        resp.status_code = 200
        resp._content = six.binary_type(json.dumps(entity).encode(b'utf8'))
        builder = SirenBuilder()
        siren = builder.from_api_response(resp)
        self.assertIsInstance(siren, SirenEntity)

    def test_bad_text_from_api_response(self):
        builder = SirenBuilder()
        self.assertRaises(MalformedSirenError, builder.from_api_response, b'asdfgsjdfg')

    def test_from_api_response_bad_type(self):
        builder = SirenBuilder()
        self.assertRaises(TypeError, builder.from_api_response, [])


class TestSirenEntity(unittest2.TestCase):

    def test_init_no_classnames(self):
        self.assertRaises(ValueError, SirenEntity, None, None)
        self.assertRaises(ValueError, SirenEntity, [], None)
        return

    def test_get_link_no_links(self):
        entity = SirenEntity([b'blah'], None)
        self.assertIsNone(entity.get_links(b'sakdf'))
        return

    def test_get_link(self):
        link = mock.Mock(rel=[b'myrel'])
        entity = SirenEntity([b'blah'], [link])
        resp = entity.get_links(b'myrel')
        self.assertEqual([link], resp)
        self.assertListEqual(entity.get_links(b'badrel'), [])

    def test_get_entity_no_entities(self):
        entity = SirenEntity([b'blah'], None)
        self.assertEqual(entity.get_entities(b'sakdf'), [])
        return

    def test_get_entities(self):
        ent = SirenEntity([b'blah'], [], rel=[b'myrel'])
        entity = SirenEntity([b'builderah'], [], entities=[ent])
        resp = entity.get_entities(b'myrel')
        self.assertEqual([ent], resp)
        self.assertEqual(entity.get_entities(b'badrel'), [])

    def test_get_primary_classname(self):
        entity = SirenEntity([b'blah'], None)
        self.assertEqual(entity.get_primary_classname(), b'blah')
        return

    def test_get_base_classnames(self):
        entity = SirenEntity([b'blah'], None)
        self.assertListEqual(entity.get_base_classnames(), [])
        entity = SirenEntity([b'blah', b'second'], None)
        self.assertListEqual(entity.get_base_classnames(), [b'second'])
        return

    def test_as_siren(self):
        entity = SirenEntity([b'blah'], [])
        siren_dict = entity.as_siren()
        self.assertIsInstance(siren_dict, dict)
        self.assertDictEqual(siren_dict, {b'class': [b'blah'], b'links': [], b'entities': [], b'actions': [], b'properties': {}})

    def test_as_json(self):
        entity = SirenEntity([b'blah'], [])
        json_string = entity.as_json()
        self.assertIsInstance(json_string, six.string_types)

    def test_as_python_object(self):
        entity = SirenEntity([b'blah'], [])
        siren_class = entity.as_python_object()
        self.assertTrue(hasattr(siren_class, b'get_entities'))

    def test_create_python_method_name(self):
        original_expected = [
         ('original', 'original'),
         ('original func', 'originalfunc'),
         ('original-func', 'original_func'),
         ('%bd#$%#$)@c', 'bdc')]
        for original, expected in original_expected:
            actual = SirenEntity._create_python_method_name(original)
            self.assertEqual(actual, expected)

    def test_create_python_method_name_invalid(self):
        bad = ('#$%^#$%&', '', '09345asda')
        for name in bad:
            self.assertRaises(ValueError, SirenEntity._create_python_method_name, name)


class TestSirenAction(unittest2.TestCase):

    def test_add_field(self):
        action = SirenAction(b'action', b'blah', b'application/json')
        self.assertEqual(action.fields, [])
        action.add_field(b'field')
        self.assertEqual(len(action.fields), 1)
        self.assertDictEqual(action.fields[0], dict(name=b'field', type=None, value=None))
        return

    def test_get_fields_dict(self):
        action = SirenAction(b'action', b'blah', b'application/json', fields=[
         dict(name=b'field', type=None, value=b'whocares')])
        field_dict = action.get_fields_as_dict()
        self.assertDictEqual(dict(field=b'whocares'), field_dict)
        return

    def test_as_siren(self):
        action = SirenAction(b'action', b'blah', b'application/json')
        siren_action = action.as_siren()
        expected = {b'href': b'blah', b'name': b'action', b'title': b'action', b'fields': [], b'type': b'application/json', b'method': b'GET'}
        self.assertDictEqual(siren_action, expected)

    def test_as_json(self):
        action = SirenAction(b'action', b'blah', b'application/json')
        siren_action = action.as_json()
        self.assertIsInstance(siren_action, six.string_types)

    def test_get_bound_href(self):
        action = SirenAction(b'action', b'blah', b'application/json')
        bound_href, request_fields = action._get_bound_href(TemplatedString, x=1, y=2)
        self.assertEqual(bound_href, b'blah')
        self.assertDictEqual(request_fields, dict(x=1, y=2))

    def test_get_bound_href_with_template(self):
        action = SirenAction(b'action', b'http://host.com/{id}/{id}', b'application/json')
        bound_href, request_fields = action._get_bound_href(TemplatedString, x=1, y=2, id=3)
        self.assertEqual(bound_href, b'http://host.com/3/3')
        self.assertDictEqual(dict(x=1, y=2), request_fields)

    def test_get_bound_href_unboud_variables(self):
        action = SirenAction(b'action', b'http://host.com/{id}/{id}', b'application/json')
        self.assertRaises(ValueError, action._get_bound_href, TemplatedString, x=1, y=2)

    def test_as_request_get(self):
        action = SirenAction(b'action', b'http://blah.com', b'application/json')
        resp = action.as_request(x=1, y=2)
        self.assertIsInstance(resp, PreparedRequest)
        self.assertEqual(resp.method, b'GET')
        self.assertIn(b'y=2', resp.path_url)
        self.assertIn(b'x=1', resp.path_url)

    def test_as_request_post(self):
        action = SirenAction(b'action', b'http://blah.com', b'application/json', method=b'POST')
        resp = action.as_request(x=1, y=2)
        self.assertIsInstance(resp, PreparedRequest)
        self.assertEqual(resp.method, b'POST')
        self.assertEqual(b'/', resp.path_url)

    def test_as_request_delete(self):
        action = SirenAction(b'action', b'http://blah.com', b'application/json', method=b'DELETE')
        resp = action.as_request(x=1, y=2)
        self.assertIsInstance(resp, PreparedRequest)
        self.assertEqual(resp.method, b'DELETE')
        self.assertEqual(b'/', resp.path_url)

    def test_make_request(self):
        action = SirenAction(b'action', b'http://blah.com', b'application/json')
        mck = mock.Mock(send=mock.Mock(return_value=True))
        resp = action.make_request(_session=mck, x=1, y=2)
        self.assertTrue(resp)
        self.assertEqual(mck.send.call_count, 1)
        self.assertIsInstance(mck.send.call_args[0][0], PreparedRequest)


class TestSirenLink(unittest2.TestCase):

    def test_init_errors(self):
        self.assertRaises(ValueError, SirenLink, [], b'href')
        self.assertRaises(ValueError, SirenLink, None, b'href')
        self.assertRaises(ValueError, SirenLink, [b'blah'], b'')
        return

    def test_init_rel_string(self):
        siren_link = SirenLink(b'blah', b'href')
        self.assertEqual([b'blah'], siren_link.rel)

    def test_add_rel(self):
        link = SirenLink([b'blah'], b'blah')
        self.assertListEqual(link.rel, [b'blah'])
        link.add_rel(b'two')
        self.assertListEqual([b'blah', b'two'], link.rel)
        link.add_rel(b'two')
        self.assertListEqual([b'blah', b'two'], link.rel)

    def test_rem_rel(self):
        link = SirenLink([b'blah'], b'blah')
        link.rem_rel(b'notreal')
        self.assertListEqual(link.rel, [b'blah'])
        link.rem_rel(b'blah')
        self.assertListEqual(link.rel, [])

    def test_as_siren(self):
        link = SirenLink([b'blah'], b'href')
        self.assertDictEqual(link.as_siren(), dict(rel=[b'blah'], href=b'href'))

    def test_as_json(self):
        link = SirenLink([b'blah'], b'href')
        self.assertIsInstance(link.as_json(), six.string_types)

    def test_as_request(self):
        href = b'http://notreal.com/'
        link = SirenLink([b'blah'], b'http://notreal.com')
        req = link.as_request()
        self.assertIsInstance(req, PreparedRequest)
        self.assertEqual(href, req.url)

    def test_make_request(self):
        link = SirenLink([b'blah'], b'http://notreal.com')
        session = mock.MagicMock()
        resp = link.make_request(_session=session)
        self.assertEqual(session.send.call_count, 1)

    def test_as_python_object(self):
        """
        Mostly just an explosion test.
        """
        link = SirenLink(b'blah', b'blah')
        with mock.patch.object(link, b'make_request') as (make_request):
            with mock.patch.object(link, b'from_api_response') as (from_api_respons):
                resp = link.as_python_object()
                self.assertEqual(make_request.call_count, 1)
                self.assertEqual(from_api_respons.call_count, 1)


class TestTemplatedString(unittest2.TestCase):

    def test_init(self):
        base = b'/blah/'
        template = TemplatedString(base)
        self.assertEqual(len(template.param_dict), 0)
        base = b'/{id}/{pk}/sdf'
        template = TemplatedString(base)
        self.assertEqual(len(template.param_dict), 2)
        self.assertEqual(template.param_dict[b'id'], b'{id}')
        self.assertEqual(template.param_dict[b'pk'], b'{pk}')

    def test_items(self):
        base = b'/{id}/{pk}/sdf'
        template = TemplatedString(base)
        for p in [('id', '{id}'), ('pk', '{pk}')]:
            self.assertIn(p, template.items())

    def test_unbound_variables(self):
        base = b'/{id}/{pk}/sdf'
        template = TemplatedString(base)
        for p in [b'id', b'pk']:
            self.assertIn(p, template.unbound_variables())

    def test_bind(self):
        base = b'/{id}/{pk}/sdf'
        template = TemplatedString(base)
        template2 = template.bind(id=1)
        self.assertEqual(template2.base, b'/1/{pk}/sdf')
        self.assertDictEqual(template2.param_dict, {b'pk': b'{pk}'})
        template3 = template2.bind(id=1)
        self.assertEqual(template3.base, b'/1/{pk}/sdf')
        self.assertDictEqual(template3.param_dict, {b'pk': b'{pk}'})
        template4 = template3.bind(pk=2)
        self.assertEqual(template4.base, b'/1/2/sdf')
        self.assertDictEqual(template4.param_dict, {})
        template5 = template4.bind(who=b'asdknf', cares=23)
        self.assertEqual(template5.base, b'/1/2/sdf')
        self.assertDictEqual(template5.param_dict, {})

    def test_has_unbound_variables(self):
        base = b'/{id}/{pk}/sdf'
        template = TemplatedString(base)
        self.assertTrue(template.has_unbound_variables())
        base = b'/sdf'
        template = TemplatedString(base)
        self.assertFalse(template.has_unbound_variables())

    def test_as_string(self):
        base = b'/{id}/{pk}/sdf'
        template = TemplatedString(base)
        self.assertEqual(base, template.as_string())


class TestMiscellaneousSiren(unittest2.TestCase):

    def test_create_action_function(self):
        action = mock.MagicMock()
        siren = mock.MagicMock()
        func = _create_action_fn(action, siren)
        self.assertIsInstance(func, types.FunctionType)
        slf = mock.MagicMock()
        resp = func(slf, blah=b'ha')
        self.assertEqual(siren.from_api_response.return_value.as_python_object.return_value, resp)
        self.assertEqual(action.make_request.return_value, siren.from_api_response.call_args[1][b'response'])

    def test_create_action_function_none_response(self):
        action = mock.MagicMock()
        siren = mock.MagicMock()
        siren.from_api_response.return_value = None
        func = _create_action_fn(action, siren)
        slf = mock.MagicMock()
        resp = func(slf, blah=b'ha')
        self.assertIsNone(resp)
        return
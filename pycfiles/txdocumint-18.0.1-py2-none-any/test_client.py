# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathan/Coding/txdocumint/txdocumint/test/test_client.py
# Compiled at: 2016-02-08 14:56:37
import json
from StringIO import StringIO
from testtools import TestCase
from testtools.matchers import AfterPreprocessing, ContainsDict, Equals, IsInstance, MatchesAll, MatchesListwise, MatchesStructure
from testtools.twistedsupport import failed, succeeded
from treq.testing import StringStubbingResource, StubTreq
from twisted.web.http_headers import Headers
from txdocumint._client import content_type, create_session, documint_request_factory, get_session, json_request, post_json, Session
from txdocumint.error import DocumintError, MalformedDocumintError

class JSONRequestTests(TestCase):
    """
    Tests for `txdocumint._client.json_request`.
    """

    def test_overwrite_accept(self):
        """
        If an existing ``Accept`` header exists it is overwritten.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('GET'))
            self.assertThat(url, Equals('http://example.com/get_json'))
            self.assertThat(headers, ContainsDict({'Accept': Equals(['application/json'])}))
            return (
             200, {}, json.dumps({'arst': 'arst'}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        self.assertThat(json_request(treq.request, 'GET', 'http://example.com/get_json', headers={'Accept': 'text/plain'}), succeeded(Equals({'arst': 'arst'})))

    def test_request(self):
        """
        Makes a request and decodes JSON responses.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('GET'))
            self.assertThat(url, Equals('http://example.com/get_json'))
            self.assertThat(headers, ContainsDict({'Accept': Equals(['application/json'])}))
            return (
             200, {}, json.dumps({'arst': 'arst'}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        self.assertThat(json_request(treq.request, 'GET', 'http://example.com/get_json'), succeeded(Equals({'arst': 'arst'})))


class PostJSONTests(TestCase):
    """
    Tests for `txdocumint._client.post_json`.
    """

    def test_own_content_type(self):
        """
        If an existing ``Content-Type`` header exists it is used instead of
        ``application/json``.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('POST'))
            self.assertThat(url, Equals('http://example.com/post_json'))
            self.assertThat(headers, ContainsDict({'Accept': Equals(['application/json']), 'Content-Type': Equals(['text/plain'])}))
            return (200, {}, json.dumps({'arst': 'arst'}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        self.assertThat(post_json(treq.request, 'http://example.com/post_json', headers={'Content-Type': 'text/plain'}), succeeded(Equals({'arst': 'arst'})))

    def test_request(self):
        """
        Makes a POST request and decodes JSON responses.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('POST'))
            self.assertThat(url, Equals('http://example.com/post_json'))
            self.assertThat(headers, ContainsDict({'Accept': Equals(['application/json']), 'Content-Type': Equals(['application/json'])}))
            return (200, {}, json.dumps({'arst': 'arst'}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        self.assertThat(post_json(treq.request, 'http://example.com/post_json'), succeeded(Equals({'arst': 'arst'})))


class DocumintRequestFactoryTests(TestCase):
    """
    Tests for `txdocumint._client.documint_request_factory`.
    """

    def test_malformed_error(self):
        """
        Documint errors that do not have a JSON content type raise
        `MalformedDocumintError`.
        """

        def _response_for(method, url, params, headers, data):
            return (
             400, {}, 'an error')

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        request = documint_request_factory(treq.request)
        self.assertThat(request('GET', 'http://example.com/malformed_error'), failed(AfterPreprocessing(lambda f: f.value, MatchesAll(IsInstance(MalformedDocumintError), MatchesStructure(data=Equals('an error'))))))

    def test_not_json_error(self):
        """
        Documint errors that have a JSON content type but do not contain valid
        JSON raise `MalformedDocumintError`.
        """

        def _response_for(method, url, params, headers, data):
            return (
             400, {'Content-Type': 'application/json'},
             'hello world')

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        request = documint_request_factory(treq.request)
        self.assertThat(request('GET', 'http://example.com/not_json_error'), failed(AfterPreprocessing(lambda f: f.value, MatchesAll(IsInstance(MalformedDocumintError), MatchesStructure(data=Equals('hello world'))))))

    def test_error(self):
        """
        Documint errors are parsed into a structured exception.
        """

        def _response_for(method, url, params, headers, data):
            return (
             400, {'Content-Type': 'application/json'},
             json.dumps({'causes': [
                         {'type': 'foo', 'reason': 42, 
                            'description': 'nope'},
                         {'type': 'bar', 'reason': 42, 
                            'description': None},
                         {'type': 'baz', 'reason': None, 
                            'description': None}]}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        request = documint_request_factory(treq.request)

        def cause(t, r=None, d=None):
            return MatchesStructure(type=Equals(t), reason=Equals(r), description=Equals(d))

        self.assertThat(request('GET', 'http://example.com/error'), failed(AfterPreprocessing(lambda f: f.value, MatchesAll(IsInstance(DocumintError), MatchesStructure(causes=MatchesListwise([
         cause('foo', 42, 'nope'),
         cause('bar', 42),
         cause('baz')]))))))
        return

    def test_success(self):
        """
        Status codes indicating success pass the response through without any
        exceptions.
        """

        def _response_for(method, url, params, headers, data):
            return (
             200, {}, 'hello world')

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        request = documint_request_factory(treq.request)
        self.assertThat(request('GET', 'http://example.com/success'), succeeded(AfterPreprocessing(treq.content, succeeded(Equals('hello world')))))


class ContentTypeTests(TestCase):
    """
    Tests for `txdocumint._client.content_type`.
    """

    def test_missing(self):
        """
        Default to ``application/octet-stream`` if there is no ``Content-Type``
        header.
        """
        headers = Headers()
        self.assertThat(content_type(headers), Equals('application/octet-stream'))

    def test_content_type(self):
        """
        Use the first ``Content-Type`` header.
        """
        headers = Headers({'Content-Type': ['application/json',
                          'text/plain']})
        self.assertThat(content_type(headers), Equals('application/json'))


class SessionTests(TestCase):
    """
    Tests for `txdocumint._client.Session`.
    """

    def test_store_content(self):
        """
        Store content in a Documint session.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('POST'))
            self.assertThat(headers, ContainsDict({'Accept': Equals(['application/json']), 
               'Content-Type': Equals(['text/plain'])}))
            self.assertThat(url, MatchesAll(IsInstance(bytes), Equals('http://example.com/store')))
            self.assertThat(data, MatchesAll(IsInstance(bytes), Equals('hello world')))
            return (200, {'Content-Type': 'application/json'},
             json.dumps({'links': {'self': 'http://example.com/stored_object'}}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        session = Session({'store-content': 'http://example.com/store'}, treq.request)
        fileobj = 'hello world'
        self.assertThat(session.store_content(fileobj, 'text/plain'), succeeded(Equals('http://example.com/stored_object')))

    def test_get_content(self):
        """
        Stream content.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('GET'))
            self.assertThat(url, MatchesAll(IsInstance(bytes), Equals('http://example.com/some_content')))
            return (200, {'Content-Type': 'text/plain'},
             'hello world')

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        session = Session({}, treq.request)
        buf = StringIO()
        self.assertThat(session.get_content('http://example.com/some_content', buf.write), succeeded(Equals('text/plain')))
        self.assertThat(buf.getvalue(), Equals('hello world'))

    def test_perform_action(self):
        """
        Perform an action within a session.
        """
        payload = {'links': {'result': 'https://example.com/result'}}
        action = {'action': 'some_action', 'parameters': {'foo': 42}}

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('POST'))
            self.assertThat(url, MatchesAll(IsInstance(bytes), Equals('http://example.com/perform')))
            self.assertThat(json.loads(data), Equals(action))
            return (200, {'Content-Type': 'application/json'},
             json.dumps(payload))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        session = Session({'perform': 'http://example.com/perform'}, treq.request)
        self.assertThat(session.perform_action((action, lambda x: x)), succeeded(Equals(payload)))

    def test_delete(self):
        """
        Delete a session.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('DELETE'))
            self.assertThat(url, MatchesAll(IsInstance(bytes), Equals('http://example.com/session')))
            return (200, {}, '')

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        session = Session({'self': 'http://example.com/session'}, treq.request)
        self.assertThat(session.delete(), succeeded(Equals('')))


class CreateSessionTests(TestCase):
    """
    Tests for `txdocumint._client.create_session`.
    """

    def test_create_session(self):
        """
        Create a session.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('POST'))
            self.assertThat(url, MatchesAll(IsInstance(bytes), Equals('http://example.com/sessions/')))
            return (
             200, {},
             json.dumps({'links': {'self': 'http://example.com/sessions/1234'}}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        self.assertThat(create_session('http://example.com', treq.request), succeeded(MatchesStructure(_session_info=Equals({'self': 'http://example.com/sessions/1234'}))))


class GetSessionTests(TestCase):
    """
    Tests for `txdocumint._client.get_session`.
    """

    def test_get_session(self):
        """
        Create a session.
        """

        def _response_for(method, url, params, headers, data):
            self.assertThat(method, Equals('GET'))
            self.assertThat(url, MatchesAll(IsInstance(bytes), Equals('http://example.com/sessions/1234')))
            return (
             200, {},
             json.dumps({'links': {'self': 'http://example.com/sessions/1234'}}))

        resource = StringStubbingResource(_response_for)
        treq = StubTreq(resource)
        self.assertThat(get_session('http://example.com/sessions/1234', treq.request), succeeded(MatchesStructure(_session_info=Equals({'self': 'http://example.com/sessions/1234'}))))
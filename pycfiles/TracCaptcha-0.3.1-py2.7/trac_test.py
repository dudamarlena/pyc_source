# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/test_util/trac_test.py
# Compiled at: 2011-02-04 10:56:30
from cStringIO import StringIO
import re
from BeautifulSoup import BeautifulSoup
from trac.core import Component, ComponentMeta
from trac.perm import DefaultPermissionPolicy, PermissionCache, PermissionSystem
from trac.web.api import Request, RequestDone
from trac.web.main import RequestDispatcher
from trac_captcha.lib.testcase import PythonicTestCase
__all__ = [
 'mock_request', 'TracTest']

class MockResponse(object):

    def __init__(self):
        self.status_line = None
        self.headers = []
        self.body = StringIO()
        return

    def code(self):
        string_code = self.status_line.split(' ', 1)[0]
        return int(string_code)

    def start_response(self, status, response_headers):
        self.status_line = status
        self.headers = response_headers
        return lambda data: self.body.write(data)

    def html(self):
        self.body.seek(0)
        body_content = self.body.read()
        self.body.seek(0)
        return body_content

    def trac_messages(self, message_type):
        soup = BeautifulSoup(self.html())
        message_container = soup.find(name='div', attrs=dict(id='warning'))
        if message_container is None:
            return []
        else:
            messages_with_tags = message_container.findAll('li')
            if len(messages_with_tags) > 0:
                strip_tags = lambda html: re.sub('^<li>(.*)</li>$', '\\1', unicode(html))
                return map(strip_tags, messages_with_tags)
            pattern = '<strong>%s:</strong>\\s*(.*?)\\s*</div>' % message_type
            match = re.search(pattern, unicode(message_container), re.DOTALL | re.IGNORECASE)
            if match is None:
                return []
            return [
             match.group(1)]

    def trac_warnings(self):
        return self.trac_messages('Warning')


def mock_request(path, request_attributes=None, **kwargs):
    request_attributes = request_attributes or {}
    wsgi_environment = {'SERVER_PORT': 4711, 
       'SERVER_NAME': 'foo.bar', 
       'REMOTE_ADDR': '127.0.0.1', 
       'REQUEST_METHOD': request_attributes.pop('method', 'GET'), 
       'PATH_INFO': path, 
       'wsgi.url_scheme': 'http', 
       'wsgi.input': StringIO()}
    wsgi_environment.update(request_attributes)
    response = MockResponse()
    request = Request(wsgi_environment, response.start_response)
    request.captured_response = response
    request.args = kwargs
    return request


class TracTest(PythonicTestCase):

    def enable_ticket_subsystem(self):
        import trac.ticket.api, trac.ticket.admin, trac.ticket.default_workflow, trac.ticket.model, trac.ticket.notification, trac.ticket.query, trac.ticket.report, trac.ticket.roadmap, trac.ticket.web_ui

    def disable_component(self, component):
        component_name = self.trac_component_name_for_class(component)
        self.env.config.set('components', component_name, 'disabled')
        self.clear_trac_rule_cache()
        if isinstance(component, (Component, ComponentMeta)):
            self.assert_false(self.env.is_component_enabled(component), '%s is not disabled' % component_name)

    def enable_component(self, component):
        component_name = self.trac_component_name_for_class(component)
        self.env.config.set('components', component_name, 'enabled')
        self.clear_trac_rule_cache()
        if isinstance(component, (Component, ComponentMeta)):
            self.assert_true(self.env.is_component_enabled(component), '%s is not enabled' % component_name)

    def grant_permission(self, username, action):
        DefaultPermissionPolicy(self.env).permission_cache = {}
        PermissionSystem(self.env).grant_permission(username, action)
        self.assert_true(self.has_permission(username, action))

    def has_permission(self, username, action):
        DefaultPermissionPolicy(self.env).permission_cache = {}
        return PermissionSystem(self.env).check_permission(action, username)

    def assert_has_permission(self, username, action):
        self.assert_true(self.has_permission(username, action))

    def assert_has_no_permission(self, username, action):
        self.assert_false(self.has_permission(username, action))

    def request(self, path, request_attributes=None, **kwargs):
        request = mock_request(path, request_attributes, **kwargs)
        request.perm = PermissionCache(self.env, username=request.remote_user)
        return request

    def post_request(self, *args, **kwargs):
        kwargs.setdefault('request_attributes', dict())
        kwargs['request_attributes']['method'] = 'POST'
        return self.request(*args, **kwargs)

    def simulate_request(self, req):
        process_request = lambda : RequestDispatcher(self.env).dispatch(req)
        self.assert_raises(RequestDone, process_request)
        response = req.captured_response
        response.body.seek(0)
        return response

    def trac_component_name_for_class(self, component_or_name):
        if isinstance(component_or_name, basestring):
            return component_or_name
        class_name = str(component_or_name.__name__)
        return str(component_or_name.__module__ + '.' + class_name).lower()

    def clear_trac_rule_cache(self):
        if hasattr(self.env, '_rules'):
            del self.env._rules
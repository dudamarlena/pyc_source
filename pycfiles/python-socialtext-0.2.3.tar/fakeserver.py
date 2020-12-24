# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/fakeserver.py
# Compiled at: 2011-12-29 15:54:18
"""
A fake server that "responds" to API methods with pre-canned responses.
"""
import requests, urlparse, urllib
from nose.tools import assert_equal
from socialtext import Socialtext
from socialtext.client import SocialtextClient
from utils import fail, assert_in, assert_not_in, assert_has_keys

class FakeConfig(object):
    username = 'username'
    password = 'password'
    url = 'https://st.example.com'
    user_agent = 'python-socialtext/test'


def resp(status, body, headers={}):
    r = requests.models.Response()
    r.status_code = status
    r.headers = headers
    return (r, body)


class FakeServer(Socialtext):

    def __init__(self, **kwargs):
        super(FakeServer, self).__init__(**kwargs)
        self.client = FakeClient()

    def _get_config(self, kwargs):
        return FakeConfig()

    def assert_called--- This code section failed: ---

 L.  38         0  LOAD_FAST             1  'method'
                3  LOAD_FAST             2  'url'
                6  BUILD_TUPLE_2         2 
                9  STORE_FAST            5  'expected'

 L.  40        12  LOAD_FAST             0  'self'
               15  LOAD_ATTR             0  'client'
               18  LOAD_ATTR             1  'callstack'
               21  POP_JUMP_IF_TRUE     37  'to 37'
               24  LOAD_ASSERT              AssertionError
               27  LOAD_CONST               'Expected %s %s but no calles were made.'
               30  LOAD_FAST             5  'expected'
               33  BINARY_MODULO    
               34  RAISE_VARARGS_2       2  None

 L.  42        37  LOAD_FAST             0  'self'
               40  LOAD_ATTR             0  'client'
               43  LOAD_ATTR             1  'callstack'
               46  LOAD_ATTR             3  'pop'
               49  CALL_FUNCTION_0       0  None
               52  STORE_FAST            6  'called'

 L.  44        55  LOAD_FAST             5  'expected'
               58  LOAD_FAST             6  'called'
               61  LOAD_CONST               0
               64  LOAD_CONST               2
               67  SLICE+3          
               68  COMPARE_OP            2  ==
               71  POP_JUMP_IF_TRUE     98  'to 98'
               74  LOAD_ASSERT              AssertionError
               77  LOAD_CONST               'Expected %s %s, got %s %s'
               80  LOAD_FAST             5  'expected'
               83  LOAD_FAST             6  'called'
               86  LOAD_CONST               0
               89  LOAD_CONST               2
               92  SLICE+3          
               93  BINARY_ADD       
               94  BINARY_MODULO    
               95  RAISE_VARARGS_2       2  None

 L.  46        98  LOAD_FAST             3  'data'
              101  LOAD_CONST               None
              104  COMPARE_OP            9  is-not
              107  POP_JUMP_IF_FALSE   130  'to 130'

 L.  47       110  LOAD_GLOBAL           5  'assert_equal'
              113  LOAD_FAST             6  'called'
              116  LOAD_CONST               2
              119  BINARY_SUBSCR    
              120  LOAD_FAST             3  'data'
              123  CALL_FUNCTION_2       2  None
              126  POP_TOP          
              127  JUMP_FORWARD          0  'to 130'
            130_0  COME_FROM           127  '127'

 L.  49       130  LOAD_FAST             4  'params'
              133  POP_JUMP_IF_FALSE   156  'to 156'

 L.  50       136  LOAD_GLOBAL           5  'assert_equal'
              139  LOAD_FAST             6  'called'
              142  LOAD_CONST               3
              145  BINARY_SUBSCR    
              146  LOAD_FAST             4  'params'
              149  CALL_FUNCTION_2       2  None
              152  POP_TOP          
              153  JUMP_FORWARD          0  'to 156'
            156_0  COME_FROM           153  '153'
              156  LOAD_CONST               None
              159  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 156


class FakeClient(SocialtextClient):

    def __init__(self):
        self.url = 'http://st.example.com'
        self.user = 'user'
        self.password = 'password'
        self.callstack = []

    def get(self, url, **kwargs):
        return self._st_request(url, 'GET', **kwargs)

    def _st_request(self, url, method, **kwargs):
        if method in ('GET', 'DELETE'):
            assert_not_in('data', kwargs)
        elif method in ('PUT', 'POST'):
            assert_in('data', kwargs)
        munged_url = url.strip('/').replace('/', '_').replace('.', '_').replace('%20', '_')
        callback = '%s_%s' % (method.lower(), munged_url)
        if not hasattr(self, callback):
            fail('Called unknown API method: %s %s' % (method, url))
        self.callstack.append((method, url, kwargs.get('data', None), kwargs.get('params', {})))
        return getattr(self, callback)(**kwargs)

    def get_data_accounts(self, **kw):
        return resp(200, [
         {'desktop_logo_uri': '/static/desktop/images/sd-logo.png', 
            'desktop_link_color': '#0081F8', 
            'desktop_bg_color': '#FFFFFF', 
            'desktop_header_gradient_bottom': '#506481', 
            'desktop_2nd_bg_color': '#F2F2F2', 
            'account_name': 'Socialtext', 
            'account_id': '2', 
            'plugins_enabled': [
                              'dashboard',
                              'groups',
                              'people',
                              'signals',
                              'widgets'], 
            'desktop_highlight_color': '#FFFDD3', 
            'desktop_header_gradient_top': '#4C739B', 
            'plugin_preferences': {'signals': {'signals_size_limit': 400}}, 
            'desktop_text_color': '#000000'}])

    def get_data_accounts_2(self, **kw):
        acct = self.get_data_accounts()[1][0]
        return resp(200, acct)

    def post_data_accounts(self, **kw):
        assert_has_keys(kw, required=['data'])
        body = kw['data']
        assert_has_keys(body, required=[
         'name'])
        return resp(201, None, headers={'location': '/data/accounts/2'})

    def get_data_accounts_2_users(self, **kw):
        return resp(200, [
         {'email_address': 'john@example.com', 
            'best_full_name': 'John Smith', 
            'user_id': 123, 
            'username': 'JAS123', 
            'last_name': 'Smith', 
            'first_name': 'John', 
            'roles': [
                    'member']}])

    def get_data_accounts_2_users_abc123(self, **kw):
        member = self.get_data_accounts_2_users()[1][0]
        return resp(200, member)

    def post_data_accounts_2_users(self, **kw):
        assert_has_keys(kw, required=['data'])
        body = kw['data']
        assert_has_keys(body, required=['username'])
        return resp(200, None)

    def get_data_config(self, **kw):
        return resp(200, {'allow_network_invitation': 0, 
           'api_version': 31, 
           'data_push_available': 1, 
           'desktop_update_url': 'https://st.example.com/st/desktop/update', 
           'server_version': '4.5.3.15', 
           'signals_size_limit': '1000'})

    def get_raise_400(self, **kw):
        return resp(400, None)

    def get_raise_401(self, **kw):
        return resp(401, None)

    def get_raise_403(self, **kw):
        return resp(403, None)

    def get_raise_404(self, **kw):
        return resp(404, None)

    def get_raise_409(self, **kw):
        return resp(409, None)

    def get_raise_413(self, **kw):
        return resp(413, None)

    def get_raise_503(self, **kw):
        return resp(503, None)

    def get_data_groups(self, **kw):
        return resp(200, [
         {'permission_set': 'self-join', 
            'name': 'Mac Fans', 
            'created_by_username': 'Joseph Hines', 
            'description': 'Those that love their shiny white laptops and phones', 
            'uri': '/data/groups/21', 
            'created_by_user_id': '131', 
            'primary_account_name': 'Ryker', 
            'primary_account_id': '9', 
            'group_id': '21', 
            'creation_date': '2010-02-22', 
            'workspace_count': '0', 
            'user_count': '4'}])

    def get_data_groups_21(self, **kw):
        group = self.get_data_groups()[1][0]
        return resp(200, group)

    def post_data_groups(self, **kw):
        assert_has_keys(kw, required=['data'])
        return resp(201, None, headers={'location': '/data/groups/21'})

    def post_data_groups_21_trash(self, **kw):
        assert_has_keys(kw, required=['data'])
        body = kw['data']
        for item in body:
            assert_has_keys(item, optional=['workspace_id', 'user_id'])

        return resp(200, None)

    def get_data_signals(self, **kw):
        query = kw.get('query', {})
        assert_has_keys(query, optional=[
         'accounts',
         'after',
         'before',
         'direct',
         'direction',
         'following',
         'groups',
         'hidden',
         'limit',
         'offset',
         'order',
         'sender'])
        return resp(200, [
         {'mentioned_users': [], 'attachments': [], 'in_reply_to': {}, 'group_ids': [], 'num_replies': '0', 
            'account_ids': [
                          '1'], 
            'tags': [
                   'foo', 'bar'], 
            'annotations': [], 'uri': '/st/signals/45ddcc89023426bf', 
            'body': 'Hello world!', 
            'hash': '103dcc89023428d82', 
            'best_full_name': 'John Smith', 
            'at': '2009-01-06 20:19:24.501494Z', 
            'user_id': '3038', 
            'signal_id': '123'},
         {'mentioned_users': [{'best_full_name': 'Smart Bob', 'id': 34343}], 'attachments': [], 'in_reply_to': {'user_id': '34343', 'signal_id': '402', 'uri': '/st/signal/d28dcc89023428f3?r=4fgdcc89023429d5'}, 'group_ids': [], 'num_replies': '0', 
            'account_ids': [
                          '1', '2', '3'], 
            'tags': [
                   'see it', 'on now'], 
            'annotations': [{'my_movies': {'title': 'Bullit'}}], 'uri': '/st/signals/45ddcc89023426bf', 
            'body': 'I got my mustang back from the shop that <a href="/?profile/3063">Smart Bob</a> owns', 
            'hash': '103dcc89023428d82', 
            'best_full_name': 'Steve McQueen', 
            'at': '2009-01-06 20:19:24.501494Z', 
            'user_id': '3037', 
            'signal_id': '987'}])

    def get_data_signals_123(self, **kw):
        signal = self.get_data_signals()[1][0]
        return resp(200, signal)

    def delete_data_signals_123(self, **kw):
        return resp(202, None)

    def put_data_signals_123_hidden(self, **kw):
        return resp(202, None)

    def post_data_signals(self, **kw):
        assert_has_keys(kw, required=['data'])
        body = kw['data']
        assert_has_keys(body, required=[
         'signal'], optional=[
         'account_ids',
         'all_accounts',
         'annotations',
         'at',
         'attachments',
         'in_reply_to',
         'group_ids',
         'recipient'])
        assert_has_keys(body.get('in_reply_to', {}), optional=[
         'signal_id',
         'search'])
        return resp(204, None, headers={'x-location': '/st/signals/45ddcc89023426bf', 
           'x-signal-id': 123, 
           'x-signal-hash': '103dcc89023428d82'})

    def get_data_signals_123_likes(self, **kw):
        return resp(200, [ dict(user_id=u['user_id'], best_full_name=u['best_full_name']) for u in self.get_data_users()[1] ])

    def delete_data_signals_123_likes_username(self, **kw):
        return resp(200, None)

    def put_data_signals_123_likes_username(self, **kw):
        return resp(204, None)

    def get_data_users(self, **kw):
        query = kw.get('query', {})
        assert_has_keys(query, optional=[
         'count', 'filter', 'offset', 'order', 'want_private_fields'])
        return resp(200, [
         {'email_address': 'john@example.com', 
            'best_full_name': 'John Smith', 
            'user_id': 123, 
            'username': 'JAS123', 
            'last_name': 'Smith', 
            'first_name': 'John'},
         {'email_address': 'bob@example.com', 
            'best_full_name': 'Bob MacDonald', 
            'user_id': 987, 
            'username': 'BAM987', 
            'last_name': 'MacDonald', 
            'first_name': 'Bob'}])

    def get_data_users_123(self, **kw):
        query = kw.get('query', {})
        assert_has_keys(query, optional=[
         'all', 'want_private_fields'])
        user = self.get_data_users()[1][0]
        return resp(200, user)

    def get_data_webhooks(self, **kw):
        return resp(200, [
         {'workspace_id': None, 
            'group_id': None, 
            'url': 'https://example.com', 
            'class': 'signal.create', 
            'id': 123, 
            'details': {'to_user': 123, 'tag': 'abc123'}, 'account_id': 1, 
            'creator_id': 110},
         {'workspace_id': 123, 
            'group_id': None, 
            'url': 'https://example.com', 
            'class': 'page.create', 
            'id': 987, 
            'details': {'page_id': 'example_page'}, 'account_id': None, 
            'creator_id': 110}])

    def get_data_webhooks_123(self, **kw):
        hook = self.get_data_webhooks()[1][0]
        return resp(200, hook)

    def get_data_webhooks_987(self, **kw):
        hook = self.get_data_webhooks()[1][1]
        return resp(200, hook)

    def delete_data_webhooks_123(self, **kw):
        return resp(202, None)

    def post_data_webhooks(self, **kw):
        assert_has_keys(kw, required=['data'])
        body = kw['data']
        assert_has_keys(body, required=[
         'class', 'url'], optional=[
         'workspace_id', 'account_id', 'group_id', 'details'])
        hook_id = 123 if body['class'] == 'signal.create' else 987
        return resp(204, None, headers={'location': '/data/webhooks/%d' % hook_id})

    def get_data_workspaces(self, **kw):
        return resp(200, [
         {'workspace_id': '123', 
            'is_all_users_workspace': 0, 
            'permission_set': 'members_only', 
            'group_count': '3', 
            'name': 'marketing', 
            'default': 0, 
            'modified_time': '2007-05-21 10:55:46.630421-07', 
            'account_id': '2', 
            'uri': '/data/workspaces/marketing', 
            'id': 123, 
            'title': 'Marketing', 
            'user_count': 2},
         {'workspace_id': '987', 
            'is_all_users_workspace': 0, 
            'permission_set': 'members_only', 
            'group_count': '1', 
            'name': 'sales', 
            'default': 0, 
            'modified_time': '2007-05-21 10:55:46.630421-07', 
            'account_id': '1', 
            'uri': '/data/workspaces/sales', 
            'id': 987, 
            'title': 'Sales', 
            'user_count': 2}])

    def get_data_workspaces_123(self, **kw):
        hook = self.get_data_workspaces()[1][0]
        return resp(200, hook)

    def get_data_workspaces_marketing(self, **kw):
        hook = self.get_data_workspaces()[1][0]
        return resp(200, hook)

    def delete_data_workspaces_123(self, **kw):
        return resp(202, None)

    def delete_data_workspaces_marketing(self, **kw):
        return self.delete_data_workspaces_123()

    def get_data_workspaces_987(self, **kw):
        hook = self.get_data_workspaces()[1][1]
        return resp(200, hook)

    def get_data_workspaces_sales(self, **kw):
        hook = self.get_data_workspaces()[1][1]
        return resp(200, hook)

    def post_data_workspaces(self, **kw):
        return resp(201, None, headers={'location': '/data/workspaces/marketing'})

    def get_data_workspaces_marketing_tags(self, **kw):
        return resp(200, [{'name': 'Test', 'page_count': 1, 'uri': '/tags/Test'}])

    def get_data_workspaces_marketing_tags_Test(self, **kw):
        tag = self.get_data_workspaces_marketing_tags()[1][0]
        return resp(200, tag)

    def put_data_workspaces_marketing_tags_Test(self, **kw):
        return resp(204, None)

    def delete_data_workspaces_marketing_tags_Test(self, **kw):
        return resp(202, None)

    def get_data_workspaces_marketing_pages(self, **kw):
        return resp(200, [
         {'page_uri': 'http://example.com/marketing/index.cgi?test_1', 
            'modified_time': 1169971407, 
            'name': 'Test 1', 
            'uri': 'test_1', 
            'revision_id': 1234567890, 
            'page_id': 'test_1', 
            'tags': [
                   'Foo', 'Bar'], 
            'last_edit_time': '2007-01-28 08:03:27 GMT', 
            'revision_count': 1, 
            'last_editor': 'bob@example.com', 
            'workspace_name': 'marketing', 
            'type': 'wiki'},
         {'page_uri': 'http://example.com/marketing/index.cgi?test_2', 
            'modified_time': 1169971407, 
            'name': 'Test 2', 
            'uri': 'test_1', 
            'revision_id': 1234567890, 
            'page_id': 'test_2', 
            'tags': [
                   'Hello', 'World'], 
            'last_edit_time': '2007-01-28 08:03:27 GMT', 
            'revision_count': 1, 
            'last_editor': 'joe@example.com', 
            'workspace_name': 'marketing', 
            'type': 'wiki'}])

    def get_data_workspaces_marketing_pages_test_1(self, **kw):
        kw.setdefault('headers', {})
        kw['headers'].setdefault('Accept', 'application/json')
        accept = kw['headers']['Accept']
        if accept == 'application/json':
            page = self.get_data_workspaces_marketing_pages()[1][0]
            return resp(200, page)
        else:
            if accept == 'text/x.socialtext-wiki':
                return resp(200, '\n            [Hello world] This is a wiki!\n            ', headers={'content-type': 'text/x.socialtext-wiki'})
            return resp(200, '\n            <div class="wiki">\n                <a href="#">Hello world</a><p>This is a wiki!</p>\n            </div>\n            ', headers={'content-type': 'text/html'})

    def put_data_workspaces_marketing_pages_Test_1(self, **kw):
        assert_has_keys(kw, required=['data'])
        body = kw['data']
        assert_has_keys(body, required=[
         'content'], optional=[
         'tags', 'edit_summary', 'signal_edit_summary'])
        return resp(204, None)

    def delete_data_workspaces_marketing_pages_test_1(self, **kw):
        return resp(202, None)

    def get_data_workspaces_marketing_pages_test_1_backlinks(self, **kw):
        pg = self.get_data_workspaces_marketing_pages()[1][1]
        return resp(200, [pg])

    def post_data_workspaces_marketing_pages_test_1_comments(self, **kw):
        assert_has_keys(kw, required=['data', 'headers'])
        return resp(204, None)

    def get_data_workspaces_marketing_pages_test_2_frontlinks(self, **kw):
        pg = self.get_data_workspaces_marketing_pages()[1][0]
        return resp(200, [pg])

    def get_data_workspaces_marketing_pages_test_1_revisions(self, **kw):
        return resp(200, [
         {'page_uri': 'http://example.com/marketing/index.cgi?test_1', 
            'modified_time': 1169971407, 
            'name': 'Test 1', 
            'uri': 'test_1', 
            'revision_id': 1234567890, 
            'page_id': 'test_1', 
            'tags': [
                   'Foo', 'Bar'], 
            'last_edit_time': '2007-01-28 08:03:27 GMT', 
            'revision_count': 1, 
            'last_editor': 'bob@example.com', 
            'workspace_name': 'marketing', 
            'type': 'wiki'},
         {'page_uri': 'http://example.com/marketing/index.cgi?test_1', 
            'modified_time': 1169971407, 
            'name': 'Test 1', 
            'uri': 'test_1', 
            'revision_id': 1234567891, 
            'page_id': 'test_1', 
            'tags': [
                   'Foo', 'Bar'], 
            'last_edit_time': '2007-01-28 08:05:32 GMT', 
            'revision_count': 1, 
            'last_editor': 'bob@example.com', 
            'workspace_name': 'marketing', 
            'type': 'wiki'}])

    def get_data_workspaces_marketing_pages_test_1_revisions_1234567890(self, **kw):
        kw.setdefault('headers', {})
        kw['headers'].setdefault('Accept', 'application/json')
        accept = kw['headers']['Accept']
        if accept == 'application/json':
            rev = self.get_data_workspaces_marketing_pages_test_1_revisions()[1][0]
            return resp(200, rev)
        else:
            if accept == 'text/x.socialtext-wiki':
                return resp(200, '\n            [Hello world] This is a wiki!\n            ', headers={'content-type': 'text/x.socialtext-wiki'})
            return resp(200, '\n            <div class="wiki">\n                <a href="#">Hello world</a><p>This is a wiki!</p>\n            </div>\n            ', headers={'content-type': 'text/html'})

    def get_data_workspaces_marketing_pages_test_1_tags(self, **kw):
        return resp(200, [{'name': 'Test', 'page_count': 1, 'uri': '/tags/Test'}])

    def get_data_workspaces_marketing_pages_test_1_tags_Test(self, **kw):
        tag = self.get_data_workspaces_marketing_pages_test_1_tags()[1][0]
        return resp(200, tag)

    def put_data_workspaces_marketing_pages_test_1_tags_Test(self, **kw):
        return resp(201, None)

    def delete_data_workspaces_marketing_pages_test_1_tags_Test(self, **kw):
        return resp(204, None)
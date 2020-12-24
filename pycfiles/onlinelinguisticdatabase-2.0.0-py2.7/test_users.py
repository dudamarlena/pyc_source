# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_users.py
# Compiled at: 2016-09-19 13:27:02
import datetime, logging, os, simplejson as json
from time import sleep
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import User
log = logging.getLogger(__name__)

class TestUsersController(TestController):

    def tearDown(self):
        TestController.tearDown(self, dirs_to_destroy=['user'])

    @nottest
    def test_index(self):
        """Tests that GET /users returns an array of all users and that order_by and pagination parameters work correctly."""

        def create_user_from_index(index):
            user = model.User()
            user.username = 'user_%d' % index
            user.password = 'Aaaaaa_%d' % index
            user.first_name = 'John%d' % index
            user.last_name = 'Doe'
            user.email = 'john.doe@gmail.com'
            user.role = 'viewer'
            return user

        users = [ create_user_from_index(i) for i in range(1, 101) ]
        Session.add_all(users)
        Session.commit()
        users = h.get_users(True)
        users_count = len(users)
        response = self.app.get(url('users'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == users_count
        assert resp[3]['first_name'] == 'John1'
        assert resp[0]['id'] == users[0].id
        assert 'password' not in resp[3]
        assert 'username' not in resp[3]
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('users'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['first_name'] == users[46].first_name
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'User', 'order_by_attribute': 'username', 'order_by_direction': 'desc'}
        response = self.app.get(url('users'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = sorted(users, key=lambda u: u.username, reverse=True)
        assert [ u.id for u in result_set ] == [ u['id'] for u in resp ]
        assert response.content_type == 'application/json'
        params = {'order_by_model': 'User', 'order_by_attribute': 'username', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('users'), params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert result_set[46].first_name == resp['items'][0]['first_name']
        order_by_params = {'order_by_model': 'User', 'order_by_attribute': 'username', 'order_by_direction': 'descending'}
        response = self.app.get(url('users'), order_by_params, status=400, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Userist', 'order_by_attribute': 'nominal', 'order_by_direction': 'desc'}
        response = self.app.get(url('users'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp[0]['id'] == users[0].id
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('users'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('users'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        assert response.content_type == 'application/json'

    @nottest
    def test_create(self):
        """Tests that POST /users creates a new user
        or returns an appropriate error if the input is invalid.
        """
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        original_researchers_directory = os.listdir(self.users_path)
        original_user_count = Session.query(User).count()
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_user_count = Session.query(User).count()
        new_researchers_directory = os.listdir(self.users_path)
        researchers_directory_m_time = os.stat(self.users_path).st_mtime
        assert new_user_count == original_user_count + 1
        assert resp['username'] == 'johndoe'
        assert resp['email'] == 'john.doe@gmail.com'
        assert 'password' not in resp
        assert new_researchers_directory != original_researchers_directory
        assert 'johndoe' in new_researchers_directory
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Zzzzzz_1', 
           'password_confirm': 'Zzzzzz_1', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        researchers_directory = new_researchers_directory
        new_researchers_directory = os.listdir(self.users_path)
        new_researchers_directory_m_time = os.stat(self.users_path).st_mtime
        assert researchers_directory == new_researchers_directory
        assert researchers_directory_m_time == new_researchers_directory_m_time
        assert new_user_count == user_count
        assert resp['errors'] == 'The username johndoe is already taken.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johannes dough', 
           'password': 'Zzzzzz_1', 
           'password_confirm': 'Zzzzzz_1', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == 'The username johannes dough is invalid; only letters of the English alphabet, numbers and the underscore are permitted.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': '', 
           'password': 'Zzzzzz_1', 
           'password_confirm': 'Zzzzzz_1', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == 'A username is required when creating a new user.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': None, 
           'password': 'Zzzzzz_1', 
           'password_confirm': 'Zzzzzz_1', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == 'A username is required when creating a new user.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johannes dough' * 200, 
           'password': 'Zzzzzz_1' * 200, 
           'password_confirm': 'Zzzzzz_1' * 200, 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors']['username'] == 'Enter a value not more than 255 characters long'
        assert resp['errors']['password'] == 'Enter a value not more than 255 characters long'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Zzzzzz_1', 
           'password_confirm': 'Zzzzzzx_1', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == 'The password and password_confirm values do not match.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': '', 
           'password_confirm': '', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == 'A password is required when creating a new user.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': [], 'password_confirm': [], 'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == 'A password is required when creating a new user.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'aA_9', 
           'password_confirm': 'aA_9', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == (' ').join([
         'The submitted password is invalid; valid passwords contain at least 8 characters',
         'and either contain at least one character that is not in the printable ASCII range',
         'or else contain at least one symbol, one digit, one uppercase letter and one lowercase letter.'])
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'abcdefg_9', 
           'password_confirm': 'abcdefg_9', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == (' ').join([
         'The submitted password is invalid; valid passwords contain at least 8 characters',
         'and either contain at least one character that is not in the printable ASCII range',
         'or else contain at least one symbol, one digit, one uppercase letter and one lowercase letter.'])
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'ABCDEFG_9', 
           'password_confirm': 'ABCDEFG_9', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == (' ').join([
         'The submitted password is invalid; valid passwords contain at least 8 characters',
         'and either contain at least one character that is not in the printable ASCII range',
         'or else contain at least one symbol, one digit, one uppercase letter and one lowercase letter.'])
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'abcdefgH9', 
           'password_confirm': 'abcdefgH9', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == (' ').join([
         'The submitted password is invalid; valid passwords contain at least 8 characters',
         'and either contain at least one character that is not in the printable ASCII range',
         'or else contain at least one symbol, one digit, one uppercase letter and one lowercase letter.'])
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'abcdefgH.', 
           'password_confirm': 'abcdefgH.', 
           'first_name': 'Johannes', 
           'last_name': 'Dough', 
           'email': 'johannes.dough@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors'] == (' ').join([
         'The submitted password is invalid; valid passwords contain at least 8 characters',
         'and either contain at least one character that is not in the printable ASCII range',
         'or else contain at least one symbol, one digit, one uppercase letter and one lowercase letter.'])
        assert response.content_type == 'application/json'
        researchers_directory = os.listdir(self.users_path)
        researchers_directory_m_time = os.stat(self.users_path).st_mtime
        sleep(1)
        params = self.user_create_params.copy()
        params.update({'username': 'aadams', 
           'password': 'abcdéfgh', 
           'password_confirm': 'abcdéfgh', 
           'first_name': 'Alexander', 
           'last_name': 'Adams', 
           'email': 'aadams@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        new_researchers_directory = os.listdir(self.users_path)
        new_researchers_directory_m_time = os.stat(self.users_path).st_mtime
        assert 'aadams' not in researchers_directory
        assert 'aadams' in new_researchers_directory
        assert researchers_directory_m_time != new_researchers_directory_m_time
        assert new_user_count == user_count + 1
        assert resp['first_name'] == 'Alexander'
        assert 'password' not in resp
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'xyh', 
           'password': 'abcdéfgh', 
           'password_confirm': 'abcdéfgh', 
           'first_name': '', 
           'last_name': 'Yetzer-Hara', 
           'affiliation': 'here, there, everywhere, ' * 200, 
           'email': 'paradoxofevil@gmail', 
           'role': 'master', 
           'markup_language': 'markdownandupanddown', 
           'page_content': 'My OLD Page\n===============\n\nWhat a great linguistic fieldwork application!\n\n', 
           'input_orthography': 1234})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count
        assert resp['errors']['first_name'] == 'Please enter a value'
        assert resp['errors']['email'] == 'The domain portion of the email address is invalid (the portion after the @: gmail)'
        assert resp['errors']['affiliation'] == 'Enter a value not more than 255 characters long'
        assert resp['errors']['role'] == "Value must be one of: viewer; contributor; administrator (not u'master')"
        assert resp['errors']['input_orthography'] == 'There is no orthography with id 1234.'
        assert resp['errors']['markup_language'] == "Value must be one of: Markdown; reStructuredText (not u'markdownandupanddown')"
        assert response.content_type == 'application/json'
        orthography1 = h.generate_default_orthography1()
        orthography2 = h.generate_default_orthography2()
        Session.add_all([orthography1, orthography2])
        Session.commit()
        orthography1_id = orthography1.id
        orthography2_id = orthography2.id
        params = self.user_create_params.copy()
        params.update({'username': 'alyoshas', 
           'password': 'xY9.Bfx_J Jré', 
           'password_confirm': 'xY9.Bfx_J Jré', 
           'first_name': 'Alexander', 
           'last_name': 'Solzhenitsyn', 
           'email': 'amanaplanacanalpanama@gmail.com', 
           'affiliation': 'Moscow State University', 
           'role': 'contributor', 
           'markup_language': 'Markdown', 
           'page_content': 'My OLD Page\n===============\n\nWhat a great linguistic fieldwork application!\n\n', 
           'input_orthography': orthography1_id, 
           'output_orthography': orthography2_id})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert new_user_count == user_count + 1
        assert resp['username'] == 'alyoshas'
        assert resp['first_name'] == 'Alexander'
        assert resp['last_name'] == 'Solzhenitsyn'
        assert resp['email'] == 'amanaplanacanalpanama@gmail.com'
        assert resp['affiliation'] == 'Moscow State University'
        assert resp['role'] == 'contributor'
        assert resp['markup_language'] == 'Markdown'
        assert resp['page_content'] == 'My OLD Page\n===============\n\nWhat a great linguistic fieldwork application!\n\n'
        assert resp['html'] == h.get_HTML_from_contents(resp['page_content'], 'Markdown')
        assert resp['input_orthography']['id'] == orthography1_id
        assert resp['output_orthography']['id'] == orthography2_id
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_new(self):
        """Tests that GET /users/new returns the data necessary to create a new user.

        The properties of the JSON object are 'roles', 'orthographies' and
        'markup_languages' and their values are arrays/lists.
        """
        response = self.app.get(url('new_user'), extra_environ=self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        application_settings = h.generate_default_application_settings()
        orthography1 = h.generate_default_orthography1()
        orthography2 = h.generate_default_orthography2()
        Session.add_all([application_settings, orthography1, orthography2])
        Session.commit()
        data = {'orthographies': h.get_mini_dicts_getter('Orthography')(), 
           'roles': h.user_roles, 
           'markup_languages': h.markup_languages}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        response = self.app.get(url('new_user'), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['orthographies'] == data['orthographies']
        assert resp['roles'] == data['roles']
        assert resp['markup_languages'] == data['markup_languages']
        assert response.content_type == 'application/json'
        params = {'orthographies': 'anything can go here!'}
        response = self.app.get(url('new_user'), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['orthographies'] == data['orthographies']
        assert resp['roles'] == data['roles']
        assert resp['markup_languages'] == data['markup_languages']
        assert response.content_type == 'application/json'
        params = {'orthographies': datetime.datetime.utcnow().isoformat()}
        response = self.app.get(url('new_user'), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['orthographies'] == data['orthographies']
        assert resp['roles'] == data['roles']
        assert resp['markup_languages'] == data['markup_languages']
        assert response.content_type == 'application/json'
        params = {'orthographies': h.get_most_recent_modification_datetime('Orthography').isoformat()}
        response = self.app.get(url('new_user'), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['orthographies'] == []
        assert resp['roles'] == data['roles']
        assert resp['markup_languages'] == data['markup_languages']
        assert response.content_type == 'application/json'

    @nottest
    def test_update(self):
        """Tests that PUT /users/id updates the user with id=id."""
        default_contributor_id = Session.query(User).filter(User.role == 'contributor').first().id
        def_contrib_environ = {'test.authentication.id': default_contributor_id}
        original_researchers_directory = os.listdir(self.users_path)
        original_user_count = Session.query(User).count()
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        user_id = resp['id']
        datetime_modified = resp['datetime_modified']
        new_user_count = Session.query(User).count()
        new_researchers_directory = os.listdir(self.users_path)
        assert new_user_count == original_user_count + 1
        assert resp['username'] == 'johndoe'
        assert resp['email'] == 'john.doe@gmail.com'
        assert 'password' not in resp
        assert new_researchers_directory != original_researchers_directory
        assert 'johndoe' in new_researchers_directory
        assert response.content_type == 'application/json'
        sleep(1)
        params = self.user_create_params.copy()
        params.update({'username': 'johnbuck', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'contributor'})
        params = json.dumps(params)
        response = self.app.put(url('user', id=user_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_datetime_modified = resp['datetime_modified']
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        researchers_directory = new_researchers_directory
        new_researchers_directory = os.listdir(self.users_path)
        assert user_count == new_user_count
        assert new_datetime_modified != datetime_modified
        assert resp['username'] == 'johnbuck'
        assert resp['role'] == 'contributor'
        assert resp['last_name'] == 'Doe'
        assert researchers_directory != new_researchers_directory
        assert 'johndoe' in researchers_directory and 'johndoe' not in new_researchers_directory
        assert 'johnbuck' in new_researchers_directory and 'johnbuck' not in researchers_directory
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johnbuck', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Buck', 
           'email': 'john.doe@gmail.com', 
           'role': 'contributor'})
        params = json.dumps(params)
        response = self.app.put(url('user', id=user_id), params, self.json_headers, def_contrib_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        user_environ = {'test.authentication.id': user_id}
        params = self.user_create_params.copy()
        params.update({'username': 'johnbuck', 
           'password': 'Zzzzzz.9', 
           'password_confirm': 'Zzzzzz.9', 
           'first_name': 'John', 
           'last_name': 'Buck', 
           'email': 'john.doe@gmail.com', 
           'role': 'contributor'})
        params = json.dumps(params)
        response = self.app.put(url('user', id=user_id), params, self.json_headers, user_environ)
        resp = json.loads(response.body)
        user_just_updated = Session.query(User).get(user_id)
        assert resp['username'] == 'johnbuck'
        assert resp['last_name'] == 'Buck'
        assert h.encrypt_password('Zzzzzz.9', str(user_just_updated.salt)) == user_just_updated.password
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'iroc_z', 
           'password': 'Zzzzzz.9', 
           'password_confirm': 'Zzzzzz.9', 
           'first_name': 'John', 
           'last_name': 'Buck', 
           'email': 'john.doe@gmail.com', 
           'role': 'contributor'})
        params = json.dumps(params)
        response = self.app.put(url('user', id=user_id), params, self.json_headers, user_environ, status=400)
        resp = json.loads(response.body)
        assert resp['errors'] == 'Only administrators can update usernames.'
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'username': 'johnbuck', 
           'password': 'Zzzzzz.9', 
           'password_confirm': 'Zzzzzz.9', 
           'first_name': 'John', 
           'last_name': 'Buck', 
           'email': 'john.doe@gmail.com', 
           'role': 'administrator'})
        params = json.dumps(params)
        response = self.app.put(url('user', id=user_id), params, self.json_headers, user_environ, status=400)
        resp = json.loads(response.body)
        assert resp['errors'] == 'Only administrators can update roles.'
        assert response.content_type == 'application/json'
        md_contents = ('\n').join([
         'My Page',
         '=======',
         '',
         'Research Interests',
         '---------------------',
         '',
         '* Item 1',
         '* Item 2',
         ''])
        params = self.user_create_params.copy()
        params.update({'first_name': 'John', 
           'last_name': 'Buckley', 
           'email': 'john.doe@gmail.com', 
           'role': 'contributor', 
           'markup_language': 'Markdown', 
           'page_content': md_contents})
        params = json.dumps(params)
        response = self.app.put(url('user', id=user_id), params, self.json_headers, user_environ)
        resp = json.loads(response.body)
        user_just_updated = Session.query(User).get(user_id)
        assert resp['username'] == 'johnbuck'
        assert resp['last_name'] == 'Buckley'
        assert h.encrypt_password('Zzzzzz.9', str(user_just_updated.salt)) == user_just_updated.password
        assert resp['html'] == h.get_HTML_from_contents(md_contents, 'Markdown')
        assert response.content_type == 'application/json'
        params = self.user_create_params.copy()
        params.update({'first_name': 'John', 
           'last_name': 'Buckley', 
           'email': 'john.doe@gmail.com', 
           'role': 'contributor', 
           'markup_language': 'Markdown', 
           'page_content': md_contents})
        params = json.dumps(params)
        response = self.app.put(url('user', id=user_id), params, self.json_headers, user_environ, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'

    @nottest
    def test_delete(self):
        """Tests that DELETE /users/id deletes the user with id=id."""
        original_researchers_directory = os.listdir(self.users_path)
        original_user_count = Session.query(User).count()
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        user_id = resp['id']
        datetime_modified = resp['datetime_modified']
        new_user_count = Session.query(User).count()
        new_researchers_directory = os.listdir(self.users_path)
        researchers_directory_m_time = os.stat(self.users_path).st_mtime
        assert new_user_count == original_user_count + 1
        assert resp['username'] == 'johndoe'
        assert resp['email'] == 'john.doe@gmail.com'
        assert 'password' not in resp
        assert new_researchers_directory != original_researchers_directory
        assert 'johndoe' in new_researchers_directory
        f = open(os.path.join(self.users_path, 'johndoe', 'test_file.txt'), 'w')
        f.write('Some content here.')
        f.close()
        assert 'test_file.txt' in os.listdir(os.path.join(self.users_path, 'johndoe'))
        response = self.app.delete(url('user', id=user_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        researchers_directory = new_researchers_directory
        new_researchers_directory = os.listdir(self.users_path)
        deleted_user = Session.query(User).get(user_id)
        assert deleted_user is None
        assert new_user_count == user_count - 1
        assert resp['id'] == user_id
        assert 'password' not in resp
        assert resp['username'] == 'johndoe'
        assert researchers_directory != new_researchers_directory
        assert 'johndoe' not in new_researchers_directory and 'johndoe' in researchers_directory
        assert response.content_type == 'application/json'
        original_researchers_directory = os.listdir(self.users_path)
        original_user_count = Session.query(User).count()
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        user_id = resp['id']
        new_user_count = Session.query(User).count()
        new_researchers_directory = os.listdir(self.users_path)
        assert new_user_count == original_user_count + 1
        assert resp['username'] == 'johndoe'
        assert resp['email'] == 'john.doe@gmail.com'
        assert 'password' not in resp
        assert new_researchers_directory != original_researchers_directory
        assert 'johndoe' in new_researchers_directory
        assert response.content_type == 'application/json'
        user_environ = {'test.authentication.id': user_id}
        response = self.app.delete(url('user', id=user_id), headers=self.json_headers, extra_environ=user_environ, status=403)
        resp = json.loads(response.body)
        user_count = new_user_count
        new_user_count = Session.query(User).count()
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        id = 9999999999999
        response = self.app.delete(url('user', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no user with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('user', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_show(self):
        """Tests that GET /users/id returns the user with id=id or an appropriate error."""
        original_researchers_directory = os.listdir(self.users_path)
        original_user_count = Session.query(User).count()
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        user_id = resp['id']
        new_user_count = Session.query(User).count()
        new_researchers_directory = os.listdir(self.users_path)
        assert new_user_count == original_user_count + 1
        assert resp['username'] == 'johndoe'
        assert resp['email'] == 'john.doe@gmail.com'
        assert 'password' not in resp
        assert new_researchers_directory != original_researchers_directory
        assert 'johndoe' in new_researchers_directory
        id = 100000000000
        response = self.app.get(url('user', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no user with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('user', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('user', id=user_id), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert 'username' not in resp
        assert 'password' not in resp
        assert resp['email'] == 'john.doe@gmail.com'
        assert response.content_type == 'application/json'

    @nottest
    def test_edit(self):
        """Tests that GET /users/id/edit returns a JSON object of data necessary to edit the user with id=id.

        The JSON object is of the form {'user': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """
        orthography1 = h.generate_default_orthography1()
        orthography2 = h.generate_default_orthography2()
        Session.add_all([orthography1, orthography2])
        Session.commit()
        data = {'orthographies': h.get_mini_dicts_getter('Orthography')(), 
           'roles': h.user_roles, 
           'markup_languages': h.markup_languages}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        original_researchers_directory = os.listdir(self.users_path)
        original_user_count = Session.query(User).count()
        params = self.user_create_params.copy()
        params.update({'username': 'johndoe', 
           'password': 'Aaaaaa_1', 
           'password_confirm': 'Aaaaaa_1', 
           'first_name': 'John', 
           'last_name': 'Doe', 
           'email': 'john.doe@gmail.com', 
           'role': 'viewer'})
        params = json.dumps(params)
        response = self.app.post(url('users'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        user_id = resp['id']
        new_user_count = Session.query(User).count()
        new_researchers_directory = os.listdir(self.users_path)
        assert new_user_count == original_user_count + 1
        assert resp['username'] == 'johndoe'
        assert resp['email'] == 'john.doe@gmail.com'
        assert 'password' not in resp
        assert new_researchers_directory != original_researchers_directory
        assert 'johndoe' in new_researchers_directory
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_user', id=user_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_user', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no user with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_user', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_user', id=user_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['user']['username'] == 'johndoe'
        assert resp['data']['orthographies'] == data['orthographies']
        assert resp['data']['roles'] == data['roles']
        assert resp['data']['markup_languages'] == data['markup_languages']
        assert response.content_type == 'application/json'
        user_environ = {'test.authentication.id': user_id}
        params = {'orthographies': h.get_most_recent_modification_datetime('Orthography').isoformat()}
        response = self.app.get(url('edit_user', id=user_id), params, headers=self.json_headers, extra_environ=user_environ)
        resp = json.loads(response.body)
        assert resp['user']['username'] == 'johndoe'
        assert resp['data']['orthographies'] == []
        assert resp['data']['roles'] == data['roles']
        assert resp['data']['markup_languages'] == data['markup_languages']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_user', id=user_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
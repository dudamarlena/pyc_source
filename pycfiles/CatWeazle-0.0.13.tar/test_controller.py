# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/catwalk/tg2/test/test_controller.py
# Compiled at: 2009-02-02 23:09:07
import os, sys, catwalk
from tg.test_stack import TestConfig, app_from_config
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catwalk.tg2.test.model import metadata, DBSession
root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, root)
test_db_path = 'sqlite:///' + root + '/test.db'
paths = Bunch(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=os.path.join(root, 'templates'))
base_config = TestConfig(folder='rendering', values={'use_sqlalchemy': True, 'model': catwalk.tg2.test.model, 
   'session': catwalk.tg2.test.model.DBSession, 
   'pylons.helpers': Bunch(), 
   'use_legacy_renderer': False, 
   'use_dotted_templatenames': True, 
   'paths': paths, 
   'package': catwalk.tg2.test, 
   'sqlalchemy.url': test_db_path})

def setup():
    engine = create_engine(test_db_path)
    metadata.bind = engine
    metadata.drop_all()
    metadata.create_all()
    session = sessionmaker(bind=engine)()
    setup_records(session)
    session.commit()


def teardown():
    os.remove(test_db_path[10:])


class TestCatwalkController:

    def __init__(self, *args, **kargs):
        self.app = app_from_config(base_config)

    def test_index(self):
        resp = self.app.get('/catwalk').follow()
        assert 'Document' in resp, resp

    def test_list_documents(self):
        resp = self.app.get('/catwalk/Document').follow()
        assert '</thead>\n    <tbody>\n    </tbody>\n</table>\n      No Records Found.\n</div>\n      </div>\n' in resp, resp

    def test_documents_new(self):
        resp = self.app.get('/catwalk/Document/new')
        assert '<tr id="blob.container" class="even" title="">\n            <td class="labelcol">\n                <label id="blob.label" for="blob" class="fieldlabel">Blob</label>\n            </td>\n            <td class="fieldcol">\n                <input type="file" name="blob" class="filefield" id="blob" value="" />\n            </td>\n        </tr>' in resp, resp

    def test_documents_metadata(self):
        resp = self.app.get('/catwalk/Document/metadata')
        assert '<td>\n        String(length=500, convert_unicode=False, assert_unicode=None)\n    </td>\n</tr>\n<tr class="even">\n    <td>\n        address\n    </td>\n    <td>\n        relation\n    </td>\n' in resp, resp

    def test_get_users(self):
        resp = self.app.get('/catwalk/User/')
        assert '<td>\n            <a href="./1/edit">edit</a> |\n            <a href="./1/delete">delete</a>\n            </td>\n            <td>******</td><td>1</td><td>someone</td><td>asdf@asdf.com</td>' in resp, resp

    def test_get_users_json(self):
        resp = self.app.get('/catwalk/User.json')
        assert '{}' in resp, resp

    def test_edit_user(self):
        resp = self.app.get('/catwalk/User/1/edit')
        assert '<td class="fieldcol">\n                <select name="town" class="propertysingleselectfield" id="town">\n        <option value="1" selected="selected">Arvada</option><option value="2">Denver</option><option value="3">Golden</option><option value="4">Boulder</option><option value="">-----------</option>\n</select>\n            </td>\n        </tr><tr id="password.container" class="even" title="">\n            <td class="labelcol">\n                <label id="password.label" for="password" class="fieldlabel">Password</label>\n            </td>\n            <td class="fieldcol">\n                <input type="password" name="password" class="passwordfield" id="password" value="" />\n            </td>' in resp, resp

    def test_edit_user_success(self):
        resp = self.app.post('/catwalk/User/1/', params={'sprox_id': 'put__User', '_method': 'PUT', 
           'user_name': 'someone', 
           'display_name': 'someone2', 
           'email_address': 'asdf2@asdf2.com', 
           '_password': 'pass', 
           'password': 'pass', 
           'town': '1', 
           'town_id': '1', 
           'user_id': '1', 
           'created': '2009-01-11 13:54:01'}).follow()
        assert '<td>******</td><td>1</td><td>someone</td><td>asdf2@asdf2.com</td>' in resp, resp
        resp = self.app.post('/catwalk/User/1/', params={'sprox_id': 'put__User', '_method': 'PUT', 
           'user_name': 'someone', 
           'display_name': 'someone2', 
           'email_address': 'asdf@asdf.com', 
           '_password': 'pass', 
           'password': 'pass', 
           'town': '1', 
           'town_id': '1', 
           'user_id': '1', 
           'created': '2009-01-11 13:54:01'}).follow()
        assert '<td>******</td><td>1</td><td>someone</td><td>asdf@asdf.com</td>' in resp, resp

    def test_add_and_remove_user(self):
        resp = self.app.post('/catwalk/User/', params={'sprox_id': 'add__User', 'user_name': 'someone', 
           'display_name': 'someone2', 
           'email_address': 'asdf2@asdf2.com', 
           '_password': 'pass', 
           'password': 'pass', 
           'town': '1', 
           'town_id': '1', 
           'user_id': '2', 
           'created': '2009-01-11 13:54:01'}).follow()
        assert '<td>asdf2@asdf2' in resp, resp
        resp = self.app.get('/catwalk/User/2/', params={'user_id': '2', '_method': 'DELETE'}).follow()
        assert 'asdf2@asdf2' not in resp, resp

    def test_add_user_existing_username(self):
        resp = self.app.post('/catwalk/User/create', params={'sprox_id': 'add__User', 'user_name': 'asdf', 
           'display_name': 'someone2', 
           'email_address': 'asdf2@asdf2.com', 
           '_password': 'pass', 
           'password': 'pass', 
           'town': '1', 
           'town_id': '1', 
           'user_id': '2', 
           'created': '2009-01-11 13:54:01'})
        assert 'That value already exists' in resp, resp
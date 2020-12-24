# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/dbmechanic/frameworks/tg2/test/testDBMechanic.py
# Compiled at: 2008-06-30 11:43:47
import os, sys, os.path, pkg_resources
from routes import url_for
from sqlalchemy.orm import sessionmaker, scoped_session
from tg.tests.base import TestWSGIController, make_app
from webob import Request, Response
from paste.deploy import loadapp
from paste.fixture import TestApp
from pprint import pprint
from nose.tools import eq_
app = None

def setup():
    global app
    here_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.join(here_dir, 'TG2TestApp')
    pkg_resources.working_set.add_entry(proj_dir)
    from tg2testapp.model import DBSession, metadata, User, Group
    app = loadapp('config:development.ini', relative_to=proj_dir)
    app = TestApp(app)
    metadata.drop_all()
    metadata.create_all()
    session = DBSession
    user = User()
    user.user_name = 'asdf'
    user.email = 'asdf@asdf.com'
    user.password = 'asdf'
    session.save(user)
    for i in range(50):
        group = Group()
        group.group_name = unicode(i)
        session.save(group)
        user.groups.append(group)

    session.save(user)
    session.commit()
    session.flush()


def teardown():
    from tg2testapp.model import User, Group, DBSession as session, metadata
    del metadata


class TestDBMechanic:

    def setup(self):
        from tg2testapp.model import users_table, user_group_table, groups_table
        users_table.delete().execute()
        groups_table.delete().execute()
        user_group_table.delete().execute()

    def testDatabaseView(self):
        resp = app.get('/dbmechanic')
        s = resp.body
        assert '<div class="tablelabelwidget">\n<a href="/dbmechanic/tableView/town_table">town_table</a>\n</div>\n<input type="hidden" name="dbsprockets_id" class="hiddenfield" id="databaseView_dbsprockets_id" value="test_tabletg_grouppermissionvisituser_groupvisit_identitygroup_permissiontg_usertown_table">\n</div>\n      </div>\n      <div class="mainView" style="bg-color:#ffffff;">\n      </div>\n<!--  <div py:for="js in tg_js_bodybottom" py:replace="ET(js.display())" />-->\n  <!-- End of main_content -->\n  </div>\n  <div id="footer">\n       <p>TurboGears 2 is a open source front-to-back web development framework written in Python</p>\n       <p>Copyright (c) 2005-2008 </p>\n  </div>\n</body>\n</html>' in s, 'actual: %s' % s

    def testTableDef(self):
        resp = app.get('/dbmechanic/tableDef/tg_user')
        value = resp.body
        assert '<tr class="tabledefwidget">\n    <td>\n        created\n    </td>\n    <td>\n    DateTime(timezone=False)\n    </td>\n</tr>\n<input type="hidden" name="dbsprockets_id" class="hiddenfield" id="tableDef__tg_user_dbsprockets_id" value="">\n</table>\n      </div>' in value, value

    def testTableView(self):
        from tg2testapp.model import User, Group, DBSession as session
        u = User()
        u.user_name = 'userTableView'
        u.password = 'asdf'
        u.email_address = 'asdftableView@asdf.com'
        session.save(u)
        group = Group()
        group.group_name = 'table_view_group'
        group.display_name = 'group'
        session.save(group)
        session.flush()
        resp = app.get('/dbmechanic/tableView/tg_user')
        value = resp.body
        assert '<thead>\n        <tr>\n            <th class="col_0">\n            </th><th class="col_1">\n            user_id\n            </th><th class="col_2">\n            user_name\n            </th><th class="col_3">\n            email_address\n            </th><th class="col_4">\n            display_name\n            </th><th class="col_5">\n            password\n            </th><th class="col_6">\n            town\n            </th><th class="col_7">\n            created\n            </th><th class="col_8">\n            tg_groups\n            </th>\n        </tr>\n    </thead>\n    <tbody>\n        <tr class="even">\n            <td><a href="/dbmechanic/editRecord/tg_user?user_id=1">'
        (
         '<td></td><td></td><td>******</td><td>' in value, value)

    def testAddRecord(self):
        resp = app.get('/dbmechanic/addRecord/tg_user')
        value = resp.body
        assert '<td>\n                <div>\n    <input type="text" id="addRecord__tg_user_created" class="dbsprocketscalendardatetimepicker" name="created" value="2007-12-21 19:02:25" />\n    <input type="button" id="addRecord__tg_user_created_trigger" class="date_field_button" value="Choose" />\n</div>\n            </td>\n        </tr><tr class="even">\n            <th>\n            </th>\n            <td>\n                <input type="submit" class="submitbutton" id="addRecord__tg_user_submit" value="Submit" />\n            </td>\n        </tr>\n    </table>'

    def testEditRecord(self):
        from tg2testapp.model import User, Group, DBSession as session
        u = User()
        u.user_name = 'user3'
        u.password = 'asdf'
        u.email_address = 'asdf@asdf2.com'
        session.save(u)
        group = Group()
        group.group_name = 'table_view_group'
        group.display_name = 'group'
        session.save(group)
        session.flush()
        resp = app.get('/dbmechanic/editRecord/tg_user?user_id=1')
        value = resp.body
        assert '<td>\n                <div>\n    <input type="text" id="editRecord__tg_user_created" class="dbsprocketscalendardatetimepicker" name="created" value="2007-12-21 20:45:00" />\n    <input type="button" id="editRecord__tg_user_created_trigger" class="date_field_button" value="Choose" />\n</div>\n            </td>\n        </tr><tr class="even">\n            <th>\n            </th>\n            <td>\n                <input type="submit" class="submitbutton" id="editRecord__tg_user_submit" value="Submit" />\n            </td>\n        </tr>\n    </table>\n</form>'

    def testAdd(self):
        resp = app.get('/dbmechanic/addRecord/tg_user')
        value = resp.body
        resp = app.get('/dbmechanic/add/tg_user', params=dict(user_id=None, user_name='new_user', email_address='new@user.com', dbsprockets_id='addRecord__tg_user'))
        actual = resp.namespace
        expected = {'controller': '/dbmechanic', 'tableName': 'tg_user'}
        mainValue = {'town': None, 'user_id': 1, 
           'email_address': 'new@user.com', 
           'tg_groups': '', 
           'display_name': None, 
           'password': '******', 
           'user_name': 'new_user'}
        for (key, value) in expected.iteritems():
            yield (eq_, value, actual[key])

        return

    def testEdit(self):
        from tg2testapp.model import User, Group, DBSession as session
        u = User()
        u.user_name = 'userTestEdit'
        u.password = 'asdf'
        u.email_address = 'test@edit.com'
        session.save(u)
        session.commit()
        session.flush()
        u_id = str(u.user_id)
        resp = app.get('/dbmechanic/editRecord/tg_user?user_id=' + u_id)
        value = resp.body
        resp = app.get('/dbmechanic/edit/tg_user', params=dict(user_id=u_id, user_name='new_username', email_address='newemail@user.com', dbsprockets_id='editRecord__tg_user'))
        actual = resp.follow().namespace
        expected = {'controller': '/dbmechanic', 'recordsPerPage': 25, 
           'tableName': 'tg_user', 
           'mainCount': 1, 
           'page': 1}
        mainValue = {'town': None, 'user_id': 1, 
           'email_address': 'newemail@user.com', 
           'tg_groups': '', 
           'display_name': None, 
           'password': '******', 
           'user_name': 'new_username'}
        for (key, value) in expected.iteritems():
            yield (eq_, value, actual[key])

        actualRow = actual['mainValue'][0]
        for (key, value) in mainValue.iteritems():
            yield (eq_, value, actualRow[key])

        return

    def testCreateRelationships(self):
        from tg2testapp.model import User, Group, DBSession as session
        u = User()
        u.user_name = 'userCreateRel'
        u.password = 'asdf'
        u.email_address = 'create@relationships.com'
        session.save(u)
        session.commit()
        group = Group()
        group.group_name = 'create_rel_group'
        group.display_name = 'group'
        session.save(group)
        session.flush()
        u_id = str(u.user_id)
        resp = app.get('/dbmechanic/edit/tg_user', params=dict(user_id=u_id, user_name='new_username', email_address='newemail@user.com', dbsprockets_id='editRecord__tg_user', many_many_tg_group='1'))

    def testCreateRelationshipsManyMany(self):
        from tg2testapp.model import user_group_table
        user_group_table.insert(values=dict(user_id=1, group_id=2)).execute()
        resp = app.get('/dbmechanic/edit/user_group', params=dict(dbsprockets_id='editRecord__user_group', user_id=1, group_id=2))

    def testEdit(self):
        from tg2testapp.model import User, Group, DBSession as session
        u = User()
        u.user_name = 'userTestEdit'
        u.password = 'asdf'
        u.email_address = 'test@edit.com'
        session.save(u)
        session.commit()
        session.flush()
        u_id = str(u.user_id)
        resp = app.get('/dbmechanic/delete/tg_user?user_id=' + u_id)
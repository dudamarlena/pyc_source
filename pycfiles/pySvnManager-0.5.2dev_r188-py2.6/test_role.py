# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/tests/functional/test_role.py
# Compiled at: 2010-08-08 03:18:44
from pysvnmanager.tests import *
from pysvnmanager.controllers import role

class TestRoleController(TestController):

    def test_index(self):
        res = self.app.get(url(controller='role', action='index'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='role', action='index'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('admin2')
        res = self.app.get(url(controller='role', action='index'))
        assert res.status == '200 OK', res.status
        assert '\n  <input type="button" class="input-button" name="save_btn"   value=\'Save\'  onClick="do_save(this.form)" DISABLED>\n  <input type="button" class="input-button" name="delete_btn" value=\'Delete\' onClick="do_delete(this.form)" DISABLED>\n  <input type="button" class="input-button" name="cancel_btn" value=\'Cancel\' onClick="role_changed()" DISABLED>' in res.body, res.body[-700:]
        self.login('root')
        res = self.app.get(url(controller='role', action='index'))
        assert res.status == '200 OK', res.status
        assert '<input type="button" class="input-button" name="save_btn"   value=\'Save\'' in res.body, res.body

    def test_get_role_info(self):
        res = self.app.get(url(controller='role', action='get_role_info'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='role', action='get_role_info'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('root')
        params = {'role': ''}
        res = self.app.get(url(controller='role', action='get_role_info'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="...";name[0]="Please choose...";\nid[1]="@admin";name[1]="Group:admin";\nid[2]="@all";name[2]="Group:all";\nid[3]="@biz";name[3]="Group:biz";\nid[4]="@dev";name[4]="Group:dev";\nid[5]="@group1";name[5]="Group:group1";\nid[6]="@group2";name[6]="Group:group2";\nid[7]="@group3";name[7]="Group:group3";\nid[8]="@office";name[8]="Group:office";\nid[9]="@tech";name[9]="Group:tech";\nid[10]="@test";name[10]="Group:test";\nid[11]="&admin";name[11]="Alias:admin";\nid[12]="&pm";name[12]="Alias:pm";\nid[13]="&tm";name[13]="Alias:tm";\nmembers_count=14;\nrevision="0.2.1";\n' == res.body, res.body
        params = {'role': '@admin'}
        res = self.app.get(url(controller='role', action='get_role_info'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="&admin";name[0]="Alias:admin";\nid[1]="admin1";name[1]="admin1";\nid[2]="admin2";name[2]="admin2";\nid[3]="admin3";name[3]="admin3";\nmembers_count=4;\nrevision="0.2.1";\n' == res.body, res.body
        params = {'role': '@group1'}
        res = self.app.get(url(controller='role', action='get_role_info'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="@group2";name[0]="Group:group2";\nid[1]="@group3";name[1]="Group:group3";\nid[2]="user1";name[2]="user1";\nid[3]="user11";name[3]="user11";\nid[4]="user12";name[4]="user12";\nmembers_count=5;\nrevision="0.2.1";\n' == res.body, res.body
        params = {'role': '@group3'}
        res = self.app.get(url(controller='role', action='get_role_info'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="user3";name[0]="user3";\nid[1]="user31";name[1]="user31";\nid[2]="user32";name[2]="user32";\nmembers_count=3;\nrevision="0.2.1";\n' == res.body, res.body
        params = {'role': '&admin'}
        res = self.app.get(url(controller='role', action='get_role_info'), params)
        assert res.status == '200 OK', res.status
        assert 'aliasname = "&admin";username = "jiangxin";\nrevision="0.2.1";\n' == res.body, res.body

    def test_save_group(self):
        res = self.app.get(url(controller='role', action='save_group'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='role', action='save_group'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('@group3')
            self.assert_(unicode(userobj) == 'group3 = user3, user31, user32', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'rolename': 'group3', 'members': '蒋鑫, user3,@group1', 'autodrop': 'no'}
            res = self.app.get(url(controller='role', action='save_group'), params)
            assert res.status == '200 OK', res.status
            assert 'Recursive group membership for @group1' in res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('@group3')
            self.assert_(unicode(userobj) == 'group3 = user3, user31, user32', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('@group3')
            self.assert_(unicode(userobj) == 'group3 = user3, user31, user32', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'rolename': 'group3', 'members': '蒋鑫, user3,@group1', 'autodrop': 'yes'}
            res = self.app.get(url(controller='role', action='save_group'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('@group3')
            self.assert_(unicode(userobj) == 'group3 = user3, 蒋鑫', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('@管理员组')
            self.assert_(userobj == None)
            self.login('root')
            params = {'rolename': '管理员组', 'members': '蒋鑫, user3,@group1'}
            res = self.app.get(url(controller='role', action='save_group'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('@管理员组')
            self.assert_(unicode(userobj) == '管理员组 = @group1, user3, 蒋鑫', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('@管理员组')
            self.assert_(userobj == None)
            self.login('root')
            params = {'rolename': '管理员组', 'members': '蒋鑫, user3,@group1', 'revision': ''}
            res = self.app.get(url(controller='role', action='save_group'), params)
            assert res.status == '200 OK', res.status
            assert 'Update failed! You are working on a out-of-date revision.' in res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('@管理员组')
            self.assert_(userobj == None)
        finally:
            self.rollback()

        return

    def test_delete_group(self):
        res = self.app.get(url(controller='role', action='delete_group'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='role', action='delete_group'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('@group3')
            self.assert_(unicode(userobj) == 'group3 = user3, user31, user32', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'role': 'group3'}
            res = self.app.get(url(controller='role', action='delete_group'), params)
            assert res.status == '200 OK', res.status
            assert 'Group group3 is referenced by group @group1.' in res.body, res.body
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('@dev')
            self.assert_(unicode(userobj) == 'dev = dev1, dev2, dev3', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'role': '@dev'}
            res = self.app.get(url(controller='role', action='delete_group'), params)
            assert res.status == '200 OK', res.status
            assert '@dev is referenced by [/:/trunk].' in res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('@dev')
            self.assert_(unicode(userobj) == 'dev = dev1, dev2, dev3', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('@all')
            self.assert_(unicode(userobj) == 'all = @admin, @dev, @test', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'role': 'all'}
            res = self.app.get(url(controller='role', action='delete_group'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('@all')
            self.assert_(userobj == None)
        finally:
            self.rollback()

        return

    def test_save_alias(self):
        res = self.app.get(url(controller='role', action='save_alias'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='role', action='save_alias'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('&admin')
            self.assert_(unicode(userobj) == 'admin = jiangxin', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'aliasname': 'admin', 'username': '蒋鑫'}
            res = self.app.get(url(controller='role', action='save_alias'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('&admin')
            self.assert_(unicode(userobj) == 'admin = 蒋鑫', unicode(userobj).encode('utf-8'))
            self.assert_(authz.is_super_user('&admin') == True, authz.is_super_user('&admin'))
            self.assert_(authz.is_super_user('蒋鑫') == True, authz.is_super_user('蒋鑫'))
            self.login('蒋鑫')
            params = {'aliasname': 'admin2', 'username': 'jiangxin'}
            res = self.app.get(url(controller='role', action='save_alias'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('&管理员')
            self.assert_(userobj == None)
            self.login('root')
            params = {'aliasname': '管理员', 'username': '蒋鑫'}
            res = self.app.get(url(controller='role', action='save_alias'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('&管理员')
            self.assert_(unicode(userobj) == '管理员 = 蒋鑫', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('&admin')
            self.assert_(unicode(userobj) == 'admin = jiangxin', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'aliasname': 'admin', 'username': '蒋鑫', 'revision': '123'}
            res = self.app.get(url(controller='role', action='save_alias'), params)
            assert res.status == '200 OK', res.status
            assert 'Update failed! You are working on a out-of-date revision.' in res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('&admin')
            self.assert_(unicode(userobj) == 'admin = jiangxin', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        return

    def test_delete_alias(self):
        res = self.app.get(url(controller='role', action='delete_alias'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='role', action='delete_alias'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('&tm')
            self.assert_(unicode(userobj) == 'tm = test1', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'aliasname': 'tm'}
            res = self.app.get(url(controller='role', action='delete_alias'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('&tm')
            self.assert_(userobj == None)
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('&tm')
            self.assert_(unicode(userobj) == 'tm = test1', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'aliasname': 'tm', 'revision': ''}
            res = self.app.get(url(controller='role', action='delete_alias'), params)
            assert res.status == '200 OK', res.status
            assert 'Update failed! You are working on a out-of-date revision.' in res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('&tm')
            self.assert_(unicode(userobj) == 'tm = test1', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            userobj = authz.get_userobj('&pm')
            self.assert_(unicode(userobj) == 'pm = dev1', unicode(userobj).encode('utf-8'))
            self.login('root')
            params = {'aliasname': 'pm', 'revision': ''}
            res = self.app.get(url(controller='role', action='delete_alias'), params)
            assert res.status == '200 OK', res.status
            assert '&pm is referenced by [/:/trunk].' in res.body, res.body
            authz = self.load_authz()
            userobj = authz.get_userobj('&pm')
            self.assert_(unicode(userobj) == 'pm = dev1', unicode(userobj).encode('utf-8'))
        finally:
            self.rollback()

        return
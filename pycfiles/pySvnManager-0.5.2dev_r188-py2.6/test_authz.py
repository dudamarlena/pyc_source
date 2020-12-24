# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/tests/functional/test_authz.py
# Compiled at: 2010-08-08 03:18:44
from pysvnmanager.tests import *
from pysvnmanager.controllers import authz

class TestAuthzController(TestController):

    def test_index(self):
        res = self.app.get(url(controller='authz', action='index'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res
        self.login('nobody')
        res = self.app.get(url(controller='authz', action='index'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.header
        self.login('admin2')
        res = self.app.get(url(controller='authz', action='index'))
        assert res.status == '200 OK', res.status
        assert (',').join(sorted(res.tmpl_context.reposlist)) == 'repos1,repos2', res.tmpl_context.reposlist
        assert '<input type="button" name="save_btn"   value=\'Save\'' in res.body, res.body
        self.login('root')
        res = self.app.get(url(controller='authz', action='index'))
        assert res.status == '200 OK', res.status
        assert (',').join(sorted(res.tmpl_context.reposlist)) == '/,document,repos1,repos2,repos3', res.tmpl_context.reposlist
        assert '<input type="button" name="save_btn"   value=\'Save\'' in res.body, res.body

    def test_init_repos_list(self):
        res = self.app.get(url(controller='authz', action='init_repos_list'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='authz', action='init_repos_list'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('root')
        res = self.app.get(url(controller='authz', action='init_repos_list'))
        assert res.status == '200 OK', res.status
        assert 'id[0]="...";name[0]="Please choose...";\nid[1]="/";name[1]="/";\nid[2]="repos3";name[2]="repos3";\nid[3]="document";name[3]="document (?)";\nid[4]="repos1";name[4]="repos1 (?)";\nid[5]="repos2";name[5]="repos2 (?)";\nid[6]="project1";name[6]="project1 (!)";\nid[7]="project2";name[7]="project2 (!)";\ntotal=8;\nrevision="0.2.1";\n' == res.body, res.body

    def test_repos_changed(self):
        res = self.app.get(url(controller='authz', action='repos_changed'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='authz', action='repos_changed'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('root')
        params = {'select': '/'}
        res = self.app.get(url(controller='authz', action='repos_changed'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="...";name[0]="Please choose...";\nid[1]="/trunk/src";name[1]="/trunk/src";\nid[2]="/trunk";name[2]="/trunk";\nid[3]="/";name[3]="/";\nid[4]="/tags";name[4]="/tags";\nid[5]="/branches";name[5]="/branches";\ntotal=6;\nadmin_users="&admin, root";\nrevision="0.2.1";\n' == res.body, res.body
        params = {'select': 'repos1'}
        res = self.app.get(url(controller='authz', action='repos_changed'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="...";name[0]="Please choose...";\nid[1]="/trunk/src";name[1]="/trunk/src";\nid[2]="/trunk";name[2]="/trunk";\nid[3]="/";name[3]="/";\ntotal=4;\nadmin_users="@admin";\nrevision="0.2.1";\n' == res.body, res.body

    def test_path_changed(self):
        params = {}
        res = self.app.get(url(controller='authz', action='path_changed'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='authz', action='path_changed'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('root')
        params = {'reposname': '/', 'path': '/tags//'}
        res = self.app.get(url(controller='authz', action='path_changed'), params)
        assert res.status == '200 OK', res.status
        assert 'user[0]="&pm";\nrights[0]="rw";\nuser[1]="$authenticated";\nrights[1]="r";\ntotal=2;\nrevision="0.2.1";\n' == res.body, res.body
        self.login('root')
        params = {'reposname': 'document', 'path': '/trunk/商务部'}
        res = self.app.get(url(controller='authz', action='path_changed'), params)
        assert res.status == '200 OK', res.status
        assert 'user[0]="*";\nrights[0]="";\nuser[1]="@admin";\nrights[1]="rw";\nuser[2]="@biz";\nrights[2]="rw";\ntotal=3;\nrevision="0.2.1";\n' == res.body, res.body
        self.login('root')
        params = {'reposname': '/', 'path': '/noexist'}
        res = self.app.get(url(controller='authz', action='path_changed'), params)
        assert res.status == '200 OK', res.status
        assert '' == res.body, res.body

    def test_set_repos_admin(self):
        try:
            res = self.app.get(url(controller='authz', action='save_authz'))
            assert res.status == '302 Found', res.status
            assert res.location.endswith('/login'), res.location
            self.login('nobody')
            res = self.app.get(url(controller='authz', action='save_authz'))
            assert res.status == '302 Found', res.status
            assert res.location.endswith('/security/failed'), res.location
            self.login('root')
            params = {'reposname': '/', 'admins': ''}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert 'You can not delete yourself from admin list.' == res.body, res.body
        finally:
            self.rollback()

        try:
            params = {'reposname': '/', 'admins': 'root, @some'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
        finally:
            self.rollback()

        try:
            self.login('jiangxin')
            params = {'reposname': '/', 'admins': '&admin'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
        finally:
            self.rollback()

        try:
            self.login('jiangxin')
            params = {'reposname': '/', 'admins': 'root'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert 'You can not delete yourself from admin list.' == res.body, res.body
        finally:
            self.rollback()

        try:
            self.login('root')
            params = {'reposname': '/repos1', 'admins': 'user1'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
        finally:
            self.rollback()

        try:
            self.login('root')
            params = {'reposname': '/repos1', 'admins': 'user1, root'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
        finally:
            self.rollback()

        try:
            self.login('admin1')
            params = {'reposname': '/repos1', 'admins': 'user1, root'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert 'You can not delete yourself from admin list.' == res.body, res.body
            self.login('admin1')
            params = {'reposname': '/repos1', 'admins': 'admin1, admin2'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
        finally:
            self.rollback()

    def test_set_rules(self):
        try:
            authz = self.load_authz()
            module1 = authz.get_module('repos1', 'trunk/src')
            self.assert_(module1 != None, type(module1))
            self.assert_(unicode(module1) == '[repos1:/trunk/src]\nuser1 = \n', unicode(module1).encode('utf-8'))
            self.login('root')
            params = {'reposname': '/repos1', 'path': '/trunk/src', 'admins': '蒋鑫', 'rules': '@管理员=rw\n&别名1=r\n*=\nuser2=r', 'mode1': 'edit', 'mode2': 'edit'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            module1 = authz.get_module('repos1', 'trunk/src')
            self.assert_(module1 != None, type(module1))
            self.assert_(unicode(module1) == '[repos1:/trunk/src]\n&别名1 = r\n* = \n@管理员 = rw\nuser2 = r\n', unicode(module1).encode('utf-8'))
            self.login('蒋鑫')
            params = {'reposname': '/repos1', 'path': '/trunk/src', 'admins': '其他', 'rules': '@管理员=rw\n&别名1=r\n*=\nuser2=r', 'mode1': 'edit', 'mode2': 'edit'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.headers
            assert 'You can not delete yourself from admin list.' in res.body, res.body
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            repos1 = authz.get_repos('reposX')
            self.assert_(repos1 == None, type(repos1))
            self.login('root')
            params = {'reposname': 'reposX', 'admins': '蒋鑫', 'rules': '@管理员=rw\n&别名1=r\n*=\nuser2=r', 'mode1': 'new', 'mode2': 'new'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            repos1 = authz.get_repos('reposX')
            self.assert_(repos1 != None, type(repos1))
            self.assert_(unicode(repos1) == '', unicode(repos1).encode('utf-8'))
            self.assert_(repos1.admins == '蒋鑫', repos1.admins.encode('utf-8'))
        finally:
            self.rollback()

        try:
            authz = self.load_authz()
            repos1 = authz.get_repos('reposX')
            self.assert_(repos1 == None, type(repos1))
            self.login('root')
            params = {'reposname': 'reposX', 'admins': '蒋鑫', 'path': '/项目a', 'rules': '@管理员=rw\n&别名1=r\n*=\nuser2=r', 'mode1': 'new', 'mode2': 'new'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert '' == res.body, res.body
            authz = self.load_authz()
            repos1 = authz.get_repos('reposX')
            self.assert_(unicode(repos1) == '[reposX:/项目a]\n&别名1 = r\n* = \n@管理员 = rw\nuser2 = r\n\n', unicode(repos1).encode('utf-8'))
            self.assert_(repos1.admins == '蒋鑫', repos1.admins.encode('utf-8'))
        finally:
            self.rollback()

        try:
            self.login('root')
            params = {'reposname': 'reposX', 'path': '/trunk/src', 'admins': '蒋鑫', 'rules': '@管理员=rw\n&别名1=r\n*=\nuser2=r', 'mode1': 'edit', 'mode2': 'edit'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert 'Module /trunk/src not exist.' == res.body, res.body
        finally:
            self.rollback()

        try:
            self.login('root')
            params = {'reposname': 'repos1', 'path': '/trunk/myproject', 'admins': '蒋鑫', 'rules': '@管理员=rw\n&别名1=r\n*=\nuser2=r', 'mode1': 'edit', 'mode2': 'edit'}
            res = self.app.get(url(controller='authz', action='save_authz'), params)
            assert res.status == '200 OK', res.status
            assert 'Module /trunk/myproject not exist.' == res.body, res.body
        finally:
            self.rollback()

        return

    def test_delete_authz(self):
        res = self.app.get(url(controller='authz', action='delete_authz'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='authz', action='delete_authz'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        authz = self.load_authz()
        module1 = authz.get_module('document', '/trunk/行政部')
        self.assert_(module1 != None, type(module1))
        self.login('root')
        params = {'reposname': 'document', 'path': '/trunk/行政部'}
        res = self.app.get(url(controller='authz', action='delete_authz'), params)
        authz = self.load_authz()
        module1 = authz.get_module('document', '/trunk/行政部')
        self.assert_(module1 == None, type(module1))
        try:
            self.login('root')
            params = {'reposname': 'document', 'path': '/trunk/行政部', 'revision': '123'}
            res = self.app.get(url(controller='authz', action='delete_authz'), params)
            assert res.status == '200 OK', res.status
            assert 'Update failed! You are working on a out-of-date revision.' in res.body, res.body
        finally:
            self.rollback()

        return
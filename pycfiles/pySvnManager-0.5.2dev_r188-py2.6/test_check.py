# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/tests/functional/test_check.py
# Compiled at: 2010-08-08 03:18:44
from pysvnmanager.tests import *
from pysvnmanager.controllers import check

class TestCheckController(TestController):

    def test_index(self):
        res = self.app.get(url(controller='check', action='index'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='check', action='index'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('admin1')
        res = self.app.get(url(controller='check', action='index'))
        assert res.tmpl_context.reposlist == ['repos1'], res.tmpl_context.reposlist
        self.login('admin2')
        res = self.app.get(url(controller='check', action='index'))
        assert res.tmpl_context.reposlist == ['repos1', 'repos2'], res.tmpl_context.reposlist
        self.login('root')
        res = self.app.get(url(controller='check', action='index'))
        assert res.status == '200 OK', res.status
        assert '<input type="submit" name="submit" value=\'Check Permissions\' class="input-button">' in res.body, res.body
        assert res.tmpl_context.reposlist == ['/', 'document', 'project1', 'project2', 'repos1', 'repos2', 'repos3'], res.tmpl_context.reposlist

    def test_access_map(self):
        res = self.app.get(url(controller='check', action='access_map'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='check', action='access_map'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('root')
        params = {'userinput': 'select', 
           'userselector': 'user1', 
           'reposinput': 'select', 
           'reposselector': '///repos1', 
           'pathinput': 'select', 
           'pathselector': '/trunk/src/test', 
           'abbr': 'True'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert res.status == '200 OK', res.status
        assert "<div id='acl_path_msg'>[repos1:/trunk/src/test] user1 =</div>" in res.body, res.body
        params = {'userinput': 'select', 
           'reposinput': 'select', 
           'pathinput': 'select', 
           'userselector': 'user1', 
           'reposselector': 'reposX', 
           'pathselector': '/trunk/src/test', 
           'abbr': 'False'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert "<div id='acl_path_msg'>User user1 has ReadOnly (RO) rights for module reposX:/trunk/src/test</div><pre>\n==================================================\nAccess map on 'reposX' for user 'user1'\n==================================================\n  * Writable:\n    \n----------------------------------------\n  * Readable:\n    /branches\n    /tags\n    /trunk/src\n----------------------------------------\n  * Denied:\n    /\n    /trunk\n----------------------------------------\n" in res.body, res.body
        params = {'userinput': 'manual', 
           'reposinput': 'manual', 
           'pathinput': 'manual', 
           'username': 'user2', 
           'reposname': 'repos1', 
           'pathname': '/trunk/src/test', 
           'abbr': '1'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert "<div id='acl_path_msg'>[repos1:/trunk/src/test] user2 = r</div>" in res.body, res.body
        params = {'userinput': 'select', 
           'reposinput': 'select', 
           'pathinput': 'manual', 
           'userselector': 'user2', 
           'reposselector': 'reposX', 
           'pathname': '/trunk/', 
           'abbr': '1'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert "<div id='acl_path_msg'>[reposX:/trunk] user2 =</div>" in res.body, res.body
        params = {'userinput': 'select', 
           'reposinput': 'select', 
           'pathinput': 'select', 
           'userselector': 'user3', 
           'reposselector': 'repos1', 
           'pathselector': '/trunk', 
           'abbr': '1'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert "<div id='acl_path_msg'>[repos1:/trunk] user3 =</div>" in res.body, res.body
        params = {'userinput': 'select', 
           'reposinput': 'select', 
           'pathinput': 'select', 
           'userselector': 'user4', 
           'reposselector': 'repos1', 
           'pathselector': '/trunk', 
           'abbr': '1'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert "<div id='acl_path_msg'>[repos1:/trunk] user4 = r</div>" in res.body, res.body
        params = {'userinput': 'select', 
           'reposinput': 'select', 
           'pathinput': 'select', 
           'userselector': 'user4', 
           'reposselector': 'reposX', 
           'pathselector': '/trunk', 
           'abbr': '1'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert "<div id='acl_path_msg'>[reposX:/trunk] user4 = r</div>" in res.body, res.body
        params = {'userinput': 'select', 
           'reposinput': 'select', 
           'pathinput': 'select', 
           'userselector': 'user5', 
           'reposselector': 'reposX', 
           'pathselector': '/trunk', 
           'abbr': '1'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert "<div id='acl_path_msg'>[reposX:/trunk] user5 =</div>" in res.body, res.body
        self.login('admin2')
        params = {'userinput': 'select', 
           'userselector': 'user1', 
           'reposinput': 'select', 
           'reposselector': '*', 
           'pathinput': 'select', 
           'pathselector': '/trunk/src/test', 
           'abbr': 'True'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert res.status == '200 OK', res.status
        assert "<div id='acl_path_msg'>[repos1:/trunk/src/test] user1 =<br>\n[repos2:/trunk/src/test] user1 = r</div><pre>\nuser1 => [repos1]\n----------------------------------------\nRW: \nRO: /branches, /tags, /trunk\nXX: /, /trunk/src\n\n\n\nuser1 => [repos2]\n----------------------------------------\nRW: /, /trunk\nRO: /branches, /tags, /trunk/src\nXX: \n\n</pre>" in res.body, repr(res.body)
        self.login('admin2')
        params = {'userinput': 'select', 
           'reposinput': 'select', 
           'pathinput': 'select', 
           'userselector': 'user1', 
           'reposselector': 'repos3', 
           'pathselector': '/trunk/src/test', 
           'abbr': 'True'}
        res = self.app.get(url(controller='check', action='access_map'), params)
        assert res.status == '200 OK', res.status
        assert res.body == 'Permission denied.', res.location

    def test_authz_path(self):
        res = self.app.get(url(controller='check', action='get_auth_path'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/login'), res.location
        self.login('nobody')
        res = self.app.get(url(controller='check', action='get_auth_path'))
        assert res.status == '302 Found', res.status
        assert res.location.endswith('/security/failed'), res.location
        self.login('root')
        params = {}
        params['repos'] = '/'
        res = self.app.get(url(controller='check', action='get_auth_path'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="...";name[0]="Please choose...";\nid[1]="/trunk/src";name[1]="/trunk/src";\nid[2]="/trunk";name[2]="/trunk";\nid[3]="/";name[3]="/";\nid[4]="/tags";name[4]="/tags";\nid[5]="/branches";name[5]="/branches";\ntotal=6;\n' == res.body, res.body
        params['repos'] = 'noexist'
        res = self.app.get(url(controller='check', action='get_auth_path'), params)
        assert res.status == '200 OK', res.status
        assert '' == res.body, res.body
        params['repos'] = 'repos1'
        res = self.app.get(url(controller='check', action='get_auth_path'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="...";name[0]="Please choose...";\nid[1]="/trunk/src";name[1]="/trunk/src";\nid[2]="/trunk";name[2]="/trunk";\nid[3]="/";name[3]="/";\ntotal=4;\n' == res.body, res.body
        params['repos'] = 'document'
        res = self.app.get(url(controller='check', action='get_auth_path'), params)
        assert res.status == '200 OK', res.status
        assert 'id[0]="...";name[0]="Please choose...";\nid[1]="/branches";name[1]="/branches";\nid[2]="/tags";name[2]="/tags";\nid[3]="/trunk/.htgroup";name[3]="/trunk/.htgroup";\nid[4]="/trunk/tech";name[4]="/trunk/tech";\nid[5]="/trunk/tech/.htaccess";name[5]="/trunk/tech/.htaccess";\nid[6]="/trunk/商务部";name[6]="/trunk/商务部";\nid[7]="/trunk/商务部/.htaccess";name[7]="/trunk/商务部/.htaccess";\nid[8]="/trunk/行政部";name[8]="/trunk/行政部";\nid[9]="/trunk/行政部/.htaccess";name[9]="/trunk/行政部/.htaccess";\ntotal=10;\n' == unicode(res.body, 'utf-8'), res.body
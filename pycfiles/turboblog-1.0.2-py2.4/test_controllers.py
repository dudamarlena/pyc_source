# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turboblog/tests/test_controllers.py
# Compiled at: 2007-03-25 08:41:45
import turbogears as tg
from nose import with_setup
from turbogears import testutil
from turboblog.controllers import Root
from turboblog.model import Blog, User, Tag, hub
import cherrypy
tg.config.update({'visit.on': True, 'identity.on': True, 'identity.failure_url': '/login'})

class TestController(testutil.BrowsingSession):
    __module__ = __name__

    def setUp(self):
        cherrypy.root = Root()
        tg.startup.startTurboGears()

    def tearDown(self):
        """Tests for apps using identity need to stop CP/TG after each test to
        stop the VisitManager thread.
        See http://trac.turbogears.org/turbogears/ticket/1217
        for details.
        """
        tg.startup.stopTurboGears()

    cherrypy.root = Root()

    def test_index_method(self):
        """the index method should return a blog instance"""
        result = testutil.call(cherrypy.root.index)
        u = User(user_name='testuser', display_name='testuser_fullname', password='test_passw', email_address='test_email', avatar=None, about='')
        assert type(result['blog']) == type(Blog(name='xx', tagline='xxx', owner=u))
        return

    def test_logintitle(self):
        """login page should have the right title"""
        testutil.createRequest('/login')
        assert '<title>login</title>' in cherrypy.response.body[0].lower()

    def test_indextitle(self):
        """The indexpage should have the right title"""
        testutil.createRequest('/')
        assert '<title>default blog</title>' in cherrypy.response.body[0].lower()
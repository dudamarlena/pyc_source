# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fosswallproxy0/tests/test_controllers.py
# Compiled at: 2008-02-10 23:37:11
import unittest, turbogears
from turbogears import testutil
from fosswallproxy.controllers import Root
import cherrypy
cherrypy.root = Root()

class TestPages(unittest.TestCase):

    def setUp(self):
        turbogears.startup.startTurboGears()

    def tearDown(self):
        """Tests for apps using identity need to stop CP/TG after each test to
        stop the VisitManager thread. 
        See http://trac.turbogears.org/turbogears/ticket/1217 for details.
        """
        turbogears.startup.stopTurboGears()

    def test_method(self):
        """the index method should return a string called now"""
        import types
        result = testutil.call(cherrypy.root.index)
        assert type(result['now']) == types.StringType

    def test_indextitle(self):
        """The indexpage should have the right title"""
        testutil.createRequest('/')
        response = cherrypy.response.body[0].lower()
        assert '<title>welcome to turbogears</title>' in response
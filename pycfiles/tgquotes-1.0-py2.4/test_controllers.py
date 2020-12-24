# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgquotes\tests\test_controllers.py
# Compiled at: 2006-12-11 14:12:29
from turbogears import testutil
from tgquotes.controllers import Root
import cherrypy
cherrypy.root = Root()

def test_method():
    """the index method should return a string called now"""
    import types
    result = testutil.call(cherrypy.root.index)
    assert type(result['now']) == types.StringType


def test_indextitle():
    """The mainpage should have the right title"""
    testutil.createRequest('/')
    assert '<TITLE>Welcome to TurboGears</TITLE>' in cherrypy.response.body[0]
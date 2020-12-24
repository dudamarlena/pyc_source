# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/cogplanet/tests/test_controllers.py
# Compiled at: 2006-12-28 02:37:03
from turbogears import testutil
from cogplanet.controllers import Root
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
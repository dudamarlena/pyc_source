# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scriptaculous/tests/test_controllers.py
# Compiled at: 2007-11-15 16:33:21
from turbogears import testutil
from scriptaculous.controllers import Root
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
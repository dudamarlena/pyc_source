# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider/tests/test_controllers.py
# Compiled at: 2006-04-09 02:16:03
from turbogears import testutil
from spider.controllers import Root
import cherrypy
cherrypy.root = Root()
q

def test_method():
    import types
    result = testutil.call(cherrypy.root.index)


def test_indextitle():
    """The mainpage should have the right title"""
    testutil.createRequest('/')
    assert '<TITLE>Welcome to Spiderpy</TITLE>' in cherrypy.response.body[0]


def test_start():
    """
    Does the spider start ok
    """

    def create_test_user():
        return 0

    def insert_root_site():
        return 0

    create_test_user()
    assert user_in_db()
    insert_root_site()
    assert root_site_in_db()
    s = spider(user)
    assert s.user == 'testuser'
    newthread(s.start())


def test_stop():
    """
    Does the spider stop ok
    """
    pass
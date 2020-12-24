# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turboblog/tests/test_model.py
# Compiled at: 2007-03-25 08:41:45
from turbogears import testutil, database
from turboblog.model import User, Blog, Tag

class TestUser(testutil.DBTest):
    """User Tests here"""
    __module__ = __name__

    def test_creation(self):
        """Object creation should set the name"""
        obj = User(user_name='gman', email_address='spam@python.not', display_name='Mr G', password='bcbcbcbc', avatar='', about='G.')
        assert obj.display_name == 'Mr G'


class TestBlog(testutil.DBTest):
    """Blog tests here"""
    __module__ = __name__

    def test_creation(self):
        """Blog creation should set a blog name"""
        u = User(user_name='gman', email_address='spam@python.not', display_name='Mr G', password='bcbcbcbc', avatar='', about='G.')
        b = Blog(owner=u, name='My Blog', tagline='Super Blogotest')
        assert b.name == 'My Blog'


class TestTag(testutil.DBTest):
    """Tag Tests here"""
    __module__ = __name__

    def test_creation(self):
        """Tag creation should set a blog"""
        u = User(user_name='gman', email_address='spam@python.not', display_name='Mr G', password='bcbcbcbc', avatar='', about='G.')
        b = Blog(owner=u, name='My Blog', tagline='Super Blogotest')
        t = Tag(name='TurboGears', blog=b)
        assert t.blog == b
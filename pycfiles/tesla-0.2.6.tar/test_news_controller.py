# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthXpProjectName/authxpprojectname/tests/functional/test_news_controller.py
# Compiled at: 2007-09-06 07:54:35
from authxpprojectname.tests import *
from paste.fixture import AppError

class TestNews(TestController):

    def setUp(self):
        TestController.setUp(self)
        self.user = model.User(username='admin', password='admin1', email='admin@localhost')
        self.newsitem = model.NewsItem(title='test', content='testing', author=self.user)
        model.flush_all()

    def test_edit_news(self):
        self.login_user('admin', 'admin1')
        resp = self.app.get(url_for(controller='news', action='edit', id=self.newsitem.id))
        assert resp.status == 200
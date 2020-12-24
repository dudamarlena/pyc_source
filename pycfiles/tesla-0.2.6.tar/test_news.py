# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/tests/unit/test_news.py
# Compiled at: 2007-09-06 07:54:25
from projectname.tests import *
from projectname.lib import fixtures
import os

class TestNews(TestModel):
    __fixtures__ = {'news': model.NewsItem}

    def test_fixtures_loaded(self):
        assert self.fixtures['news']['first']
        assert model.NewsItem.get_by(title='This is the headline')

    def test_execute(self):
        assert model.execute('select * from newsitems')

    def test_dump_data_to_fixtures(self):
        fixtures.dump_data(model.NewsItem)
        fixture_file = os.path.join(os.getcwd(), 'projectname', 'fixtures', 'news', 'newsitems.json')
        assert os.path.exists(fixture_file)
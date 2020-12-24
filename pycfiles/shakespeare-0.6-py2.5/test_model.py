# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/tests/test_model.py
# Compiled at: 2008-10-29 17:02:17
import shakespeare.model as model

class TestMaterial(object):

    @classmethod
    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.url = 'http://www.openshakespeare.org/blah.txt'
        self.text = model.Material(name=self.name, title=self.title, url=self.url)
        model.Session.flush()
        self.textid = self.text.id
        model.Session.clear()

    @classmethod
    def teardown_class(self):
        text = model.Material.query.get(self.textid)
        model.Session.delete(text)
        model.Session.flush()

    def test1(self):
        txt2 = model.Material.query.get(self.textid)
        txt3 = model.Material.byName(self.name)
        assert self.text.id == txt2.id
        assert self.text.id == txt3.id

    def test_get_cache_path(self):
        out = self.text.get_cache_path('plain')
        assert len(out) > 0

    def _test_get_text(self):
        text = model.Material.byName('phoenix_and_the_turtle_gut')
        out = text.get_text()
        out = out.read()
        assert len(out) > 0
        assert out[:26] == 'THE PHOENIX AND THE TURTLE'


class TestStatistic:

    @classmethod
    def setup_class(self):
        self.name = 'test-123'
        self.title = 'Hamlet'
        self.text = model.Material(name=self.name, title=self.title)
        self.word = 'jones'
        self.freq = 5
        self.cc1 = model.Statistic(text=self.text, word=self.word, freq=self.freq)
        model.Session.flush()
        self.statid = self.cc1.id
        model.Session.clear()

    @classmethod
    def teardown_class(self):
        stat = model.Statistic.query.get(self.statid)
        model.Session.delete(stat)
        model.Session.delete(stat.text)
        model.Session.flush()
        model.Session.remove()

    def test1(self):
        out1 = model.Statistic.query.get(self.statid)
        assert out1.text.name == self.name
        assert out1.freq == self.freq

    def test_select(self):
        tresults = model.Statistic.query.filter_by(text=self.text).filter_by(word=self.word)
        num = tresults.count()
        assert num == 1
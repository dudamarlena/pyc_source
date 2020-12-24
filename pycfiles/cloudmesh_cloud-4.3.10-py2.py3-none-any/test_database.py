# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_basic/test_database.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture tests/cm_basic/test_database.py:Test_database.test_001\n\nnosetests -v --nocapture tests/cm_basic/test_database.py\n\nor\n\nnosetests -v tests/cm_basic/test_database.py\n\n'
from pprint import pprint
from cloudmesh_client import CloudmeshDatabase
from cloudmesh_client import DEFAULT
from cloudmesh_client.default import Default
from cloudmesh_client import Printer
from cloudmesh_client.common.util import HEADING

class Test_database:
    cm = CloudmeshDatabase()

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_000(self):
        HEADING('testing DEFAULT add')
        print Printer.write(self.cm.info())
        assert True

    def test_001(self):
        HEADING('testing DEFAULT add')
        m = DEFAULT(name='hallo', value='world')
        self.cm.add(m)
        print 'added'
        n = self.cm.filter_by(kind='default', name='hallo', scope='first')
        print n
        assert n.name == 'hallo'
        assert n.value == 'world'

    def test_002(self):
        HEADING('testing list')
        n = self.cm.find(provider='general', kind='default', scope='first', name='hallo')
        pprint(n)
        assert n.name == 'hallo'
        assert n.value == 'world'

    def test_003(self):
        HEADING('testing find')
        m = DEFAULT(name='hallo', value='world')
        n = self.cm.find(kind='default', scope='all', name='hallo')
        print list(n)
        assert len(list(n)) > 0

    def test_004(self):
        print Printer.write(self.cm.info())
        m = Default.set_counter('index', 2)
        self.cm.add(m)
        o = Default.get_counter('index')
        print ('OOO', o)
        Default.set_counter('index', 0)
        for i in range(0, 10):
            Default.incr_counter('index')

        print Printer.write(self.cm.info())
        c = self.cm.all(kind='default')
        print Printer.write(c, order=['name', 'value', 'provider', 'type'])
        print Default.get_counter(name='index')
        i = Default.get(name='index')
        assert type(i) == int
        assert i == 10
        i = Default.index
        assert type(i) == int
        assert i == 10
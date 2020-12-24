# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_basic/test_tables.py
# Compiled at: 2017-04-23 10:30:41
""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_tables.py:Test_tables.test_001

nosetests -v --nocapture tests/cm_basic/test_tables.py

or

nosetests -v tests/cm_basic/test_tables.py

"""
from pprint import pprint
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.util import HEADING

class Test_tables:
    """define tests for dict printer so you test
    yaml
    json
    table
    csv
    dict
    printing
    """

    def setup(self):
        self.d = [
         {'id': 'a', 
            'x': 1, 
            'y': 2},
         {'id': 'b', 
            'x': 3, 
            'y': 4}]

    def tearDown(self):
        pass

    def test_001_yaml(self):
        HEADING('Printer.write of a yaml object')
        output = Printer.write(self.d, order=None, header=None, output='yaml', sort_keys=True)
        print output
        assert ':' in output
        return

    def test_002_json(self):
        HEADING('Printer.write of a json object')
        output = Printer.write(self.d, order=None, header=None, output='json', sort_keys=True)
        print output
        assert '{' in output
        return

    def test_003_dict(self):
        HEADING('Printer.write of a dict object')
        output = Printer.write(self.d, order=None, header=None, output='dict', sort_keys=True)
        pprint(output)
        assert type(output) == dict
        return

    def test_004_table(self):
        HEADING('Printer.write of a table object')
        output = Printer.write(self.d, order=None, header=None, output='table', sort_keys=True)
        print output
        return

    def test_005_csv(self):
        HEADING('Printer.write of a csv object')
        output = Printer.write(self.d, order=None, header=None, output='csv', sort_keys=True)
        print output
        return
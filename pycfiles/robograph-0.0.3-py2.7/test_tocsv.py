# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_tocsv.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import transcoders
DATA_MATRIX = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
HEADER = ['one', 'two', 'three']
DELIMITER = ','
LINESEP = '\n'
EXPECTED = 'one,two,three\n1,2,3\n4,5,6\n7,8,9'

def test_requirements():
    expected = [
     'data_matrix', 'header_list', 'delimiter', 'linesep']
    instance = transcoders.ToCSV()
    assert instance.requirements == expected


def test_input():
    instance = transcoders.ToCSV()
    instance.input(dict(data_matrix=DATA_MATRIX, header_list=HEADER, delimiter=DELIMITER, linesep=LINESEP))
    instance.set_output_label('any')
    assert instance.output() == EXPECTED


def test_output():
    instance = transcoders.ToCSV(data_matrix=DATA_MATRIX, header_list=HEADER, delimiter=DELIMITER, linesep=LINESEP)
    instance.set_output_label('any')
    assert instance.output() == EXPECTED
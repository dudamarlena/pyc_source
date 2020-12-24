# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_text_file_writer.py
# Compiled at: 2016-07-13 17:51:17
import os
from robograph.datamodel.nodes.lib import files
FILEPATH = os.path.abspath('robograph/datamodel/tests/outputfile.txt')
EXPECTED_CONTENT = 'a\nb\nc'

def check_output_file():
    with open(FILEPATH, 'r') as (of):
        result = of.read()
        assert EXPECTED_CONTENT == result


def test_requirements():
    expected = [
     'filepath', 'encoding', 'data']
    instance = files.TextFileWriter()
    assert instance.requirements == expected


def test_input():
    instance = files.TextFileWriter()
    instance.input(dict(filepath=FILEPATH, encoding='UTF-8', data=EXPECTED_CONTENT))
    instance.set_output_label('any')
    instance.output()
    check_output_file()


def test_output():
    instance = files.TextFileWriter(filepath=FILEPATH, encoding='UTF-8', data=EXPECTED_CONTENT)
    instance.set_output_label('any')
    instance.output()
    check_output_file()
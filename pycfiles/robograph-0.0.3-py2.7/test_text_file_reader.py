# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_text_file_reader.py
# Compiled at: 2016-07-13 17:51:17
import os
from robograph.datamodel.nodes.lib import files
FILEPATH = os.path.abspath('robograph/datamodel/tests/file.txt')

def test_requirements():
    expected = [
     'filepath', 'encoding']
    instance = files.TextFileReader()
    assert instance.requirements == expected


def test_input():
    expected = 'one\ntwo\nthree'
    instance = files.TextFileReader()
    instance.input(dict(filepath=FILEPATH, encoding='UTF-8'))
    instance.set_output_label('any')
    assert instance.output() == expected


def test_output():
    expected = 'one\ntwo\nthree'
    instance = files.TextFileReader(filepath=FILEPATH, encoding='UTF-8')
    instance.set_output_label('any')
    assert instance.output() == expected
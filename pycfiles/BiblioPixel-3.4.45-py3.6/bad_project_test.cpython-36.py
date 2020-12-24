# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/bad_project_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 4770 bytes
import unittest
from unittest import mock
from bibliopixel.project import project
from bibliopixel.util import data_file
from .make import make
PYTHON_FILE = 'driver = {"a": "b"}'
MISSING_LAYOUT = '{"animation": "off", "driver": "dummy"}'
BAD_SECTION = '\n{\n    "bad_section": {"foo": true},\n    "driver": "dummy",\n    "layout": "matrix",\n    "animation": "off"\n}\n'
BAD_SECTION2 = '\n{\n    "verbose": true,\n    "driver": "dummy",\n    "layout": "matrix",\n    "animation": "off"\n}\n'
MISSING_DATATYPE = '\n{\n    "driver": {\n         "width": 16,\n         "height": 16\n    },\n    "layout": "matrix",\n    "animation": "off"\n}\n'
BAD_DRIVER_ATTRIBUTE = '\n{\n    "driver": {\n         "typename": "simpixel",\n         "width": 16,\n         "height": 16,\n         "bad_attribute": 16\n    },\n    "layout": "matrix",\n    "animation": "off"\n}\n'
BAD_LAYOUT_ATTRIBUTE = '\n{\n    "driver": "dummy",\n    "layout": {"typename": "matrix", "bad_attribute": true},\n    "animation": "off"\n}\n'
BAD_ANIMATION_ATTRIBUTE = '\n{\n    "driver": "dummy",\n    "layout": "matrix",\n    "animation": {"typename": "off", "bad_attribute": "hello"}\n}\n\n'
BAD_RUN_ATTRIBUTE = '\n{\n    "driver": "dummy",\n    "layout": "matrix",\n "animation": "off",\n    "run": {"bad_attribute": 23.5}\n}\n'
BAD_PROJECT_ERROR = '\nwhile parsing a block mapping\n  in "<unicode string>", line 1, column 1:\n    driver = {"a": "b"}\n    ^\nexpected <block end>, but found \'}\'\n  in "<unicode string>", line 1, column 19:\n    driver = {"a": "b"}\n                      ^\n'

class BadProjectTest(unittest.TestCase):

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', False)
    def test_bad_project_json(self):
        with self.assertRaises(Exception) as (e):
            make(PYTHON_FILE)
        self.assertEqual(e.exception.args[0::2], ('There was a error in the data file',
                                                  'Expecting value: line 1 column 1 (char 0)'))

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', True)
    def test_bad_project_yaml(self):
        with self.assertRaises(Exception) as (e):
            make(PYTHON_FILE)
        self.assertEqual(str(e.exception).strip(), BAD_PROJECT_ERROR.strip())

    def test_cant_open(self):
        with self.assertRaises(FileNotFoundError) as (e):
            make('this-file-does-not-exist.json')
        self.assertEqual(e.exception.args, (2, 'No such file or directory'))

    def test_bad_section(self):
        with self.assertRaises(ValueError) as (e):
            make(BAD_SECTION)
        self.assertEqual(e.exception.args, ('There is no Project section named "bad_section"', ))

    def test_bad_section2(self):
        with self.assertRaises(ValueError) as (e):
            make(BAD_SECTION2)
        self.assertEqual(e.exception.args, ('There is no Project section named "verbose"', ))

    def test_missing_datatype(self):
        with self.assertRaises(ValueError) as (e):
            make(MISSING_DATATYPE)
        self.assertEqual(e.exception.args, ('Unable to create drivers', 'No "datatype" field in section "drivers"'))

    def test_bad_driver_attribute(self):
        with self.assertRaises(ValueError) as (e):
            make(BAD_DRIVER_ATTRIBUTE)
        self.assertEqual(e.exception.args, ('Unable to create drivers', 'Unknown attribute for driver SimPixel: "bad_attribute"'))

    def test_bad_layout_attribute(self):
        with self.assertRaises(ValueError) as (e):
            make(BAD_LAYOUT_ATTRIBUTE)
        self.assertEqual(e.exception.args, ('Unable to create layout', 'Unknown attribute for layout Matrix: "bad_attribute"'))

    def test_bad_animation_attribute(self):
        animation = make(BAD_ANIMATION_ATTRIBUTE, run_start=False)
        self.assertEqual(animation.exception.args, ('Unknown attribute for animation Off: "bad_attribute"', ))

    def test_bad_run_attribute(self):
        animation = make(BAD_RUN_ATTRIBUTE, run_start=False)
        self.assertEqual(animation.exception.args, ('Unknown attribute for run: "bad_attribute"', ))

    def test_missing_layout(self):
        animation = make(MISSING_LAYOUT, run_start=False)
        self.assertEqual(animation.__class__.__name__, 'Off')
        self.assertEqual(animation.layout.__class__.__name__, 'Strip')

    def test_missing_everything(self):
        animation = make('{}', run_start=False)
        self.assertEqual(animation.__class__.__name__, 'Animation')
        self.assertEqual(animation.layout.__class__.__name__, 'Strip')